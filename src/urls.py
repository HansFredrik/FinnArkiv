from django.conf.urls.defaults import patterns, include
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^FinnPluss/', include('FinnPluss.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^make', 'web.views.make'),
    (r'^model', 'web.views.model'),
    (r'^classified', 'web.views.classified'),
    (r'^search', 'web.views.search'),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/Hansi/Documents/Development/Python/projects/FinnPluss/src/web/Templates/Resources'}),

    
    (r'^', 'web.views.index'),
)
