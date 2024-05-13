from django.test import TestCase
from dashboards.models import DashboardData
from entities.models import mmCompanies
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class DashboardDataTestCase(TestCase):
    def setUp(self):
        # Set up data here
        user = User.objects.create(username='testuser', password='testpass')
        company = mmCompanies.objects.create(name='Test Company')
        DashboardData.objects.create(user=user, payload={}, clean_payload={})

    def test_update_dashboard_data(self):
        # This is where you call your function
        update_dashboard_data()
        
        # Now check the results
        dashboard_data = DashboardData.objects.first()
        self.assertNotEqual(dashboard_data.clean_payload, {})  # Example condition

        # Add more assertions here to validate the state of the database or other side effects

