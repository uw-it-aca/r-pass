from django.conf.urls import url
from r_pass.views import home, service, create, edit


urlpatterns = [
    url(r'', home),
    url(r'^service/.*/(?P<service_id>[0-9]+)/edit/?$', edit),
    url(r'^service/.*/(?P<service_id>[0-9]+)/?$', service),
    url(r'^create/?$', create),
]
