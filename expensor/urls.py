from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from core.views import ActionView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^auth/', include('django.contrib.auth.urls', namespace='auth',
                           app_name='auth')),
    url(r'_/', include('core.urls', namespace='core', app_name='core')),
    # Examples:
    # url(r'^$', 'expensor.views.home', name='home'),
    # url(r'^expensor/', include('expensor.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
