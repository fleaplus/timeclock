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
        event1 = EventFactory(user=employee)
        event2 = EventFactory(user=employee)

        self.assertEqual(Period.objects.count(), 1)
        period = Period.objects.last()
        self.assertEqual(period.user, employee)
        self.assertEqual(period.start, event1)
        self.assertEqual(period.end, event2)


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
