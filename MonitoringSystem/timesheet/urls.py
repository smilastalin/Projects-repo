from django.conf.urls.defaults import url, patterns

uuid_regex = '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'

urlpatterns = patterns('MonitoringSystem.timesheet.views',
    url(r'^create/$', 'create', name='create'),
    url(r'^edit/$', 'edit', name='edit'),
    url(r'^save/$', 'save', name='save'),
    url(r'^list/$', 'list', name='list'),
    url(r'^multi_approval/$', 'multi_approval', name='multi_approval'),
    url(r'^save_previous_duration/$', 'save_previous_duration',
        name='save_previous_duration'),
    )
