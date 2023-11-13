from django.test import TestCase
from django.urls import reverse

from .models import *


# Create your tests here.

class TestRooms(TestCase):
    uri = reverse('rooms')

    def setUp(self):
        user = User.objects.create(name='John', email='john', password='john', phone='123456789', address='john',
                                   birthdate='2023-01-01')
        room = Room.objects.create(name='room', price=100, max_guests=1, type='d')
        Booking.objects.create(room_id=room, user_id=user, total_price=100, check_in='2024-01-01',
                               check_out='2024-01-03',
                               breakfast=False, lunch=False, extra_bed=False)

    def test_before_date(self):
        content = self.client.post(self.uri, {'data_inicial': '2023-12-30', 'data_final': '2023-12-31'})
        self.assertEqual(content.status_code, 200)
        self.assertEqual(content.context['double_room'], True)

    def test_before_limit(self):
        content = self.client.post(self.uri, {'data_inicial': '2023-12-30', 'data_final': '2024-01-01'})
        self.assertEqual(content.status_code, 200)
        self.assertEqual(content.context['double_room'], False)

    def test_checkout_overlap(self):
        content = self.client.post(self.uri, {'data_inicial': '2023-12-30', 'data_final': '2024-01-02'})
        self.assertEqual(content.status_code, 200)
        self.assertEqual(content.context['double_room'], False)

    def test_same_interval(self):
        content = self.client.post(self.uri, {'data_inicial': '2024-01-01', 'data_final': '2024-01-03'})
        self.assertEqual(content.status_code, 200)
        self.assertEqual(content.context['double_room'], False)

    def test_checkin_overalp(self):
        content = self.client.post(self.uri, {'data_inicial': '2024-01-02', 'data_final': '2024-01-04'})
        self.assertEqual(content.status_code, 200)
        self.assertEqual(content.context['double_room'], False)

    def test_after_limit(self):
        content = self.client.post(self.uri, {'data_inicial': '2024-01-03', 'data_final': '2024-01-04'})
        self.assertEqual(content.status_code, 200)
        self.assertEqual(content.context['double_room'], False)

    def test_after_date(self):
        content = self.client.post(self.uri, {'data_inicial': '2024-01-04', 'data_final': '2024-01-05'})
        self.assertEqual(content.status_code, 200)
        self.assertEqual(content.context['double_room'], True)

    def test_contains(self):
        content = self.client.post(self.uri, {'data_inicial': '2023-12-30', 'data_final': '2024-01-05'})
        self.assertEqual(content.status_code, 200)
        self.assertEqual(content.context['double_room'], False)
