from django.conf.urls import patterns, include, url
from django.contrib import admin

from core.views import ActionView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ActionView.as_view(), name='actions')
    # Examples:
    # url(r'^$', 'expensor.views.home', name='home'),
    # url(r'^expensor/', include('expensor.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
