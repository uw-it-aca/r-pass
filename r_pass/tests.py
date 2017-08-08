from django.test import TestCase
from r_pass.models import AccessToken, Service


class AccessTokenModelTest(TestCase):
    def tearDown(self):
        AccessToken.objects.all().delete()
        Service.objects.all().delete()

    def test_save(self):
        service = Service(title="Test Service")
        service.save()

        token = AccessToken()
        token.name = "Test Token"
        token.user = "javerage"
        token.access_token = "00000000"
        token.service = service
        token.save()

        token = AccessToken.objects.get(name="Test Token")
        self.assertEqual(token.user, "javerage")
        self.assertEqual(token.access_token, "00000000")


class ServiceModelTest(TestCase):
    def test_urls(self):
        service = Service(id=1, title="Test Service")
        self.assertEqual(service.view_url(), "/r-pass/service/test-service/1")
        self.assertEqual(service.edit_url(),
                         "/r-pass/service/test-service/1/edit")
        self.assertEqual(str(service), "ID: 1, Title: Test Service")
