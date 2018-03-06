from django.test import TestCase
from django.test import modify_settings
from django.test import override_settings

from django.conf import settings
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site


OLD_PATH = '/a/'
NEW_PATH = '/b/?x=specified'

REQUESTS = dict(
    no_params=OLD_PATH,
    x_only=OLD_PATH + '?x=requested',
    y_only=OLD_PATH + '?y=requested',
    x_and_y=OLD_PATH + '?x=requested&y=requested'
)


@modify_settings(MIDDLEWARE={'append': 'django_marketing_redirects.middleware.RedirectFallbackMiddleware'})
@override_settings(APPEND_SLASH=False, ROOT_URLCONF='tests.urls', SITE_ID=1)
class RedirectRemoveQueryParamsTest(TestCase):

    def setUp(self):
        self.site = Site.objects.get(pk=settings.SITE_ID)
        self.redirect = Redirect.objects.create(site=self.site, old_path=OLD_PATH, new_path=NEW_PATH)

    def test_no_params(self):
        response = self.client.get(REQUESTS['no_params'])
        self.assertRedirects(response, NEW_PATH, status_code=301, target_status_code=404)
