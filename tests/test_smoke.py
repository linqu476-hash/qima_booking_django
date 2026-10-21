from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.bookings.models import BookingRun
class DashboardSmokeTests(TestCase):
 def setUp(self): self.user=get_user_model().objects.create_user(username='tester',password='test-password-123')
 def test_dashboard_requires_login(self):
  response=self.client.get(reverse('dashboard'))
  self.assertEqual(response.status_code,302)
 def test_dashboard_after_login(self):
  self.client.login(username='tester',password='test-password-123')
  response=self.client.get(reverse('dashboard'))
  self.assertEqual(response.status_code,200)
 def test_user_sees_own_runs(self):
  self.client.login(username='tester',password='test-password-123')
  BookingRun.objects.create(user=self.user,status='queued')
  self.assertContains(self.client.get(reverse('dashboard')),'Queued')
