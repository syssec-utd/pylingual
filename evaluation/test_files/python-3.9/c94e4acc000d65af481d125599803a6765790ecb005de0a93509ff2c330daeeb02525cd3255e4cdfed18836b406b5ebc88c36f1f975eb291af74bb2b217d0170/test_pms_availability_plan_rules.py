import datetime
from odoo import fields
from odoo.exceptions import ValidationError
from .common import TestPms

class TestPmsRoomTypeAvailabilityRules(TestPms):

    def setUp(self):
        super().setUp()
        self.pms_property2 = self.env['pms.property'].create({'name': 'Property 2', 'company_id': self.company1.id, 'default_pricelist_id': self.pricelist1.id})
        self.pricelist2 = self.env['product.pricelist'].create({'name': 'test pricelist 1', 'pms_property_ids': [(4, self.pms_property1.id), (4, self.pms_property2.id)]})
        self.sale_channel_direct1 = self.env['pms.sale.channel'].create({'name': 'Door', 'channel_type': 'direct'})
        self.test_room_type_availability1 = self.env['pms.availability.plan'].create({'name': 'Availability plan for TEST', 'pms_pricelist_ids': [(6, 0, [self.pricelist2.id])]})
        self.pms_property3 = self.env['pms.property'].create({'name': 'MY PMS TEST', 'company_id': self.company1.id, 'default_pricelist_id': self.pricelist2.id})
        self.test_room_type_single = self.env['pms.room.type'].create({'pms_property_ids': [self.pms_property3.id], 'name': 'Single Test', 'default_code': 'SNG_Test', 'class_id': self.room_type_class1.id})
        self.test_room_type_double = self.env['pms.room.type'].create({'pms_property_ids': [(4, self.pms_property3.id)], 'name': 'Double Test', 'default_code': 'DBL_Test', 'class_id': self.room_type_class1.id})
        self.test_room1_double = self.env['pms.room'].create({'pms_property_id': self.pms_property3.id, 'name': 'Double 201 test', 'room_type_id': self.test_room_type_double.id, 'capacity': 2})
        self.test_room2_double = self.env['pms.room'].create({'pms_property_id': self.pms_property3.id, 'name': 'Double 202 test', 'room_type_id': self.test_room_type_double.id, 'capacity': 2})
        self.test_room1_single = self.env['pms.room'].create({'pms_property_id': self.pms_property3.id, 'name': 'Single 101 test', 'room_type_id': self.test_room_type_single.id, 'capacity': 1})
        self.test_room2_single = self.env['pms.room'].create({'pms_property_id': self.pms_property3.id, 'name': 'Single 102 test', 'room_type_id': self.test_room_type_single.id, 'capacity': 1})
        self.partner1 = self.env['res.partner'].create({'name': 'Charles'})

    def test_availability_rooms_all(self):
        """
        Check the availability of rooms in a property with an availability plan without
        availability rules.
        ---------------------
        The checkin and checkout dates on which the availability will be checked are saved
        in a variable and in another all the rooms of the property are also saved. Then the
        free_room_ids compute field is called which should return the number of available rooms
        of the property and they are saved in another variable with which it is verified that
        all the rooms have been returned because there are no availability rules for that plan.
        """
        checkin = fields.date.today()
        checkout = (fields.datetime.today() + datetime.timedelta(days=4)).date()
        test_rooms_double_rooms = self.env['pms.room'].search([('pms_property_id', '=', self.pms_property3.id)])
        pms_property = self.pms_property3.with_context(checkin=checkin, checkout=checkout)
        result = pms_property.free_room_ids
        obtained = all((elem.id in result.ids for elem in test_rooms_double_rooms))
        self.assertTrue(obtained, "Availability should contain the test roomsbecause there's no availability rules for them.")

    def test_plan_avail_update_to_one(self):
        """
        Check that the plan avail on a room is updated when the real avail is changed
        --------------------------------------------------------------
        Room type with 2 rooms, new reservation with this room type, the plan avail
        must to be updated to 1. You must know that the pricelist2 is linked
        with the plan test_room_type_availability1
        """
        checkin = fields.date.today()
        checkout = (fields.datetime.today() + datetime.timedelta(days=4)).date()
        room_type = self.test_room_type_double
        self.test_room_type_availability_rule1 = self.env['pms.availability.plan.rule'].create({'availability_plan_id': self.test_room_type_availability1.id, 'room_type_id': self.test_room_type_double.id, 'date': fields.datetime.today(), 'pms_property_id': self.pms_property3.id})
        self.env['pms.reservation'].create({'pms_property_id': self.pms_property3.id, 'checkin': checkin, 'checkout': checkout, 'partner_id': self.partner1.id, 'room_type_id': room_type.id, 'sale_channel_origin_id': self.sale_channel_direct1.id})
        result = self.test_room_type_availability_rule1.plan_avail
        self.assertEqual(result, 1, 'There should be only one room in the result of the availability planbecause the real avail is 1 and the availability planis updated.')

    def test_plan_avail_update_to_zero(self):
        """
        Check that the plan avail on a room is updated when the real avail is changed
        with real avail 0
        --------------------------------------------------------------
        Room type with 2 rooms, two new reservations with this room type, the plan avail
        must to be updated to 0. You must know that the pricelist2 is linked
        with the plan test_room_type_availability1
        """
        checkin = fields.date.today()
        checkout = (fields.datetime.today() + datetime.timedelta(days=4)).date()
        room_type = self.test_room_type_double
        self.test_room_type_availability_rule1 = self.env['pms.availability.plan.rule'].create({'availability_plan_id': self.test_room_type_availability1.id, 'room_type_id': self.test_room_type_double.id, 'date': fields.datetime.today(), 'pms_property_id': self.pms_property3.id})
        self.env['pms.reservation'].create({'pms_property_id': self.pms_property3.id, 'checkin': checkin, 'checkout': checkout, 'partner_id': self.partner1.id, 'room_type_id': room_type.id, 'sale_channel_origin_id': self.sale_channel_direct1.id})
        self.env['pms.reservation'].create({'pms_property_id': self.pms_property3.id, 'checkin': checkin, 'checkout': checkout, 'partner_id': self.partner1.id, 'room_type_id': room_type.id, 'sale_channel_origin_id': self.sale_channel_direct1.id})
        result = self.test_room_type_availability_rule1.plan_avail
        self.assertEqual(result, 0, 'There should be zero in the result of the availability planbecause the real avail is 0 and the availability planis updated.')

    def test_availability_rooms_all_lines(self):
        """
        Check the availability of rooms in a property with an availability plan without
        availability rules and passing it the reservation lines of a reservation for that
        property.
        -----------------
        The checkin and checkout dates on which the availability will be checked are saved
        in a variable and in another all the rooms of the property are also saved. Then create
        a reservation for this property and the free_room_ids compute field is called with the
        parameters checkin, checkout and the reservation lines of the reservation as a curent
        lines, this method should return the number of available rooms of the property. Then the
        result is saved in another variable with which it is verified that all the rooms have
        been returned because there are no availability rules for that plan.
        """
        checkin = fields.date.today()
        checkout = (fields.datetime.today() + datetime.timedelta(days=4)).date()
        test_rooms_double_rooms = self.env['pms.room'].search([('pms_property_id', '=', self.pms_property3.id)])
        test_reservation = self.env['pms.reservation'].create({'pms_property_id': self.pms_property3.id, 'checkin': checkin, 'checkout': checkout, 'partner_id': self.partner1.id, 'sale_channel_origin_id': self.sale_channel_direct1.id})
        pms_property = self.pms_property3.with_context(checkin=checkin, checkout=checkout, current_lines=test_reservation.reservation_line_ids.ids)
        result = pms_property.free_room_ids
        obtained = all((elem.id in result.ids for elem in test_rooms_double_rooms))
        self.assertTrue(obtained, "Availability should contain the test roomsbecause there's no availability rules for them.")

    def test_availability_rooms_room_type(self):
        """
        Check the availability of a room type for a property.
        ----------------
        Double rooms of a property are saved in a variable. The free_room_ids compute field
        is called giving as parameters checkin, checkout and the type of room (in this
        case double). Then with the all () function we check that all rooms of this type
        were returned.
        """
        test_rooms_double_rooms = self.env['pms.room'].search([('pms_property_id', '=', self.pms_property3.id), ('room_type_id', '=', self.test_room_type_double.id)])
        pms_property = self.pms_property3.with_context(checkin=fields.date.today(), checkout=(fields.datetime.today() + datetime.timedelta(days=4)).date(), room_type_id=self.test_room_type_double.id)
        result = pms_property.free_room_ids
        obtained = all((elem.id in result.ids for elem in test_rooms_double_rooms))
        self.assertTrue(obtained, "Availability should contain the test roomsbecause there's no  availability rules for them.")

    def test_availability_closed_no_room_type(self):
        """
        Check that rooms of a type with an availability rule with closed = True are
        not available on the dates marked in the date field of the availability rule.
        --------------------
        Create an availability rule for double rooms with the field closed = true
        and the date from today until tomorrow. Then the availability is saved in a
        variable through the free_room_ids computed field, passing it the pricelist that
        it contains the availability plan where the rule is included, and the checkin
        and checkout dates are between the date of the rule. Then it is verified that
        the double rooms are not available.
        """
        self.test_room_type_availability_rule1 = self.env['pms.availability.plan.rule'].create({'availability_plan_id': self.test_room_type_availability1.id, 'room_type_id': self.test_room_type_double.id, 'date': (fields.datetime.today() + datetime.timedelta(days=2)).date(), 'closed': True, 'pms_property_id': self.pms_property3.id})
        pms_property = self.pms_property3.with_context(checkin=fields.date.today(), checkout=(fields.datetime.today() + datetime.timedelta(days=4)).date(), pricelist_id=self.pricelist2.id)
        result = pms_property.free_room_ids
        self.assertNotIn(self.test_room_type_double, result.mapped('room_type_id'), 'Availability should not contain rooms of a type which its availability rules applies')

    def test_availability_rules(self):
        """
        Check through subtests that the availability rules are applied
        for a specific room type.
        ----------------
        Test cases:
        1. closed_arrival = True
        2. closed_departure = True
        3. min_stay = 5
        4. max_stay = 2
        5. min_stay_arrival = 5
        6. max_stay_arrival = 3
        7. quota = 0
        8. max_avail = 0
        For each test case, it is verified through the free_room_ids compute field,
        that double rooms are not available since the rules are applied to this
        room type.
        """
        self.test_room_type_availability_rule1 = self.env['pms.availability.plan.rule'].create({'availability_plan_id': self.test_room_type_availability1.id, 'room_type_id': self.test_room_type_double.id, 'date': fields.date.today(), 'pms_property_id': self.pms_property3.id})
        checkin = fields.date.today()
        checkout = (fields.datetime.today() + datetime.timedelta(days=4)).date()
        test_cases = [{'closed': False, 'closed_arrival': True, 'closed_departure': False, 'min_stay': 0, 'max_stay': 0, 'min_stay_arrival': 0, 'max_stay_arrival': 0, 'quota': -1, 'max_avail': -1, 'date': checkin}, {'closed': False, 'closed_arrival': False, 'closed_departure': True, 'min_stay': 0, 'max_stay': 0, 'min_stay_arrival': 0, 'max_stay_arrival': 0, 'quota': -1, 'max_avail': -1, 'date': checkout}, {'closed': False, 'closed_arrival': False, 'closed_departure': False, 'min_stay': 5, 'max_stay': 0, 'min_stay_arrival': 0, 'max_stay_arrival': 0, 'quota': -1, 'max_avail': -1, 'date': checkin}, {'closed': False, 'closed_arrival': False, 'closed_departure': False, 'min_stay': 0, 'max_stay': 2, 'min_stay_arrival': 0, 'max_stay_arrival': 0, 'quota': -1, 'max_avail': -1, 'date': checkin}, {'closed': False, 'closed_arrival': False, 'closed_departure': False, 'min_stay': 0, 'max_stay': 0, 'min_stay_arrival': 5, 'max_stay_arrival': 0, 'quota': -1, 'max_avail': -1, 'date': checkin}, {'closed': False, 'closed_arrival': False, 'closed_departure': False, 'min_stay': 0, 'max_stay': 0, 'min_stay_arrival': 0, 'max_stay_arrival': 3, 'quota': -1, 'max_avail': -1, 'date': checkin}, {'closed': False, 'closed_arrival': False, 'closed_departure': False, 'min_stay': 0, 'max_stay': 0, 'min_stay_arrival': 0, 'max_stay_arrival': 0, 'quota': 0, 'max_avail': -1, 'date': checkin}, {'closed': False, 'closed_arrival': False, 'closed_departure': False, 'min_stay': 0, 'max_stay': 0, 'min_stay_arrival': 0, 'max_stay_arrival': 0, 'quota': -1, 'max_avail': 0, 'date': checkin}]
        for test_case in test_cases:
            with self.subTest(k=test_case):
                self.test_room_type_availability_rule1.write(test_case)
                pms_property = self.pms_property3.with_context(checkin=checkin, checkout=checkout, room_type_id=self.test_room_type_double.id, pricelist_id=self.pricelist2.id)
                result = pms_property.free_room_ids
                self.assertNotIn(self.test_room_type_double, result.mapped('room_type_id'), 'Availability should not contain rooms of a type which its availability rules applies')

    def test_rule_on_create_reservation(self):
        """
        Check that a reservation is not created when an availability rule prevents it .
        -------------------
        Create an availability rule for double rooms with the
        field closed = True and the date from today until tomorrow. Then try to create
        a reservation for that type of room with a checkin date today and a checkout
        date within 4 days. This should throw a ValidationError since the rule does
        not allow creating reservations for those dates.
        """
        self.test_room_type_availability_rule1 = self.env['pms.availability.plan.rule'].create({'availability_plan_id': self.test_room_type_availability1.id, 'room_type_id': self.test_room_type_double.id, 'date': (fields.datetime.today() + datetime.timedelta(days=2)).date(), 'closed': True, 'pms_property_id': self.pms_property3.id})
        checkin = datetime.datetime.now()
        checkout = datetime.datetime.now() + datetime.timedelta(days=4)
        with self.assertRaises(ValidationError, msg='Availability rules should be applied that would prevent the creation of the reservation.'):
            self.env['pms.reservation'].create({'pms_property_id': self.pms_property3.id, 'checkin': checkin, 'checkout': checkout, 'adults': 2, 'room_type_id': self.test_room_type_double.id, 'pricelist_id': self.pricelist2.id, 'partner_id': self.partner1.id})

    def test_rule_update_quota_on_create_reservation(self):
        """
        Check that the availability rule with quota = 1 for a room
        type does not allow you to create more reservations than 1
        for that room type.
        """
        self.test_room_type_availability_rule1 = self.env['pms.availability.plan.rule'].create({'availability_plan_id': self.test_room_type_availability1.id, 'room_type_id': self.test_room_type_double.id, 'date': datetime.date.today(), 'quota': 1, 'pms_property_id': self.pms_property3.id})
        self.pricelist2.pms_property_ids = [(4, self.pms_property1.id), (4, self.pms_property2.id), (4, self.pms_property3.id)]
        r1 = self.env['pms.reservation'].create({'pms_property_id': self.pms_property3.id, 'checkin': datetime.date.today(), 'checkout': datetime.date.today() + datetime.timedelta(days=1), 'adults': 2, 'room_type_id': self.test_room_type_double.id, 'pricelist_id': self.pricelist2.id, 'partner_id': self.partner1.id, 'sale_channel_origin_id': self.sale_channel_direct1.id})
        r1.flush()
        with self.assertRaises(ValidationError, msg='The quota shouldnt be enough to create a new reservation'):
            self.env['pms.reservation'].create({'pms_property_id': self.pms_property3.id, 'checkin': datetime.date.today(), 'checkout': datetime.date.today() + datetime.timedelta(days=1), 'adults': 2, 'room_type_id': self.test_room_type_double.id, 'pricelist_id': self.pricelist2.id, 'partner_id': self.partner1.id})