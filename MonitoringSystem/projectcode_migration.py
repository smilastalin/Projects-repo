import csv
import sys

from django.conf import settings
from django.http import HttpResponseNotModified
from django.utils.translation import ugettext as _

from MonitoringSystem.OITS.oi.models import *
from MonitoringSystem.OITS.project_budget.models import *
from MonitoringSystem.common.logs.logger import CapturLog

ERROR_MESSAGE = 'ERROR : %s \nLINE NUMBER : %s'
MODULE = 'PROJECTCODE_MIGRATION'
MESSAGE = {'': '',
            'UPDATE': ('Project code updated successfully'),
            'UPDATEERROR': ('Project code update unsuccessful'),
        }


def pojectcode_migration(request):
    try:
        output = ''
        filename = settings.MEDIA_ROOT + "/projectcodelist.csv"
        count = 0
        spamReader = csv.reader(open(filename, 'rb'), delimiter=';')
        address_id = ''
        for row in spamReader:
            if(count > 1):
                if(row.__len__() < 5):
                    continue
                base_budget = BaseBudget.objects.filter(project_code=row[2].strip(), oi__oinumber=row[1].strip())
                if(len(base_budget) > 0):
                    base_budget = base_budget[0]
                    project_code = base_budget.project_code
                    old_proj_code = row[4].strip()
                    if(project_code[:8] == old_proj_code[:8]):
                        BaseBudget.objects.filter(project_code=row[2].strip(), oi__oinumber=row[1].strip()).update(code=old_proj_code[-3:], project_code=old_proj_code)
                    else:
                        output += ' Not Updated: ' + row[2]
                else:
                    output += ' Not Exists: ' + row[2]
            count = count + 1
        CapturLog().LogData(request, 'Update', MODULE, output)
    except:
        errMessage = ERROR_MESSAGE % (sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
        CapturLog().LogData(request, 'UpdateError', MODULE, errMessage)
    return HttpResponseNotModified()
