# Django settings for MonitoringSystem project.
import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': '',                      # Or path to database file if using sqlite3.
#        'USER': '',                      # Not used with sqlite3.
#        'PASSWORD': '',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
#}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Calcutta'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
EXPORT_PATH = '/home/sangeetha/Projects/Thinksoft/trunk/src/MonitoringSystem/media/documents/'
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(os.path.realpath(os.path.dirname(__file__)), 'media'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'u_&6!_8w00j394*d9-b#1ot6fzv5yq(aqo4j^6e6tiwokhp5l9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
INTERNAL_IPS = ('127.0.0.1',)
ROOT_URLCONF = 'MonitoringSystem.urls'

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
    os.path.join(os.path.dirname(__file__), "templates"),
#    "/usr/local/lib/python2.6/dist-packages/django_debug_toolbar-0.9.4-py2.6.egg/debug_toolbar/templates"
)
#DEBUG_TOOLBAR_CONFIG = {
#    'INTERCEPT_REDIRECTS': False,
#}
DATE_FORMAT = 'd-M-Y'
PAGE_SIZE = 15

APP_DATE_FORMAT = "%d-%b-%Y"
DB_DATE_FORMAT = "%Y-%m-%d"

### Ldap auth settings
AUTHENTICATION_BACKENDS = (
    'MonitoringSystem.access_control.authentication.LDAPBackend1',
    'MonitoringSystem.access_control.authentication.LDAPBackend2',
    'django.contrib.auth.backends.ModelBackend',
    #'MonitoringSystem.access_control.permission.ObjectPermission',
)

LDAP_SERVER1 = '192.168.1.141'
LDAP_SERVER2 = '192.168.1.141'
USER_SESSION_TIMEOUT = 60
LOGIN_DOMAIN = ''
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'smila@fifthgentech.com'
EMAIL_HOST_PASSWORD = 'selvastalin1988'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_CONTENT_TYPE = 'html'

CRON_POLLING_FREQUENCY = 86400

# ERP configurations
ERP_FILE = os.path.join(PROJECT_ROOT, 'ERP_log')
ERP_ID_UPDATE = False
ERP_HOST = '192.168.1.38\SQLEXPRESS'
ERP_USER = 'sa'
ERP_PASSWORD = 'Sql2008'
ERP_DATABASE = 'erp_oct18'
ERP_THINKSOFT_ENTITY = '59327d56-5bc1-11e1-9735-0e7aec00b83f'


#ADR ERP configurations
ADR_SC_LOG_PATH = os.path.join(MEDIA_ROOT, 'adr_staging_log/adr_sc_log/')
ADR_SC_ERR_LOG_PATH = os.path.join(MEDIA_ROOT, 'adr_staging_log/adr_sc_err_log/')
SC_ADR_LOG_PATH = os.path.join(MEDIA_ROOT, 'adr_staging_log/sc_adr_log/')
SC_ADR_ERR_LOG_PATH = os.path.join(MEDIA_ROOT, 'adr_staging_log/sc_adr_err_log/')
ADR_ERR_LOG_FILE_IS_UPDATE = 0
ADR_ID_UPDATE = True
ADR_HOST = '192.168.1.57\SQLEXPRESS'
ADR_USER = 'sa'
ADR_PASSWORD = 'Sql2008'
ADR_DATABASE = 'adrenalin'#TS_Adrenalin#adr_new1
LOG_URL_PATH = 'http://192.168.1.40:8000/static/adr_staging_log/'

#Query_browser configrations
QRY_BROWSER_HOST = '127.0.0.1'#'192.168.1.39'
QRY_BROWSER_USER = 'root'
QRY_BROWSER_PASSWORD = 'root'
QRY_BROWSER_DATABASE = 'thinksoft'

#Timesheet configrations
TIMESHEET_EFFORT_MIN_LIMIT = 7
TIMESHEET_EFFORT_MAX_LIMIT = 10

#IIS configrations
IIS_HOST = "192.168.1.41"
IIS_SHARED_NAME = 'smila_shared'
IIS_USER = "senthilkumar"
IIS_PASSWORD = "Fiveg123"
LOCALUSER = "linuxuser"
ROOT_PASSWORD = "password"

# Imported master data file configrations
IMPORT_FILE_PATH = '/home/linuxuser/projects/Thinksoft/trunk/src/MonitoringSystem/media/Consolidated Project Taskscsv.csv'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    #'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    #'django_jenkins',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
#    'debug_toolbar',
    'fields',
    'common.client',
    'common.alert',
    'common.grid',
    'common.holiday',    
    'MonitoringSystem.django_cron',
    'MonitoringSystem.common.master',
    'MonitoringSystem.common.holiday',
    'MonitoringSystem.ERP',
    'MonitoringSystem.ADR_ERP',
    'MonitoringSystem.query_browser',
    'MonitoringSystem.timesheet',
    'seating_management.project_folder_tracker',
    'seating_management.practice_folder',
    'seating_management.seating_unit',
    'OITS.proposal_abstract',
    'OITS.oi_request',
    'OITS.oi',
    'OITS.project_budget',
    'RATS.resourcerelease',
    'RATS.longleave',
    'RATS.onnotice',
    'RATS.resource_allocation',
    'RATS.recruitment',
    'RATS.travel_information',
    'RATS.star_group',
    'RATS.profile_updation',
    'RATS.skill_matrix',
    'RATS.resource_requirement',
    'RATS.bg_client',
    'RATS.bgstandard',
    'RATS.bg_verification',
    'RATS.group_resource',
    'RATS.myprofile',
    'RATS.rap',
    'RATS.resource_projection',
    'RATS.seating_request',
    'RATS.certification_tracker',
    'RATS.input_invoice_sheet',
    'common.ts_user',
    'common.logs',
    'common.security',
    'common.reinstatement',
    'MonitoringSystem.management',
    'MonitoringSystem',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    import local_settings
except ImportError:
    print "error"
    import sys
    sys.exit(1)
else:
    import re
    for attr in dir(local_settings):
        if re.search('^[A-Z]', attr):
            globals()[attr] = getattr(local_settings, attr)

import logging
logging.basicConfig(
    level=logging.INFO,
    format=' %(asctime)s %(levelname)s  %(message)s ',
    filename=os.path.join(os.path.dirname(__file__), 'media/myapp.log'),
    filemode='a',
)
