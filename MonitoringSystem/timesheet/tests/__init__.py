from MonitoringSystem.common.ts_user.tests.viewstest import LoginTest
from MonitoringSystem.timesheet.tests.viewstest import TimesheetTest

__test__ = {
    'PROJECT_TESTS': TimesheetTest,
    'LOGIN_TESTS': LoginTest,
}
