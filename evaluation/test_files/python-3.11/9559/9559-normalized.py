def Entity(cls, ent: Entity, ctx: HwtSerializerCtx):
    """
        Entity is just forward declaration of Architecture, it is not used
        in most HDL languages as there is no recursion in hierarchy
        """
    cls.Entity_prepare(ent, ctx, serialize=False)
    ent.name = ctx.scope.checkedName(ent.name, ent, isGlobal=True)
    ports = list(map(lambda p: (p.name, cls.HdlType(p._dtype, ctx)), ent.ports))
    return unitHeadTmpl.render(name=ent.name, ports=ports)