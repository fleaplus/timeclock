from django.test import TestCase
from django.utils import timezone

from .factories import EventFactory
from .models import Event

from accounts.factories import EmployeeFactory


class EventModelTestCase(TestCase):

    def test_can_store_time(self):
        now = timezone.now()
        event = EventFactory(time=now)

        self.assertEqual(Event.objects.first().time, now)

    def test_can_store_employee(self):
        employee = EmployeeFactory()
        event = EventFactory(user=employee)

        self.assertEqual(Event.objects.first().user, employee)

class EventCreateViewTestCase(TestCase):

    def test_new_event_view(self):
        employee = EmployeeFactory()

        self.client.login(username=employee.email, password='password')
        r = self.client.get('/events/new/')

        self.assertEqual(r.status_code, 200)
