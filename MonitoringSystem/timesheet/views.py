import sys
import random
import calendar
from django.conf import settings
from datetime import datetime, timedelta
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.core import serializers
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from dateutil.rrule import rrule, DAILY
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from MonitoringSystem.timesheet.models import Timesheet, TimesheetDetails, \
    ApproveTimesheetDetails
from MonitoringSystem.common.holiday.models import HolidayMaster, HolidayDetail
from MonitoringSystem.RATS.resource_allocation.models import \
    ResourceAllocationDetails, ResourceAllocationHistory, TaskAllocationDetails
from MonitoringSystem.common.master.models import GeneralTask, GroupTask
from MonitoringSystem.common.ts_user.models import Resources
from MonitoringSystem.common.alert.views import alert_engine_star

PERMISSION = {True: '1', False: '0'}


@login_required
def create(request, login_from=''):
    start_date, end_date, selected_date = _select_date_range(request)
    datelist = []
    image_choice = {'RS4': 'approved_image.png', 'RS18': 'rejected_image.png',
        'RS17': 'waiting_image.png', 'empty': 'empty_image.png',
        'RS1': 'empty_image.png'}
    '''
    Differenciate the timesheet user is a resource or reviewer.
    '''
    resource_designation = Resources.objects.filter(auth_user=request.user.id,
            is_active=1, designation__designation_type__in=['Domain', 'Testing'])
    print 'resource_designation', resource_designation
    if str(request.user.id) not in ['1', '2', '3', '4'] and \
            len(resource_designation) > 0:
        if request.GET.get('employee_id', '') != '':
            '''
            If the request has employee_id, then the timesheet user is an approver.
            '''
            resource = Resources.objects.get(
                id=request.GET.get('employee_id', ''))
        else:
            resource = Resources.objects.get(\
                id=request.user.resources_set.all()[0].id)
        '''
        Set timesheet entry permission, based on employee's previous day
        timesheet entry duration and the selected date is present or past dates
        not a future date.
        '''
        today = datetime.today().date()
        prev_days_duration = today - relativedelta(
            days=resource.timesheet_duration)
        for each_date in rrule(DAILY, dtstart=start_date, until=end_date):
            image = image_choice['empty']
            total_hrs = '00:00'
            timesheet = Timesheet.objects.select_related().filter(
                entry_date=each_date,
                is_active=1, resource=resource.id)
            '''
            Set save button, approve button and comments view  permissions.
            '''
            save_permission = PERMISSION[\
                (resource.auth_user.id == request.user.id) and\
                (each_date.date() <= today) and \
                (each_date.date() >= prev_days_duration)]
            approve_permission = PERMISSION[False]
            comments_view_permission = PERMISSION[False]
            if len(timesheet) > 0:
                timesheet = timesheet[0]
                if resource.auth_user.id == request.user.id:
                    save_permission = PERMISSION[save_permission and \
                        (timesheet.record_status_id not in ['RS4', 'RS17'])]
                    comments_view_permission = \
                        PERMISSION[timesheet.record_status_id == 'RS18']
                else:
                    comments_view_permission = PERMISSION[True]
                    approve_permission = \
                        PERMISSION[timesheet.record_status_id == 'RS17']
                '''
                Set date tab image  based on each date timesheet entries
                record status.
                '''
                image = image_choice[timesheet.record_status_id]
                if timesheet.record_status_id == 'RS4' and \
                        timesheet.reviewer.auth_user.id == request.user.id:
                    total_hrs = timesheet.approved_total_hrs.strftime('%H:%M')
                else:
                    total_hrs = timesheet.total_hrs.strftime('%H:%M')
            else:
                timesheet = ''

            datelist.append({
                'date': each_date,
                'timesheet': timesheet,
                'image': image,
                'save_permission': save_permission,
                'approve_permission': approve_permission,
                'total_hrs': total_hrs,
                'comments_view_permission': comments_view_permission,
                })
        page_data = {
                'datelist': datelist,
                'selected_date': selected_date,
                'task_list': _get_resource_task(request, start_date, end_date, \
                    selected_date),
                'resource': resource,
                'login_from': login_from,
                'effort_min_limit': settings.TIMESHEET_EFFORT_MIN_LIMIT,
                'effort_max_limit': settings.TIMESHEET_EFFORT_MAX_LIMIT}
    else:
        page_data = {'page_permission': '0'}
    return render_to_response('timesheet.html', {'page_data': page_data},
        context_instance=RequestContext(request))


def _select_date_range(request):
    today = datetime.now().date()
    '''
    Get datelist of selected week (sunday to monday).
    '''
    selected_week = request.GET.get('selected_week', '')
    if selected_week in ['nextweek', 'prevweek']:
        selected_start_date = datetime.strptime(\
            request.GET.get('current_start_date', ''),
            settings.APP_DATE_FORMAT)
        if selected_week == 'nextweek':
            start_date = selected_start_date + timedelta(days=7)
        else:
            start_date = selected_start_date + timedelta(days=-7)
        '''
        Set monday is a selected day for previous and next week navigation
        '''
        selected_date = start_date + timedelta(days=1)
    else:
        if request.GET.get('timesheet_id', '') != '':
            selected_date = Timesheet.objects.get(
                id=request.GET.get('timesheet_id', '')).entry_date
        elif request.GET.get('navigated_date', '') != '':
            selected_date = datetime.strptime(
                request.GET.get('navigated_date', ''), '%d-%b-%Y')
        else:
            selected_date = today
        '''
        If the selected day is sunday, set it as startdate of a week 
        or find the sundayday date of a selected week and set it as startdate.
        '''
        start_date = selected_date + timedelta(days=-(selected_date.weekday()\
            + 1)) if selected_date.weekday() != 6 else selected_date
    end_date = start_date + timedelta(days=6)
    return start_date, end_date, selected_date


def _get_timesheet_details(request, timesheet_id):
    timesheet = Timesheet.objects.select_related().filter(
        id=timesheet_id, is_active=1)
    timesheet_det = []
    if len(timesheet) > 0:
        if timesheet[0].reviewer.auth_user.id == request.user.id and\
                timesheet[0].record_status_id == 'RS4':
            '''
            If the user is an approver and the selected timesheet is
            already approved, then get the timesheet details from
            ApproveTimesheetDetails.
            '''
            timesheet_table = ApproveTimesheetDetails
        else:
            timesheet_table = TimesheetDetails
        timesheet_det = timesheet_table.objects.select_related().filter(
            timesheet=timesheet_id, is_active=1).order_by('sequence')
    return timesheet, timesheet_det


@login_required
def edit(request):
    selected_date = datetime.strptime(request.GET.get('selected_date'),
        settings.APP_DATE_FORMAT)
    timesheet_list = []
    timesheet = []
    timesheet_det = []
    if request.GET.get('timesheet_id', '') != '':
        timesheet, timesheet_det = _get_timesheet_details(\
            request, request.GET.get('timesheet_id', ''))
    if request.GET.get('edit_type', '') == 'multi_approval':
        '''
        Get timesheet details for approval list page popup
        '''
        total_hours = 0
        if len(timesheet) > 0:
            if timesheet[0].record_status_id == 'RS4':
                total_hours = timesheet[0].approved_total_hrs
            else:
                total_hours = timesheet[0].total_hrs
        return render_to_response('timesheet_details_popup.html', {
            'total_hours': total_hours, 'timesheet_det': timesheet_det},
            context_instance=RequestContext(request))
    for each in timesheet_det:
        '''
        Form the timesheet details dict based on task category.
        '''
        if each.task_category == 'project':
            timesheet_dict = {
                'task_id': each.project_task.id,
                'project_code': each.project_task.task_allocation.project.\
                    basebudgetdata.project_code,
                'project_name': each.project_task.task_allocation.project.\
                    basebudgetdata.oi.oirequestnumber.title_of_engagement,
                'phase_name': each.project_task.task.phase.name,
                'identifier': each.project_task.identifier.identifier_name \
                    if each.project_task.identifier else '',
                'task_code':  each.project_task.task.code,
                'task_name': each.project_task.task.name,
                }
        if each.task_category == 'group':
            timesheet_dict = {
                'task_id': each.group_task.id,
                'project_code': each.group_task.group.code,
                'project_name': each.group_task.group.name,
                'phase_name': '',
                'identifier': '',
                'task_code':  each.group_task.type.code,
                'task_name': each.group_task.name,
                }
        if each.task_category == 'general':
            timesheet_dict = {
                'task_id': each.general_task.id,
                'project_code': '',
                'project_name': '',
                'phase_name': '',
                'identifier': '',
                'task_code':  each.general_task.code,
                'task_name': each.general_task.name,
                }
        timesheet_dict.update({
            'task_categ': each.task_category,
            'effort': each.effort.strftime('%H:%M'),
            'task_completion': each.task_completion,
            'id': each.id})
        timesheet_list.append(timesheet_dict)

    '''
    Set Holiday warning flag.
    '''
    holiday_flag = PERMISSION[False]
    weekend = False
    holiday = False
    if len(timesheet) > 0:
        currentlocation = timesheet[0].resource.current_location_id
###    elif
    else:
        currentlocation = request.user.resources_set.all()[0].\
            current_location_id
    if currentlocation:
        '''
        Check the selected date is an week end.
        '''
        weekend = HolidayMaster.objects.select_related().filter(
            regiondata=currentlocation,
            is_active=1, is_locked=0)
        if len(weekend) > 0:
            weekend = str(selected_date.weekday() + 1) in \
                weekend[0].weekend.split(',')
        '''
        Check the selected date is an holiday.
        '''
        holiday = len(HolidayDetail.objects.select_related().filter(\
            holiday__regiondata=currentlocation,
            holiday__is_active=1, holiday__is_locked=0,
            holi_date=selected_date)) > 0
    if holiday or weekend:
        holiday_flag = PERMISSION[True]
    result = [{'holiday_flag': holiday_flag, 'timesheet_list': timesheet_list}]
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/javascript')


def _get_resource_task(request, start_date, end_date, selected_date):
    task_list = {}
    project_task = []
    '''
    Current project tasks.
    '''
    res_alloc_det = ResourceAllocationDetails.objects.select_related().filter(\
        employee=request.user.resources_set.all()[0].id,
        is_in_active=False, is_invalid_entry=False)
    if len(res_alloc_det) > 0:
        '''
        Filter resource tasks based on resource allocation role.
        '''
        if res_alloc_det[0].allocate_type == 'BUDGET':
            '''
            Filter resource tasks based on project phase, for budgeted
            resources only.
            '''            
            project_task_details = TaskAllocationDetails.objects.select_related(\
                ).filter(
                task_allocation__project=res_alloc_det[0].resource_allocation.\
                project.id,
                role=res_alloc_det[0].role.id, is_completed=0, is_active=1,
                is_lock=0, task__phase=res_alloc_det[0].phase_detail.\
                projecbudgetphaseeffort.phase.id)
        elif res_alloc_det[0].allocate_type == 'ADDITIONAL':
            '''
            If the resource,  additionaly allocated in resource allocation
            and in task allocation, no task allocated to the resource's role,
            then filter all the tasks of that project to the resource.
            '''
            project_task_details = TaskAllocationDetails.objects.\
                select_related().filter(
                task_allocation__project=res_alloc_det[0].resource_allocation.\
                project.id, is_completed=0, is_active=1, is_lock=0)
        for each_task in project_task_details:
            project_task.append(each_task)
    '''
    Get the resource task from resource allocation history based on the
    selected week start and end date.
    '''
    res_alloc_history = ResourceAllocationHistory.objects.select_related().\
        filter(employee=request.user.resources_set.all()[0].id,
        allocation_date__lte=end_date, release_date__gte=start_date,
        is_invalid_entry=False).exclude(detail=None)
    if len(res_alloc_history) > 0:
        if res_alloc_history[0].allocate_type == 'BUDGET':
            history_project_task = TaskAllocationDetails.objects.select_related().\
                filter(task_allocation__project=res_alloc_history[0].project.id,
                role=res_alloc_history[0].role.id, is_completed=0, is_active=1,
                is_lock=0, task__phase=res_alloc_history[0].detail.phase_detail.\
                projecbudgetphaseeffort.phase.id)
        elif res_alloc_history[0].allocate_type == 'ADDITIONAL':
            project_task_details = TaskAllocationDetails.objects.\
                select_related().filter(
                task_allocation__project=res_alloc_history[0].project.id,
                is_completed=0, is_active=1, is_lock=0)
        for each_task in history_project_task:
            project_task.append(each_task)

    general_task = GeneralTask.objects.select_related().filter(is_active=1)
    resource = Resources.objects.select_related().filter(is_active=1,
        auth_user=request.user.id).exclude(star_group=None)
    user_group = resource[0].star_group.id if len(resource) > 0 else []
    group_task = GroupTask.objects.select_related().filter(is_active=1,
        group=user_group) if len(resource) > 0 else []
    task_list = {'project_task': project_task,
        'group_task': group_task,
        'general_task': general_task}
    return task_list


@login_required
def multi_approval(request):
    selected_ids = request.GET.get('selected_id', '').split(',')
    timesheet_list = Timesheet.objects.select_related().filter(\
        id__in=selected_ids)
    for timesheet in timesheet_list:
        timesheet.record_status_id = 'RS4'
        timesheet.approved_on = datetime.today().strftime(\
            settings.DB_DATE_FORMAT)
        timesheet.modified_by_id = request.user.id
        timesheet.approved_total_hrs = timesheet.total_hrs
        timesheet.save()
        '''
        Get timesheet details dict from timsaheet details table
        and save the dict in approved timesheet details.
        '''
        timesheet_det_dict = TimesheetDetails.objects.select_related().filter(\
            timesheet=timesheet.id, is_active=1).values('timesheet_id',
            'task_category',
            'project_task_id', 'group_task_id',
            'general_task_id', 'effort', 'task_completion', 'sequence')
        for each_det in timesheet_det_dict:
            ApproveTimesheetDetails(**each_det).save()
    return HttpResponseRedirect('/timesheet/list/')


@login_required
def save(request):
    selected_date = request.POST.get('selected_date', '')
    timesheet = Timesheet.objects.select_related().filter(\
        id=request.POST.get('timesheet_id' + selected_date, ''))
    record_status = request.POST.get('record_status', '')
    timesheet_dict = {
        'id': request.POST.get('timesheet_id' + selected_date, ''),
        'entry_date': datetime.strptime(selected_date,\
            settings.APP_DATE_FORMAT),
        'record_status_id': record_status,
        'comments': request.POST.get('comments' + selected_date, ''),
        'modified_by_id': request.user.id,
        }
    if len(timesheet) == 0:
        timesheet_dict.update({
            'resource_id': request.user.resources_set.all()[0].id,
            'reviewer_id': request.user.resources_set.all()[0].\
                reporting_manager.resources_set.all()[0].id,
            'created_by_id': request.user.id,
            'created_on': datetime.today().strftime(settings.DB_DATE_FORMAT),
            'holiday': int(request.POST.get('holiday' + selected_date, '0')),
            })
    else:
        timesheet_dict.update({
            'resource_id': timesheet[0].resource.id,
            'reviewer_id': timesheet[0].reviewer.id,
            'created_by_id': timesheet[0].created_by.id,
            'created_on': timesheet[0].created_on,
            'holiday': timesheet[0].holiday,
            })
    if record_status == 'RS4':
        timesheet_dict.update({
            'approved_total_hrs': \
                request.POST.get('tot_hrs' + selected_date, '0.0'),
            'total_hrs': timesheet[0].total_hrs if len(timesheet) > 0 \
                else '0.0',
            'approved_on': datetime.today().strftime(settings.DB_DATE_FORMAT),
            })
        '''
        If the user is an approver then save the timesheet details in
        ApproveTimesheetDetails
        '''
        timesheet_table = ApproveTimesheetDetails
    else:
        timesheet_dict.update({
            'total_hrs': request.POST.get('tot_hrs' + selected_date, '0.0')})
        timesheet_table = TimesheetDetails
    if request.POST.get('leave' + selected_date, '') == 'on':
        timesheet_dict.update({'on_leave': True})
    timesheet = Timesheet(**timesheet_dict)
    timesheet.save()
    if request.POST.get('leave' + selected_date, '') != 'on':
        effort_len = request.POST.get('effort_table_len' + selected_date, '')
        '''
        Delete the timesheet details.
        '''
        delete_timesheet = request.POST.get("delete_timesheet" +\
            selected_date).split(',')
        delete_objects = timesheet_table.objects.select_related().filter(\
            id__in=delete_timesheet, timesheet=timesheet)
        delete_objects.update(is_active=0)
        sequence = 1
        for each in range(1, int(effort_len) if effort_len != '' else 0):
            row_name = selected_date + str(each)
            task_category = request.POST.get('task_cat' + row_name, '')
            if task_category == '' or task_category == None:
                continue
            timesheet_dict = {
                'id': request.POST.get('timesheet_det_id' + row_name, ''),
                'timesheet_id': timesheet.id,
                'task_category': task_category,
                'effort': request.POST.get('effort_time' + row_name, ''),
                'task_completion': request.POST.get('task_completion' + \
                    row_name, ''),
                'sequence': sequence,
                task_category + '_task_id': request.POST.get('task_id' +\
                    row_name, '')}
            timesheet_table(** timesheet_dict).save()
    if record_status == 'RS18':
        alert_engine_star(request, 'alertconfig62', timesheet.id,
                timesheet.resource.star_group.id if timesheet.resource.star_group else '', '')
    return HttpResponseRedirect('/timesheet/create/?timesheet_id=' +\
        str(timesheet.id) + '&employee_id=' + \
            request.GET.get('employee_id', ''))


@login_required
def list(request):
    resource_designation = Resources.objects.filter(auth_user=request.user.id,
            is_active=1, designation__designation_type__in=['Domain', 'Testing'])
    if str(request.user.id) not in ['1', '2', '3', '4'] and \
            len(resource_designation) > 0:
        start_date, end_date, selected_date = _select_date_range(request)
        datelist = []
        emp_details = []
        approval_color = {'RS4': 'accept', 'RS18': 'reject',
                    'RS17': 'waiting_approval',
                    'RS1': 'save', 'empty': 'empty'}
        for each_date in rrule(DAILY, dtstart=start_date, until=end_date):
            datelist.append({'date': each_date})
        '''
        Get all resources, who are having login user as reporting manager.
        '''
        resources = Resources.objects.select_related().filter(\
            reporting_manager=request.user.id, is_active=1)
        for each_res in resources:
            resource_timesheet_dict = []
            timesheet_dict = {}
            '''
            Get each employee's submitted(send for approval) timesheet details
            '''
            timesheet = Timesheet.objects.select_related().filter(\
                resource=each_res.id).values_list('entry_date', 'id',
                'total_hrs', 'record_status')
            if len(timesheet) > 0:
                for record in timesheet:
                    timesheet_dict.update({record[0]: [record[1], record[2],
                        record[3]]})
            for each_date in rrule(DAILY, dtstart=start_date, until=end_date):
                timesheet_entry = timesheet_dict.get(each_date.date(), 'empty')
                if timesheet_entry != 'empty':
                    timesheet_id = timesheet_entry[0]
                    total_hrs = timesheet_entry[1]
                    record_status = timesheet_entry[2]
                else:
                    timesheet_id = ''
                    total_hrs = None
                    record_status = 'empty'
                resource_timesheet_dict.append({
                    'total_hrs': total_hrs,
                    'color': approval_color[record_status],
                    'timesheet_id': timesheet_id,
                    'entry_date': each_date})
            emp_details.append({
                            'employee': each_res,
                            'resource_timesheet_dict': resource_timesheet_dict})
        page_data = {'datelist': datelist, 'emp_details': emp_details,
            'view_permission': '1', 'duration_range' : range(0,201) }
    else:
        page_data = {'view_permission': '0'}
    return render_to_response('timesheet_approval.html',
        {'page_data': page_data},
        context_instance=RequestContext(request))


def save_previous_duration(request):
    '''
    save previous date timesheet entry duration.
    '''
    employee_len = request.POST.get('employee_len', '')
    for each_emp in range(1, int(employee_len) + 1):
        Resources.objects.filter(id=request.POST.get('emp_id' + \
            str(each_emp), '')).update(
            timesheet_duration=request.POST.get('previous_duration' +\
            str(each_emp), ''))
    messages.success(request, 'Timesheet-Days configurations saved successfully')
    return HttpResponseRedirect('/timesheet/list')
