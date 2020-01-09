import os.path

from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib.auth.models import User, Group

import MonitoringSystem.django_cron
MonitoringSystem.django_cron.autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#admin.site.unregister(User)
#admin.site.unregister(Group)

urlpatterns = patterns('', (r'^jsi18n/$', 'MonitoringSystem.i18nDate.javascript_catalog', {'packages': 'django.conf'}), )

urlpatterns += patterns('', (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': os.path.join(os.path.realpath(os.path.dirname(__file__)), "media")}), )

urlpatterns += patterns('',
    # Examples:
    # url(r'^$', 'MonitoringSystem.views.home', name='home'),
    # url(r'^MonitoringSystem/', include('MonitoringSystem.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
    # This for login_required decorators check
    (r'^$', 'MonitoringSystem.common.ts_user.views.login'),
    (r'^login/$', 'MonitoringSystem.common.ts_user.views.login'),
    (r'^accounts/login/$', 'MonitoringSystem.common.ts_user.views.login'),
    (r'^projcodeupdate/$', 'MonitoringSystem.projectcode_migration.pojectcode_migration'),
    (r'^logs/', include('MonitoringSystem.common.logs.urls')),
    (r'^tsuser/', include('MonitoringSystem.common.ts_user.urls')),
    (r'^master/', include('MonitoringSystem.common.master.urls')),
    (r'^privilege/', include('MonitoringSystem.common.security.urls')),
    (r'^proposalabstract/', include('MonitoringSystem.OITS.proposal_abstract.urls')),
    (r'^oirequest/', include('MonitoringSystem.OITS.oi_request.urls')),
    (r'^oi/', include('MonitoringSystem.OITS.oi.urls')),
    (r'^projectbudget/', include('MonitoringSystem.OITS.project_budget.urls')),
    (r'^upload/', include('MonitoringSystem.common.upload.urls')),
    (r'^holiday/', include('MonitoringSystem.common.holiday.urls')),
    (r'^alert/', include('MonitoringSystem.common.alert.urls')),
    (r'^resourcerelease/', include('MonitoringSystem.RATS.resourcerelease.urls', namespace="resourcerelease")),
    (r'^longleave/', include('MonitoringSystem.RATS.longleave.urls', namespace="longleave")),
    (r'^onnotice/', include('MonitoringSystem.RATS.onnotice.urls', namespace="onnotice")),
    (r'^resource_allocation/', include('MonitoringSystem.RATS.resource_allocation.urls', namespace="resource_allocation")),
    (r'^skillmatrix/', include('MonitoringSystem.RATS.skill_matrix.urls', namespace="skillmatrix")),
    (r'^recruitment/', include('MonitoringSystem.RATS.recruitment.urls', namespace="recruitment")),
    (r'^resourcerequirement/', include('MonitoringSystem.RATS.resource_requirement.urls', namespace="resourcerequirement")),
    (r'^travel_information/', include('MonitoringSystem.RATS.travel_information.urls', namespace="travel_information")),
    (r'^stargroup/', include('MonitoringSystem.RATS.star_group.urls', namespace="stargroup")),
    (r'^profileupdation/', include('MonitoringSystem.RATS.profile_updation.urls', namespace="profileupdation")),
    (r'^bgclient/', include('MonitoringSystem.RATS.bg_client.urls', namespace="bgclient")),
    (r'^bgstandard/', include('MonitoringSystem.RATS.bgstandard.urls', namespace="bgstandard")),
    (r'^bgverification/', include('MonitoringSystem.RATS.bg_verification.urls', namespace="bgverification")),
    (r'^group_resource/', include('MonitoringSystem.RATS.group_resource.urls', namespace="group_resource")),
    (r'^myprofile/', include('MonitoringSystem.RATS.myprofile.urls', namespace="myprofile")),
    (r'^rap/', include('MonitoringSystem.RATS.rap.urls', namespace="rap")),
    (r'^resource_projection/', include('MonitoringSystem.RATS.resource_projection.urls', namespace="resource_projection")),
    (r'^seating_request/', include('MonitoringSystem.RATS.seating_request.urls', namespace="seating_request")),
    (r'^certification_tracker/', include('MonitoringSystem.RATS.certification_tracker.urls', namespace="certification_tracker")),

    (r'^user/$', direct_to_template, {"template": "user.html"}),
    (r'^bg_check_category/$', direct_to_template, {"template": "bg_check_category.html"}),
    (r'^bg_check_type/$', direct_to_template, {"template": "bg_check_type.html"}),
    (r'^bg_check_associate/$', direct_to_template, {"template": "bg_check_associate.html"}),
    (r'^group_summary/$', direct_to_template, {"template": "group_summary.html"}),

    (r'^common/$', direct_to_template, {"template": "common_list_n.html"}),
    (r'^group_resource_summary_list/$', direct_to_template, {"template": "group_resource_summary_list.html"}),
    (r'^user_list/$', direct_to_template, {"template": "user_list.html"}),
    
    (r'^reinstatement/', include('MonitoringSystem.common.reinstatement.urls', namespace="reinstatement")),
    (r'^insert/', include('MonitoringSystem.ERP.urls', namespace="insert_respool")),
    (r'^adr_erp/', include('MonitoringSystem.ADR_ERP.urls', namespace="adr_erp")),
    (r'^query_browser/', include('MonitoringSystem.query_browser.urls', namespace="query_browser")),
    (r'^timesheet/', include('MonitoringSystem.timesheet.urls', namespace="timesheet")),
    (r'^iis/', include('MonitoringSystem.RATS.input_invoice_sheet.urls', namespace="iis")),
    (r'^project_folder_tracker/', include('MonitoringSystem.seating_management.project_folder_tracker.urls', namespace="project_folder_tracker")),
    (r'^practice_folder/',include('MonitoringSystem.seating_management.practice_folder.urls',namespace="practice_folder")),
    (r'^seating_unit/',include('MonitoringSystem.seating_management.seating_unit.urls',namespace="seating_unit"))
)
