import logging
logger = logging.getLogger(__name__)
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from lino.api import dd, rt
from lino import mixins
from etgen.html import E
from lino.modlib.system.choicelists import PeriodEvents
from lino.mixins.human import parse_name
from lino_xl.lib.contacts.mixins import ContactRelated
from lino_xl.lib.addresses.choicelists import AddressTypes
from lino_xl.lib.boards.mixins import BoardDecision
from lino_xl.lib.excerpts.mixins import ExcerptTitle
from lino_welfare.modlib.pcsw.roles import SocialUser
from .roles import AidsUser, AidsStaff
from .mixins import Confirmable, Confirmation
from .choicelists import ConfirmationTypes, AidRegimes, ConfirmationStates
from lino.mixins import ObservedDateRange

class Category(mixins.BabelNamed):

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class Categories(dd.Table):
    model = 'aids.Category'
    required_roles = dd.login_required(AidsStaff)
    column_names = 'name *'
    order_by = ['name']
    detail_layout = '\n    id name\n    aids.IncomeConfirmationsByCategory\n    '

class AidType(ContactRelated, ExcerptTitle):

    class Meta:
        verbose_name = _('Aid Type')
        verbose_name_plural = _('Aid Types')
    aid_regime = AidRegimes.field(default=AidRegimes.as_callable('financial'))
    confirmation_type = ConfirmationTypes.field(blank=True)
    short_name = models.CharField(max_length=50, blank=True)
    board = dd.ForeignKey('boards.Board', blank=True, null=True)
    print_directly = models.BooleanField(_('Print directly'), default=True)
    is_integ_duty = models.BooleanField(_('Integration duty'), default=False, help_text=_('Whether aid grantings of this type are considered as duty for integration contract.'))
    is_urgent = models.BooleanField(_('Urgent'), default=False, help_text=_('Whether aid grantings of this type are considered as urgent.'))
    confirmed_by_primary_coach = models.BooleanField(_('Confirmed by primary coach'), default=True, help_text=_("Whether grantings for this aid type are to be signed by the client's primary coach."))
    pharmacy_type = dd.ForeignKey('clients.ClientContactType', blank=True, null=True)
    address_type = AddressTypes.field(blank=True, null=True, help_text=_('Which client address to print on confirmations. If this is empty, Lino will use the primary address.'))
    body_template = models.CharField(max_length=200, verbose_name=_('Body template'), blank=True, help_text='The body template to use instead of the default body template as defined for the excerpt type.')

    @dd.chooser(simple_values=True)
    def body_template_choices(cls, confirmation_type):
        if not confirmation_type:
            return []
        tplgroup = confirmation_type.model.get_template_group()
        return settings.SITE.list_templates('.body.html', tplgroup)

class AidTypes(dd.Table):
    model = 'aids.AidType'
    required_roles = dd.login_required(AidsStaff)
    column_names = 'name board short_name *'
    order_by = ['name']
    insert_layout = '\n    name\n    confirmation_type\n    '
    detail_layout = '\n    id short_name confirmation_type\n    name\n    excerpt_title\n    body_template print_directly is_integ_duty is_urgent     confirmed_by_primary_coach board\n    company contact_person contact_role pharmacy_type\n    aids.GrantingsByType\n    '

class GrantingManager(models.Manager):

    def get_by_aidtype(self, client, period, **aidtype_filter):
        at_list = rt.models.aids.AidType.objects.filter(**aidtype_filter)
        qs = self.get_queryset()
        qs = qs.filter(client=client, aid_type__in=at_list)
        qs = PeriodEvents.active.add_filter(qs, period)
        if qs.count() == 1:
            return qs[0]
        return None

class Granting(Confirmable, BoardDecision):

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Granting')
        verbose_name = _('Aid granting')
        verbose_name_plural = _('Aid grantings')
    objects = GrantingManager()
    client = dd.ForeignKey('pcsw.Client')
    aid_type = dd.ForeignKey('aids.AidType')
    category = dd.ForeignKey('aids.Category', blank=True, null=True)
    request_date = models.DateField(_('Date of request'), blank=True, null=True)

    @classmethod
    def get_confirmable_fields(cls):
        return 'client signer aid_type board decision_date start_date end_date category request_date'

    def full_clean(self):
        super(Granting, self).full_clean()
        if self.client_id and (not self.signer_id) and self.aid_type_id and self.aid_type.confirmed_by_primary_coach:
            self.signer = self.client.get_primary_coach()

    def __str__(self):
        if self.aid_type_id is not None:
            t1 = self.aid_type.short_name or str(self.aid_type)
            return '%s/%s/%s' % (t1, dd.fds(self.start_date), self.client.id)
        return '%s #%s' % (self._meta.verbose_name, self.pk)

    def get_aid_type(self):
        return self.aid_type

    def get_pharmacies(self, **kw):
        pt = self.aid_type.pharmacy_type
        if pt:
            return rt.models.contacts.Company.objects.filter(client_contact_type=pt, **kw)
        return []

    @dd.displayfield(_('Actions'))
    def custom_actions(self, ar, **kw):
        if self.aid_type_id is None or ar is None:
            return ''
        at = self.aid_type
        ct = at.confirmation_type
        if not ct:
            return ''
        sar = ct.table_class.insert_action.request_from(ar, master_instance=self)
        txt = _('Create confirmation')
        btn = sar.ar2button(None, txt, icon_name=None)
        return E.div(btn)
dd.update_field(Granting, 'start_date', verbose_name=_('Applies from'), default=dd.today, null=False, blank=False)
dd.update_field(Granting, 'end_date', verbose_name=_('until'))

class Grantings(dd.Table):
    model = 'aids.Granting'
    required_roles = dd.login_required(AidsUser)
    order_by = ['-start_date']
    detail_layout = '\n    id client user signer workflow_buttons\n    request_date board decision_date\n    aid_type category start_date end_date custom_actions\n    aids.ConfirmationsByGranting\n    '
    insert_layout = '\n    client\n    aid_type signer\n    board decision_date\n    start_date end_date\n    '
    parameters = dict(observed_event=dd.PeriodEvents.field(blank=True, default=dd.PeriodEvents.as_callable('active')), board=dd.ForeignKey('boards.Board', blank=True, null=True, help_text=_('Only rows decided by this board.')), aid_type=dd.ForeignKey('aids.AidType', blank=True, null=True, help_text=_('Only confirmations about this aid type.')))
    params_layout = 'board aid_type user signer state'

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Grantings, self).get_request_queryset(ar)
        pv = ar.param_values
        if pv.aid_type:
            qs = qs.filter(aid_type=pv.aid_type)
        if pv.board:
            qs = qs.filter(board=pv.board)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Grantings, self).get_title_tags(ar):
            yield t
        pv = ar.param_values
        for k in ('board', 'aid_type'):
            v = pv[k]
            if v:
                yield (str(self.parameters[k].verbose_name) + ' ' + str(v))

class AllGrantings(Grantings):
    required_roles = dd.login_required(AidsStaff)

class MyPendingGrantings(Grantings):
    required_roles = dd.login_required(SocialUser)
    column_names = 'client aid_type category start_date end_date user workflow_buttons *'
    label = _('Grantings to confirm')
    auto_fit_column_widths = True
    welcome_message_when_count = 0

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyPendingGrantings, self).param_defaults(ar, **kw)
        kw.update(signer=ar.get_user())
        kw.update(state=ConfirmationStates.requested)
        return kw

class GrantingsByClient(Grantings):
    master_key = 'client'
    column_names = 'detail_link start_date end_date signer workflow_buttons board custom_actions *'
    auto_fit_column_widths = True
    insert_layout = '\n    aid_type\n    board decision_date\n    start_date end_date\n    '

class GrantingsByType(Grantings):
    auto_fit_column_widths = True
    master_key = 'aid_type'
    column_names = 'detail_link client start_date end_date id *'

class Confirmations(dd.Table):
    """Abstract base class for all confirmation tables.

    Note that Lino is not currently able to render tables on abstract
    database models.

    """
    required_roles = dd.login_required(AidsStaff)
    order_by = ['-created']
    column_names = 'detail_link created user printed start_date end_date *'
    parameters = dict(observed_event=dd.PeriodEvents.field(blank=True, default=dd.PeriodEvents.as_callable('active')), board=dd.ForeignKey('boards.Board', blank=True, null=True, help_text=_('Only rows decided by this board.')), aid_type=dd.ForeignKey('aids.AidType', blank=True, null=True, help_text=_('Only confirmations about this aid type.')))
    params_layout = 'start_date end_date observed_event board signer user\n    aid_type state client gender'

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Confirmations, self).get_request_queryset(ar)
        pv = ar.param_values
        if pv.observed_event:
            qs = pv.observed_event.add_filter(qs, pv)
        if pv.aid_type:
            qs = qs.filter(granting__aid_type=pv.aid_type)
        if pv.gender:
            qs = qs.filter(client__gender=pv.gender)
        if pv.board:
            qs = qs.filter(granting__board=pv.board)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Confirmations, self).get_title_tags(ar):
            yield t
        pv = ar.param_values
        for k in ('signer', 'board', 'aid_type', 'state'):
            v = pv[k]
            if v:
                yield (str(self.parameters[k].verbose_name) + ' ' + str(v))

    @dd.virtualfield(models.IntegerField(_('Adults')))
    def num_adults(self, obj, ar):
        ac = rt.models.households.RefundsByPerson.get_adults_and_children(obj.client, obj.start_date or obj.end_date or dd.today())
        return ac[0]

    @dd.virtualfield(models.IntegerField(_('Children')))
    def num_children(self, obj, ar):
        ac = rt.models.households.RefundsByPerson.get_adults_and_children(obj.client, obj.start_date or obj.end_date or dd.today())
        return ac[1]

class PrintConfirmation(dd.Action):
    label = _('Print')
    icon_name = 'printer'

    def run_from_ui(self, ar, **kw):
        for obj in ar.selected_rows:
            obj.do_print.run_from_ui(ar)

class ConfirmationsByGranting(dd.VirtualTable):
    """Shows the confirmations issued for a given granting.

    This is a "pseudo-virtual" table because it operates on normal
    database objects.  It needs to be virtual because Confirmation
    is an abstract model.  In order to have a detail and a print
    function, it must define `get_pk_field` and `get_row_by_pk`.
    """
    label = _('Issued confirmations')
    required_roles = dd.login_required(AidsUser)
    master = 'aids.Granting'
    column_names = 'detail_link created user signer printed start_date end_date *'
    do_print = PrintConfirmation()

    @classmethod
    def get_data_rows(self, ar):
        mi = ar.master_instance
        if mi is None:
            return []
        ct = mi.aid_type.confirmation_type
        if ct is None:
            return []
        return ct.model.objects.filter(granting=mi).order_by('-created')

    @classmethod
    def get_pk_field(self):
        return SimpleConfirmation._meta.pk

    @classmethod
    def get_row_by_pk(self, ar, pk):
        mi = ar.master_instance
        if mi is None:
            return None
        ct = mi.aid_type.confirmation_type
        if ct is None:
            return None
        return ct.model.objects.get(pk=pk)

    @dd.virtualfield('aids.SimpleConfirmation.start_date')
    def start_date(self, obj, ar):
        return obj.start_date

    @dd.virtualfield('aids.SimpleConfirmation.end_date')
    def end_date(self, obj, ar):
        return obj.end_date

    @dd.virtualfield('aids.SimpleConfirmation.created')
    def created(self, obj, ar):
        return obj.created

    @dd.virtualfield('aids.SimpleConfirmation.user')
    def user(self, obj, ar):
        return obj.user

    @dd.virtualfield('aids.SimpleConfirmation.signer')
    def signer(self, obj, ar):
        return obj.signer

    @dd.displayfield(_('Printed'))
    def printed(self, obj, ar):
        return obj._meta.get_field('printed').value_from_object(obj, ar)
dd.update_field(ConfirmationsByGranting, 'detail_link', verbose_name=_('Confirmation'))

class SimpleConfirmation(Confirmation):
    """This is when a social agent confirms that a client benefits of some
simple aid during a given period.

    """

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'SimpleConfirmation')
        verbose_name = _('Simple confirmation')
        verbose_name_plural = _('Simple confirmations')

class SimpleConfirmations(Confirmations):
    model = 'aids.SimpleConfirmation'
    required_roles = dd.login_required(AidsUser)
    detail_layout = dd.DetailLayout('\n    id client user signer workflow_buttons\n    granting start_date end_date\n    # confirmation_text\n    company contact_person language printed\n    remark\n    ')

class AllSimpleConfirmations(SimpleConfirmations):
    required_roles = dd.login_required(AidsStaff)
    column_names = 'id client start_date end_date granting client__address_column client__gender num_adults num_children *'

class SimpleConfirmationsByGranting(SimpleConfirmations):
    master_key = 'granting'
    insert_layout = dd.InsertLayout('\n    start_date end_date\n    company contact_person language\n    remark\n    # client granting:25\n    ', window_size=(50, 16))
    column_names = 'id client granting start_date end_date *'
ConfirmationTypes.add_item(SimpleConfirmation, SimpleConfirmationsByGranting)

class IncomeConfirmation(Confirmation):
    """This is when a social agent confirms that a client benefits of a
    given income during a given period.

    """

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'IncomeConfirmation')
        verbose_name = _('Income confirmation')
        verbose_name_plural = _('Income confirmations')
    category = dd.ForeignKey('aids.Category', blank=True, null=True)
    amount = dd.PriceField(_('Amount'), blank=True, null=True)

class IncomeConfirmations(Confirmations):
    model = 'aids.IncomeConfirmation'
    required_roles = dd.login_required(AidsUser)
    detail_layout = dd.DetailLayout('\n    client user signer workflow_buttons printed\n    company contact_person language\n    granting:25 start_date end_date\n    category amount id\n    remark\n    ')

class AllIncomeConfirmations(IncomeConfirmations):
    required_roles = dd.login_required(AidsStaff)
    column_names = 'id client start_date end_date granting client__address_column client__gender num_adults num_children *'

class IncomeConfirmationsByGranting(IncomeConfirmations):
    """Show the confirmations of a Granting whose `aid_type` has
    :class:`IncomeConfirmation` as `confirmation_type`.

    """
    master_key = 'granting'
    insert_layout = dd.InsertLayout('\n    client granting:25\n    start_date end_date\n    category amount\n    company contact_person language\n    remark\n    ', window_size=(70, 20), hidden_elements='client granting')
    column_names = 'id client category amount start_date end_date *'

class IncomeConfirmationsByCategory(IncomeConfirmations):
    master_key = 'category'
ConfirmationTypes.add_item(IncomeConfirmation, IncomeConfirmationsByGranting)
dd.inject_field('clients.ClientContactType', 'can_refund', models.BooleanField(_('Can refund'), default=False, help_text=_('Whether persons of this type can be used as doctor of a refund confirmation.')))

class RefundConfirmation(Confirmation):
    """This is when a social agent confirms that a client benefits of a
    refund aid (Kostenrückerstattung) during a given period.

    .. attribute:: doctor_type

    You can leave this field empty, but if you do so, you must specify
    a :attr:`doctor`, and Lino will use that doctor's type.

    .. attribute:: doctor

    Pointer to the doctor (an instance of :class:`contacts.Person
    <lino_xl.lib.contacts.models.Person>`).

    .. attribute:: pharmacy

    The pharmacy for which this confirmation is being issued.

    The selection list will work only if the aid type defined on the
    granting of this confirmation has a pharmacy_type defined.

    """

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'RefundConfirmation')
        verbose_name = _('Refund confirmation')
        verbose_name_plural = _('Refund confirmations')
    doctor_type = dd.ForeignKey('clients.ClientContactType', verbose_name=_('Doctor type'), blank=True)
    doctor = dd.ForeignKey('contacts.Person', verbose_name=_('Doctor'), blank=True, null=True)
    pharmacy = dd.ForeignKey('contacts.Company', verbose_name=_('Pharmacy'), blank=True, null=True)

    def on_create(self, ar):
        super(RefundConfirmation, self).on_create(ar)
        if self.granting_id:
            qs = self.granting.get_pharmacies(clients_clientcontact_set_by_company__client=self.client)
            if len(qs) == 1:
                self.pharmacy = qs[0]

    @dd.chooser()
    def pharmacy_choices(cls, granting):
        if granting:
            return granting.get_pharmacies()
        return []

    @dd.chooser()
    def doctor_choices(cls, doctor_type):
        fkw = dict()
        if doctor_type:
            fkw.update(client_contact_type=doctor_type)
        else:
            qs = rt.models.clients.ClientContactType.objects.filter(can_refund=True)
            fkw.update(client_contact_type__in=qs)
        return rt.models.contacts.Person.objects.filter(**fkw)

    def create_doctor_choice(self, text, ar=None):
        """The :meth:`create_FOO_choice
        <lino.core.model.Model.create_FOO_choice>` method which turns
        :attr:`doctor` into a learning combobox.

        This is called when an unknown doctor name was given in order
        to auto-create a new doctor.

        The text is expected to be the doctor's name, formatted
        "first_name last_name" without title.

        Doctors are stored as :class:`contacts.Person
        <lino_xl.lib.contacts.models.Person>`.

        The :attr:`title` field of the new doctor will be "Dr." (this
        is currently not configurable).

        The user can enter title, phone number and more by clicking on
        the pointer arrow when the confirmation has been created.

        """
        if not self.doctor_type_id:
            raise ValidationError(_('Cannot auto-create without doctor type'))
        Person = rt.models.contacts.Person
        kw = parse_name(text)
        if len(kw) != 2:
            raise ValidationError('Cannot find first and last names in %r to                 auto-create doctor', text)
        kw.update(client_contact_type=self.doctor_type)
        kw.update(title=_('Dr.'))
        p = Person(**kw)
        p.full_clean()
        p.save()
        return p

    @dd.chooser()
    def doctor_type_choices(cls):
        return rt.models.clients.ClientContactType.objects.filter(can_refund=True)

    def full_clean(self):
        super(RefundConfirmation, self).full_clean()
        if self.doctor_type_id is None and self.doctor_id:
            self.doctor_type = self.doctor.client_contact_type
        if not self.doctor_type_id:
            raise ValidationError(_('Please specify a doctor type.'))

class RefundConfirmations(Confirmations):
    model = 'aids.RefundConfirmation'
    required_roles = dd.login_required(AidsUser)
    detail_layout = dd.DetailLayout('\n    id client user signer workflow_buttons\n    granting:25 start_date end_date\n    doctor_type doctor pharmacy\n    company contact_person language printed\n    remark\n    ')

class AllRefundConfirmations(RefundConfirmations):
    required_roles = dd.login_required(AidsStaff)
    column_names = 'id client start_date end_date granting client__address_column client__gender num_adults num_children *'

class RefundConfirmationsByGranting(RefundConfirmations):
    master_key = 'granting'
    insert_layout = dd.InsertLayout('\n    # client granting:25\n    start_date end_date\n    doctor_type doctor pharmacy\n    company contact_person language printed\n    remark\n    ', window_size=(70, 20))
    column_names = 'id client granting start_date end_date *'
ConfirmationTypes.add_item(RefundConfirmation, RefundConfirmationsByGranting)

class SubmitInsertAndPrint(dd.SubmitInsert):
    """A customized variant of the standard :class:`SubmitInsert
    <dd.SubmitInsert>` which prints the `Confirmation` after
    successful creation (if :attr:`AidType.print_directly` is checked).

    """

    def run_from_ui(self, ar, **kw):
        elem = ar.create_instance_from_request()
        self.save_new_instance(ar, elem)
        ar.set_response(close_window=True)
        if elem.granting and elem.granting.aid_type.print_directly:
            elem.do_print.run_from_ui(ar, **kw)
'Overrides the :attr:`submit_insert\n<lino.core.model.Model.submit_insert>` action of :class:`Confirmation`\nwith our custom action :class:`SubmitInsertAndPrint`.\n\n'
dd.update_model(Confirmation, submit_insert=SubmitInsertAndPrint())