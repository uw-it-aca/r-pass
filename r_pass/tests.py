from django.test import TestCase
from r_pass.models import AccessToken, Service


class AccessTokenModelTest(TestCase):
    def test_save(self):
        pass


class ServiceModelTest(TestCase):
    def test_urls(self):
        service = Service(id=1, title="Test Service")
        self.assertEqual(service.view_url(), "/r-pass/service/test-service/1")
        self.assertEqual(service.edit_url(), "/r-pass/service/test-service/1/edit")
        self.assertEqual(str(service), "ID: 1, Title: Test Service")
