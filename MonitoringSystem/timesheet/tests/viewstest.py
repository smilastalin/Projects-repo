import ast

from django.test import TestCase
from django.test.client import Client as base_client
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from MonitoringSystem.common.ts_user.tests.viewstest import LoginTest
from MonitoringSystem.common.master.models import GeneralTask, GroupTask, \
    ProjectPhase, Role, City, ServiceTask, TaskType, ServiceType
from MonitoringSystem.RATS.star_group.models import StarGroup
from MonitoringSystem.common.ts_user.models import Resources
from MonitoringSystem.timesheet.models import Timesheet, TimesheetDetails,\
    ApproveTimesheetDetails
from MonitoringSystem.RATS.resource_allocation.tests.viewstest import \
    _common_save
from MonitoringSystem.RATS.resource_allocation.models import \
    ResourceAllocation, ResourceAllocationDetails, ResourceAllocationHistory,\
    TaskAllocation, TaskAllocationDetails
from MonitoringSystem.OITS.project_budget.models import ProjectBudget, \
    ProjectBudgetPhaseEffort, ProjectBudgetRoleDetails


def _create_PM_masters(user_id):
    task_type = TaskType.objects.create(name='testcasetasktype', code='001',
        is_active=1)
    general_id = GeneralTask.objects.create(name='Meeting', code='001',
        description='general task testing').id
    user_group = Resources.objects.filter(auth_user=user_id)[0]
    group_id = GroupTask.objects.create(name='Meeting',
        group_id=user_group.star_group_id,
        description='general task testing', type=task_type).id
    return general_id, group_id


def _add_task_alloc_etails(user_id, alloc_table='', alloc_type=''):
    user_group = Resources.objects.filter(auth_user=user_id)[0]
    pjt_bud = ProjectBudget.objects.all()[0]
    role = Role.objects.all()[0]
    city = City.objects.all()[0]
    pjt_phase = ProjectPhase.objects.create(code='001',
        name='testcase projectphase', is_active='1')
    today = datetime.today()
    phase_effort = ProjectBudgetPhaseEffort.objects.create(
        projectbudget_id=pjt_bud, phase=pjt_phase,
        phase_start_date=today,
        phase_end_date=today + timedelta(days=50))
    phase_role_det = ProjectBudgetRoleDetails.objects.create(
        projecbudgetphaseeffort=phase_effort, effort_type='Role',
        role=role, count=2, start_date=today,
        end_date=today + timedelta(days=50))
    res_alloc = ResourceAllocation.objects.create(project=pjt_bud,
        is_active=1, is_locked=0, record_status_id='RS4')
    role2 = Role.objects.create(code='002', name='CMG Team',
        role_type='Project')
    if alloc_type == 'BUDGET':
        allocate_type = 'BUDGET'
        role_id = role
        phase_detail = phase_role_det
    elif alloc_type == 'ADDITIONAL':
        allocate_type = 'ADDITIONAL'
        role_id = role
        phase_detail = None
    elif alloc_type == 'ADDITIONAL_alltask':
        allocate_type = 'ADDITIONAL'
        role_id = role2
        phase_detail = None
    res_alloc_det = ResourceAllocationDetails.objects.create(
        resource_allocation=res_alloc, allocate_type=allocate_type,
            role=role_id,
            phase_detail=phase_detail, city=city, employee=user_group,
            allocation_date=today + timedelta(days=-20),
            release_date=today + timedelta(days=20), allocation_pds=40,
            is_in_active=False, is_invalid_entry=False)

    if alloc_table == 'history':
        res_alloc_det = ResourceAllocationHistory.objects.create(
            project=pjt_bud, allocate_type=allocate_type,
            detail=res_alloc_det, role=role_id, city=city,
            employee=user_group, allocation_date=today + timedelta(days=-20),
            release_date=today + timedelta(days=-1),
            allocation_pds=40, is_back_dated_entry=True,
            is_invalid_entry=False)
    '''
    Task Allocation
    '''
    task_type = TaskType.objects.all()[0]
    service = ServiceType.objects.create(short_name='testcaseservice',
        code='001', is_active=1)
    service_task = ServiceTask.objects.create(service=service,
        phase=pjt_phase, name='servicetask testcase', code='001',
        task_type=task_type, is_active=1)
    task_alloc = TaskAllocation.objects.create(project=pjt_bud, is_lock=0)
    TaskAllocationDetails.objects.create(task_allocation=task_alloc,
        task=service_task, role=role, effort_days=40, is_completed=0,
        is_active=1)
    if alloc_type == 'ADDITIONAL_alltask':
        service_task2 = ServiceTask.objects.create(service=service,
            phase=pjt_phase, name='all_servicetask for additional resource',
            code='001', task_type=task_type, is_active=1)
        TaskAllocationDetails.objects.create(task_allocation=task_alloc,
            task=service_task2, role=role, effort_days=40, is_completed=0,
            is_active=1)


class TimesheetTest(TestCase):
    client = base_client()

    def setUp(self):
        self.client = LoginTest('testlogin').testlogin()
        _common_save(self)
        self.general, self.group = _create_PM_masters(
            self.client.session.items()[0][1])
        self.image_choice = {'RS4': 'approved_image.png',
            'RS18': 'rejected_image.png',
            'RS17': 'waiting_image.png', 'empty': 'empty_image.png',
            'RS1': 'empty_image.png'}
        self.today = datetime.now().date()
        self.start_date = self.today + timedelta(days=-(self.today.weekday() \
            + 1))
        timesheet_duration = Resources.objects.get(
            auth_user=self.client.session.items()[0][1]).timesheet_duration
        self.res_timesheet_duration = self.today + timedelta(
            days=-timesheet_duration)

    def _test_permissions(self, timesheet_dict):
        '''
        test resources save, approve and comments view permission.
        '''
        for each in timesheet_dict:
            '''
            Test each date save permissions.
            '''
            if (each['date'].date() <= self.today) and \
                    (each['date'].date() >= self.res_timesheet_duration):
                if each['timesheet'] != '':
                    if each['timesheet'].record_status_id in  ['RS4', 'RS17']:
                        self.assertEquals(each['save_permission'], '0')
                    else:
                        self.assertEquals(each['save_permission'], '1')
                    '''
                    test comments_view_permission
                    '''
                    if each['timesheet'].record_status_id == 'RS18':
                        self.assertEquals(each['comments_view_permission'],
                            '1')
                    else:
                        self.assertEquals(each['comments_view_permission'],
                            '0')
                else:
                    self.assertEquals(each['save_permission'], '1')
                    self.assertEquals(each['comments_view_permission'], '0')
            else:
                self.assertEquals(each['save_permission'], '0')
                self.assertEquals(each['comments_view_permission'], '0')
            '''
            Test tab image based on record status.
            '''
            if each['timesheet'] != '':
                self.assertEquals(each['image'],
                    self.image_choice[each['timesheet'].record_status_id])
            else:
                self.assertEquals(each['image'], 'empty_image.png')
            '''
            test approve_permission
            '''
            self.assertEquals(each['approve_permission'], '0')

    def test_create(self):
        response = self.client.post('/timesheet/create/', {})
        '''
        Test task list from Group, General, and project
        '''
        self.assertEquals(
            len(response.context['page_data']['task_list']['project_task']), 0)
        self.assertEquals(
            len(response.context['page_data']['task_list']['group_task']), 1)
        self.assertEquals(
            len(response.context['page_data']['task_list']['general_task']), 1)
        self._test_permissions(response.context['page_data']['datelist'])
        '''
        test week duration and week start and end date
        '''
        self.assertEquals(len(response.context['page_data']['datelist']), 7)
        self.assertEquals(
            response.context['page_data']['datelist'][0]['date'].date(),
            self.start_date)
        self.assertEquals(
            response.context['page_data']['datelist'][6]['date'].date(),
            self.start_date + timedelta(days=6))
        self.assertEquals(
            response.context['page_data']['selected_date'], self.today)
        '''
        Test the login user is an resource.
        '''
        self.assertEquals(self.client.session.items()[0][1],
            response.context['page_data']['resource'].auth_user.id)

        self.assertEquals(response.status_code, 200)

    def test_budget_service_task(self):
        '''
        Allocate login user as Budget resource to a role in resource
        allocation and allocate a task to that role, project service
        and phase and test project task count.
        '''
        _add_task_alloc_etails(self.client.session.items()[0][1],
            'details', 'BUDGET')
        response = self.client.post('/timesheet/create/', {})
        self.assertEquals(
            len(response.context['page_data']['task_list']['project_task']), 1)

    def test_additional_res_rolewise_service_task(self):
        '''
        Allocate login user as Additioanl resource to a role in resource
        allocation without phase details and  allocate a task to that role,
        project service and phase and test project task count.
        '''
        _add_task_alloc_etails(
            self.client.session.items()[0][1], 'details', 'ADDITIONAL')
        response = self.client.post('/timesheet/create/', {})
        self.assertEquals(
            len(response.context['page_data']['task_list']['project_task']), 1)

    def test_additional_res_all_service_task(self):
        '''
        Allocate login user as Additioanl resource to a role in resource
        allocation without phase details and  allocate a task in different
        role, project service and phase and test project task count.
        '''
        _add_task_alloc_etails(
            self.client.session.items()[0][1], 'details', 'ADDITIONAL_alltask')
        response = self.client.post('/timesheet/create/', {})
        self.assertEquals(
            len(response.context['page_data']['task_list']['project_task']), 2)

    def test_history_budget_service_task(self):
        '''
        Allocate login user as Budget resource to a role in resource
        allocation history  and allocate a task to that role, project service
        and phase and test project task count.
        '''
        _add_task_alloc_etails(self.client.session.items()[0][1],
            'history', 'BUDGET')
        response = self.client.post('/timesheet/create/', {})
        self.assertEquals(
            len(response.context['page_data']['task_list']['project_task']), 2)

    def test_history_additional_res_rolewise_service_task(self):
        '''
        Allocate login user as Additioanl resource to a role in resource
        allocation history  without phase details and  allocate a task to that
        role, project service and phase and test project task count.
        '''
        _add_task_alloc_etails(self.client.session.items()[0][1],
            'history', 'ADDITIONAL')
        response = self.client.post('/timesheet/create/', {})
        self.assertEquals(
            len(response.context['page_data']['task_list']['project_task']), 2)

    def test_history_additional_res_all_service_task(self):
        '''
        Allocate login user as Additioanl resource to a role in resource
        allocation history without phase details and  allocate a task in
        different role, project service and phase and test project task count.
        '''
        _add_task_alloc_etails(self.client.session.items()[0][1], 'history',
            'ADDITIONAL_alltask')
        response = self.client.post('/timesheet/create/', {})
        self.assertEquals(
            len(response.context['page_data']['task_list']['project_task']), 2)

    def test_next_week_navigation(self):
        '''
        Test start and end date of week navigation for next week.
        '''
        response = self.client.post(
            '/timesheet/create/?selected_week=nextweek&current_start_date=' \
            + self.start_date.strftime('%d-%b-%Y'), {})
        start_date = self.start_date + timedelta(days=7)
        self.assertEquals(
            response.context['page_data']['datelist'][0]['date'].date(),
            start_date)
        self.assertEquals(
            response.context['page_data']['datelist'][6]['date'].date(),
            start_date + timedelta(days=6))
        self.assertEquals(
            response.context['page_data']['selected_date'].date(),
            start_date + timedelta(days=1))
        self.assertEquals(response.status_code, 200)

    def test_prev_week_navigation(self):
        '''
        Test start and end date of week navigation for previous week.
        '''
        response = self.client.post(
            '/timesheet/create/?selected_week=prevweek&current_start_date='\
            + self.start_date.strftime('%d-%b-%Y'), {})
        start_date = self.start_date + timedelta(days=-7)
        self.assertEquals(
            response.context['page_data']['datelist'][0]['date'].date(),
            start_date)
        self.assertEquals(
            response.context['page_data']['datelist'][6]['date'].date(),
            start_date + timedelta(days=6))
        self.assertEquals(
            response.context['page_data']['selected_date'].date(),
            start_date + timedelta(days=1))
        self.assertEquals(response.status_code, 200)

    def _save_timesheet(self):
        selected_date = self.today.strftime('%d-%b-%Y')
        response = self.client.post('/timesheet/save/', {
            'selected_date': selected_date,
            'effort_time' + selected_date + '1': '02:05',
            'effort_time' + selected_date + '2': '03:15',
            'effort_time' + selected_date + '3': '01:45',
            'effort_table_len' + selected_date: '4',
            'task_cat' + selected_date + '1': 'group',
            'task_cat' + selected_date + '2': 'group',
            'task_cat' + selected_date + '3': 'general',
            'task_id' + selected_date + '1': self.group,
            'task_id' + selected_date + '2': self.group,
            'task_id' + selected_date + '3': self.general,
            'record_status': 'RS1',
            'tot_hrs' + selected_date: '07:05',
            'delete_timesheet' + selected_date: '',
            })
        return response

    def test_save(self):
        response = self._save_timesheet()
        self.assertEquals(len(Timesheet.objects.all()), 1)
        self.assertEquals(len(TimesheetDetails.objects.all()), 3)
        self.assertEquals(len(ApproveTimesheetDetails.objects.all()), 0)
        self.assertEquals(response.status_code, 302)

    def test_edit_timesheet_details(self):
        self._save_timesheet()
        timesheet_id = Timesheet.objects.all()[0].id
        response = self.client.get('/timesheet/edit/', {
            'timesheet_id': timesheet_id,
            'selected_date': self.today.strftime('%d-%b-%Y')})
        result = ast.literal_eval(response.content)
        self.assertEquals(result[0]['holiday_flag'], '0')
        self.assertEquals(len(result[0]['timesheet_list']), 3)
        self.assertEquals(response.status_code, 200)

    def test_multi_approval_edit(self):
        self._save_timesheet()
        timesheet = Timesheet.objects.all()[0]
        response = self.client.get('/timesheet/edit/', {
            'timesheet_id': timesheet.id,
            'selected_date': self.today.strftime('%d-%b-%Y'),
            'edit_type': 'multi_approval'})
        self.assertEquals(len(response.context['timesheet_det']), 3)
        '''
        check timesheet total hrs with approved_total_hrs and check
        timesheet details table name
        '''
        self.assertEquals(response.context['total_hours'],
            timesheet.total_hrs)
        self.assertEquals(str(response.context['timesheet_det'][0].__class__),
            "<class 'MonitoringSystem.timesheet.models.TimesheetDetails'>")
        self.assertEquals(response.status_code, 200)

    def test_send_for_approval(self):
        self.test_save()
        selected_date = self.today.strftime('%d-%b-%Y')
        timesheet = Timesheet.objects.all()[0].id
        timesheet_det = TimesheetDetails.objects.all()
        response = self.client.post('/timesheet/save/', {
            'selected_date': selected_date,
            'timesheet_id' + selected_date: timesheet,
            'timesheet_det_id' + selected_date + '1': timesheet_det[0].id,
            'timesheet_det_id' + selected_date + '2': timesheet_det[1].id,
            'timesheet_det_id' + selected_date + '3': timesheet_det[2].id,
            'effort_time' + selected_date + '1': '02:05',
            'effort_time' + selected_date + '2': '03:15',
            'effort_time' + selected_date + '3': '01:45',
            'effort_table_len' + selected_date: '4',
            'task_cat' + selected_date + '1': 'group',
            'task_cat' + selected_date + '2': 'group',
            'task_cat' + selected_date + '3': 'general',
            'task_id' + selected_date + '1': self.group,
            'task_id' + selected_date + '2': self.group,
            'task_id' + selected_date + '3': self.general,
            'record_status': 'RS17',
            'tot_hrs' + selected_date: '07:05',
            'delete_timesheet' + selected_date: '',
            })
        saved_timesheet = Timesheet.objects.all()
        self.assertEquals(len(saved_timesheet), 1)
        self.assertEquals(len(TimesheetDetails.objects.all()), 3)
        self.assertEquals(len(ApproveTimesheetDetails.objects.all()), 0)
        self.assertEquals(saved_timesheet[0].record_status_id, 'RS17')
        self.assertEquals(response.status_code, 302)
        response = self.client.post('/timesheet/create/', {})
        self._test_permissions(response.context['page_data']['datelist'])

    def test_approval(self):
        self.test_send_for_approval()
        selected_date = self.today.strftime('%d-%b-%Y')
        timesheet = Timesheet.objects.all()[0].id
        timesheet_det = TimesheetDetails.objects.all()
        response = self.client.post('/timesheet/save/', {
            'selected_date': selected_date,
            'timesheet_id' + selected_date: timesheet,
            'timesheet_det_id' + selected_date + '1': timesheet_det[0].id,
            'timesheet_det_id' + selected_date + '2': timesheet_det[1].id,
            'timesheet_det_id' + selected_date + '3': timesheet_det[2].id,
            'effort_time' + selected_date + '1': '02:05',
            'effort_time' + selected_date + '2': '03:15',
            'effort_time' + selected_date + '3': '01:45',
            'effort_table_len' + selected_date: '4',
            'task_cat' + selected_date + '1': 'group',
            'task_cat' + selected_date + '2': 'group',
            'task_cat' + selected_date + '3': 'general',
            'task_id' + selected_date + '1': self.group,
            'task_id' + selected_date + '2': self.group,
            'task_id' + selected_date + '3': self.general,
            'record_status': 'RS4',
            'tot_hrs' + selected_date: '07:05',
            'delete_timesheet' + selected_date: '',
            })
        saved_timesheet = Timesheet.objects.all()
        self.assertEquals(len(saved_timesheet), 1)
        self.assertEquals(len(TimesheetDetails.objects.all()), 3)
        self.assertEquals(len(ApproveTimesheetDetails.objects.all()), 3)
        self.assertEquals(saved_timesheet[0].record_status_id, 'RS4')
        self.assertEquals(response.status_code, 302)
        response = self.client.post('/timesheet/create/', {})
        self._test_permissions(response.context['page_data']['datelist'])

    def test_edit_approved_timesheet(self):
        self.test_approval()
        timesheet = Timesheet.objects.all()[0]
        response = self.client.get('/timesheet/edit/', {
            'timesheet_id': timesheet.id,
            'selected_date': self.today.strftime('%d-%b-%Y'),
            'edit_type': 'multi_approval'})
        self.assertEquals(len(response.context['timesheet_det']), 3)
        '''
        check timesheet total hrs with approved_total_hrs and check
        timesheet details table name
        '''
        self.assertEquals(response.context['total_hours'],
            timesheet.approved_total_hrs)
#self.assertEquals(str(response.context['timesheet_det'][0].__class__),
#"<class 'MonitoringSystem.timesheet.models.ApprovedTimesheetDetails'>")
        self.assertEquals(response.status_code, 200)

    def test_reject(self):
        self.test_send_for_approval()
        selected_date = self.today.strftime('%d-%b-%Y')
        timesheet = Timesheet.objects.all()[0].id
        timesheet_det = TimesheetDetails.objects.all()
        response = self.client.post('/timesheet/save/', {
            'selected_date': selected_date,
            'timesheet_id' + selected_date: timesheet,
            'timesheet_det_id' + selected_date + '1': timesheet_det[0].id,
            'timesheet_det_id' + selected_date + '2': timesheet_det[1].id,
            'timesheet_det_id' + selected_date + '3': timesheet_det[2].id,
            'effort_time' + selected_date + '1': '02:05',
            'effort_time' + selected_date + '2': '03:15',
            'effort_time' + selected_date + '3': '01:45',
            'effort_table_len' + selected_date: '4',
            'task_cat' + selected_date + '1': 'group',
            'task_cat' + selected_date + '2': 'group',
            'task_cat' + selected_date + '3': 'general',
            'task_id' + selected_date + '1': self.group,
            'task_id' + selected_date + '2': self.group,
            'task_id' + selected_date + '3': self.general,
            'record_status': 'RS18',
            'tot_hrs' + selected_date: '07:05',
            'delete_timesheet' + selected_date: '',
            })
        saved_timesheet = Timesheet.objects.all()
        self.assertEquals(len(saved_timesheet), 1)
        self.assertEquals(len(TimesheetDetails.objects.all()), 3)
        self.assertEquals(len(ApproveTimesheetDetails.objects.all()), 0)
        self.assertEquals(saved_timesheet[0].record_status_id, 'RS18')
        self.assertEquals(response.status_code, 302)
        response = self.client.post('/timesheet/create/', {})
        self._test_permissions(response.context['page_data']['datelist'])

    def test_multi_approval(self):
        self._save_timesheet()
        self._save_timesheet()
        self._save_timesheet()
        saved_timesheet = Timesheet.objects.all()
        response = self.client.get('/timesheet/multi_approval/', {
            'selected_id': str(saved_timesheet[0].id) + ','\
                + str(saved_timesheet[1].id) + ',' +\
                str(saved_timesheet[2].id)})
        approved_timesheet = Timesheet.objects.filter(record_status='RS4')
        self.assertEquals(len(saved_timesheet), len(approved_timesheet))
        self.assertEquals(response.status_code, 302)

    def test_previous_duration_save(self):
        resources = Resources.objects.all()
        response = self.client.post('/timesheet/save_previous_duration/', {
            'employee_len': '3',
            'emp_id1': resources[0].id,
            'emp_id2': resources[1].id,
            'emp_id3': resources[2].id,
            'previous_duration1': '5',
            'previous_duration2': '25',
            'previous_duration3': '15',
            })
        resources = Resources.objects.all()
        self.assertEquals(resources[0].timesheet_duration, 5)
        self.assertEquals(resources[1].timesheet_duration, 25)
        self.assertEquals(resources[2].timesheet_duration, 15)
        self.assertEquals(response.status_code, 302)

    def test_approval_list(self):
        response = self.client.post('/timesheet/list/', {})
        resources = Resources.objects.filter(
            reporting_manager=self.client.session.items()[0][1])
        self.assertEquals(
            len(resources), len(response.context['page_data']['emp_details']))
        self.assertEquals(response.status_code, 200)
