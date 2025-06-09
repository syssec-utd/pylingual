import inspect
import logging
import sys
from odoo import SUPERUSER_ID, api, models
from .models.spec_models import SpecModel, StackedModel
_logger = logging.getLogger(__name__)

def post_init_hook(cr, registry, module_name, spec_module):
    """
    Automatically generate access rules for spec models
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    remaining_models = get_remaining_spec_models(cr, registry, module_name, spec_module)
    fields = ['id', 'name', 'model_id/id', 'group_id/id', 'perm_read', 'perm_write', 'perm_create', 'perm_unlink']
    access_data = []
    for model in remaining_models:
        underline_name = model.replace('.', '_')
        model_id = '%s_spec.model_%s' % (module_name, underline_name)
        access_data.append(['access_%s_user' % (underline_name,), underline_name, model_id, '%s.group_user' % (module_name,), '1', '0', '0', '0'])
        access_data.append(['access_%s_manager' % (underline_name,), underline_name, model_id, '%s.group_manager' % (module_name,), '1', '1', '1', '1'])
    env['ir.model.access'].load(fields, access_data)

def get_remaining_spec_models(cr, registry, module_name, spec_module):
    """
    Figure out the list of spec models not injected into existing
    Odoo models.
    """
    cr.execute("select ir_model.model from ir_model_data\n               join ir_model on res_id=ir_model.id\n               where ir_model_data.model='ir.model'\n               and module=%s;", (module_name,))
    module_models = [i[0] for i in cr.fetchall() if registry.get(i[0]) and (not registry[i[0]]._abstract)]
    injected_models = set()
    for model in module_models:
        base_class = registry[model]
        if hasattr(base_class, '_inherit'):
            injected_models.add(base_class._name)
            for cls in base_class.mro():
                if hasattr(cls, '_inherit') and cls._inherit:
                    if isinstance(cls._inherit, list):
                        inherit_list = cls._inherit
                    else:
                        inherit_list = [cls._inherit]
                    for inherit in inherit_list:
                        if inherit.startswith('spec.mixin.'):
                            injected_models.add(cls._name)
    injected_classes = set()
    remaining_models = set()
    for m in injected_models:
        c = SpecModel._odoo_name_to_class(m, spec_module)
        if c is not None:
            injected_classes.add(c)
    for model in module_models:
        base_class = registry[model]
        if hasattr(base_class, '_stacked'):
            node = SpecModel._odoo_name_to_class(base_class._stacked, spec_module)
            base_class._visit_stack(node, injected_classes, base_class._stacked.split('.')[-1], registry, cr)
    all_spec_models = {c._name for (name, c) in inspect.getmembers(sys.modules[spec_module], inspect.isclass)}
    remaining_models = remaining_models.union({i for i in all_spec_models if i not in [c._name for c in injected_classes]})
    return remaining_models

def register_hook(env, module_name, spec_module, force=False):
    """
    Called by Model#_register_hook once all modules are loaded.
    Here we take all spec models that are not injected in existing concrete
    Odoo models and we make them concrete automatically with
    their _auto_init method that will create their SQL DDL structure.
    """
    load_key = '_%s_loaded' % (spec_module,)
    if hasattr(env.registry, load_key) and (not force):
        return
    setattr(env.registry, load_key, True)
    remaining_models = get_remaining_spec_models(env.cr, env.registry, module_name, spec_module)
    for name in remaining_models:
        spec_class = StackedModel._odoo_name_to_class(name, spec_module)
        spec_class._module = 'fiscal'
        fields = env[spec_class._name].fields_get_keys()
        rec_name = next(filter(lambda x: x.startswith(env[spec_class._name]._field_prefix) and '_choice' not in x, fields))
        c = type(name, (SpecModel, spec_class), {'_name': name, '_inherit': [spec_class._inherit, 'spec.mixin'], '_original_module': 'fiscal', '_odoo_module': module_name, '_spec_module': spec_module, '_rec_name': rec_name})
        models.MetaModel.module_to_models[module_name] += [c]
        c._build_model(env.registry, env.cr)
        env[name]._prepare_setup()
        env[name]._setup_base()
        env[name]._setup_fields()
        env[name]._setup_complete()
    hook_key = '_%s_need_hook' % (module_name,)
    if hasattr(env.registry, hook_key) and getattr(env.registry, hook_key):
        env.registry.init_models(env.cr, remaining_models, {'module': module_name})
        setattr(env.registry, hook_key, False)