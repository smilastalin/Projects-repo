from django.db import models
from django.contrib.auth.models import User

from MonitoringSystem.common.master.models import RecordStatus, GroupTask
from MonitoringSystem.common.master.models import GeneralTask, Role
from MonitoringSystem.common.ts_user.models import Resources
from MonitoringSystem.RATS.resource_allocation.models import \
    TaskAllocationDetails
from MonitoringSystem.OITS.project_budget.models import ProjectBudget
from MonitoringSystem.fields import UUIDField


class Timesheet(models.Model):
    id = UUIDField(primary_key=True)
    resource = models.ForeignKey(Resources, blank=True, null=True)
    entry_date = models.DateField(blank=True, null=True)
    record_status = models.ForeignKey(RecordStatus, blank=True, null=True)
    comments = models.TextField(blank=True, null=True, default="")
    reviewer = models.ForeignKey(Resources, related_name='timesheet_reviewer',
        null=True)
    total_hrs = models.TimeField(blank=True, null=True)
    approved_total_hrs = models.TimeField(blank=True, null=True)
    on_leave = models.BooleanField(default=False)
    holiday = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_lock = models.BooleanField(default=True)
    #audit fields
    created_by = models.ForeignKey(User, related_name='timesheet_create',
        null=True)
    created_on = models.DateField(blank=True, null=True)
    modified_by = models.ForeignKey(User, related_name='timesheet_modify',
        null=True)
    modified_on = models.DateTimeField(auto_now=True)
    approved_on = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'Timesheet'


class TimesheetDetails(models.Model):
    id = UUIDField(primary_key=True)
    timesheet = models.ForeignKey(Timesheet, blank=True, null=True)
    task_category = models.CharField(max_length=50, blank=True, null=True)
    project_task = models.ForeignKey(TaskAllocationDetails, blank=True,
        null=True)
    group_task = models.ForeignKey(GroupTask, blank=True, null=True)
    general_task = models.ForeignKey(GeneralTask, blank=True, null=True)
    effort = models.TimeField(blank=True, null=True)
    task_completion = models.CharField(max_length=10, blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'TimesheetDetails'


class ApproveTimesheetDetails(models.Model):
    id = UUIDField(primary_key=True)
    timesheet = models.ForeignKey(Timesheet, blank=True, null=True)
    task_category = models.CharField(max_length=50, blank=True, null=True)
    project_task = models.ForeignKey(TaskAllocationDetails, blank=True,
        null=True)
    group_task = models.ForeignKey(GroupTask, blank=True, null=True)
    general_task = models.ForeignKey(GeneralTask, blank=True, null=True)
    effort = models.TimeField(blank=True, null=True)
    task_completion = models.CharField(max_length=10, blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'ApproveTimesheetDetails'
