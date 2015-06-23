from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils import formats

from .factories import EventFactory, PeriodFactory
from .models import Event, Period

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


class PeriodModelTestCase(TestCase):

    def test_create(self):
        employee = EmployeeFactory()
        event1 = Event.objects.create(user=employee, time=timezone.now())
        event2 = Event.objects.create(user=employee, time=timezone.now())

        self.assertEqual(Period.objects.count(), 1)
        period = Period.objects.last()
        self.assertEqual(period.user, employee)
        self.assertEqual(period.start, event1)
        self.assertEqual(period.end, event2)

    def test_can_be_completed(self):
        PeriodFactory(completed=True)

        self.assertTrue(Period.objects.last().completed)

    def test_event_occurred_start(self):
        employee = EmployeeFactory()
        event = EventFactory(user=employee)

        Period.objects.event_occurred(event)

        period = Period.objects.last()

        self.assertEqual(period.start, event)
        self.assertEqual(period.end, None)

    def test_event_occurred_end(self):
        employee = EmployeeFactory()
        event_start = EventFactory(user=employee)
        event_end = EventFactory(user=employee)
        PeriodFactory(user=employee, start=event_start, end=None, completed=False)

        Period.objects.event_occurred(event_end)

        period = Period.objects.last()

        self.assertEqual(period.end, event_end)
        self.assertTrue(period.completed)

    def test_duration_for_completed_period(self):
        employee = EmployeeFactory()
        event_start = EventFactory(user=employee, time=timezone.now() - timedelta(hours=1))
        event_end = EventFactory(user=employee, time=timezone.now())

        period = PeriodFactory(user=employee, start=event_start, end=event_end)

        self.assertAlmostEqual(period.duration.total_seconds(), 3600, places=0)

    def test_duration_for_incomplete_period(self):
        employee = EmployeeFactory()
        event_start = EventFactory(user=employee, time=timezone.now() - timedelta(hours=1))

        period = PeriodFactory(user=employee, start=event_start, end=None, completed=False)

        self.assertAlmostEqual(period.duration.total_seconds(), 3600, places=0)

class EventCreateViewTestCase(TestCase):

    def setUp(self):
        self.employee = EmployeeFactory()
        self.client.login(username=self.employee.email, password='password')

    def test_get(self):
        r = self.client.get('/events/new/')

        self.assertEqual(r.status_code, 200)

    def test_get_sets_default_time(self):
        r = self.client.get('/events/new/')

        self.assertEqual(r.context['form']['time'].value(), timezone.now().replace(second=0, microsecond=0))

    def test_post(self):
        r = self.client.post('/events/new/', {'time_0': '2015-01-01', 'time_1': '01:01:01'})

        self.assertEqual(r.status_code, 302)
        self.assertEqual(Event.objects.count(), 1)

    def test_get_requires_user_to_be_logged_in(self):
        self.client.logout()

        r = self.client.get('/events/new/')

        self.assertRedirects(r, '/accounts/login/?next=/events/new/', fetch_redirect_response=False)

    def test_post_sets_user_to_current_user(self):
        r = self.client.post('/events/new/', {'time_0': '2015-01-01', 'time_1': '01:01:01'})

        self.assertEqual(Event.objects.last().user, self.employee)


class PeriodListViewTestCase(TestCase):

    def setUp(self):
        self.employee = EmployeeFactory()
        self.client.login(username=self.employee.email, password='password')

    def test_get(self):
        period = PeriodFactory(user=self.employee)

        r = self.client.get(reverse('periods_index'))

        self.assertEqual(r.status_code, 200)
        formatted_time = formats.date_format(timezone.localtime(period.start.time), "DATETIME_FORMAT")
        self.assertContains(r, formatted_time)
        self.assertContains(r, "1.00")
