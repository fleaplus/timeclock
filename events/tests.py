from django.test import TestCase
from django.utils import timezone

from .factories import EventFactory
from .models import Event

class EventModelTestCase(TestCase):

	def test_can_store_time(self):
		now = timezone.now()
		event = EventFactory(time=now)

		self.assertEqual(Event.objects.first().time, now)
