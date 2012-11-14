from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^service/.*/(?P<service_id>[0-9]+)$', 'r_pass.views.service'),
    url(r'', 'r_pass.views.home'),
)
