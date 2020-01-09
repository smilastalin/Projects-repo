import os
import time
import random
import md5
import uuid
import sys
import logging

from django.contrib.auth.models import UserManager
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from datetime import datetime, date
from django.core import mail
#from django.db import router
#from django.contrib import admin
#from django.db.models.deletion import Collector
#from django.utils.text import capfirst
#from django.utils.encoding import force_unicode, smart_unicode, smart_str

ERROR_MESSAGE = 'ERROR : %s \nLINE NUMBER : %s'

class Utility:
    def __init__(self):
        return

    def Guid(self):
        uniqueId = str(uuid.uuid4())        
        return uniqueId[:36]

    def GeneratePassword(self):
        """
        >>> from jtm.Utilities import Utility
        >>> Utility().GeneratePassword()
        'Zgf3Xu'
        >>>
        """
        return UserManager().make_random_password(length=6, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')

    def get_values(self, objects):
        """ return the values in tuples with name and pk for choice field """
        return [(str(each.pk).strip(), str(each.name).strip()) for each in objects]

    def get_strvalues(self, objects):
        """ return the values in tuples with name and pk for choice field """
        return [(str(each.name).strip(), str(each.name).strip()) for each in objects]

    def get_all_modules(self):
        EXCLUDE_AUTHERIZATION = [u'accesscontrol', u'sessions', u'sites', u'auth', u'contenttypes', u'address', 'admin']
        return list(set([(obj.app_label) for obj in ContentType.objects.all() if not EXCLUDE_AUTHERIZATION.__contains__(obj.app_label)]))

    ### This method used for change the application date format(%d-%b-%Y) into database format(%Y-%m-%d)
    def getdate(self, data):
        newdate = ''
        try:
            olddate = datetime.strptime(data, settings.APP_DATE_FORMAT)
            newdate = datetime.strftime(olddate, settings.DB_DATE_FORMAT)
        except:
            return newdate
        return newdate

    ### This method returns the start date of every month between the start and end dates
    def spanning_months(self, start, end):
        assert start <= end
        current = start.year * 12 + start.month - 1
        end = end.year * 12 + end.month - 1
        while current <= end:
            yield date(current // 12, current % 12 + 1, 1)
            current += 1


class Email:
    def __init__(self):
        return

    def send_email(self, subject, message, recipients, contenttype='plain', attach='', from_email='', copyc='', trigger_count=0):
        #try:
        #    from django.core.mail import EmailMessage, SMTPConnection, send_mail
        #    passworddata = ''
        #    from settings import EMAIL_USE_TLS
        #    emaildata = EmailSettings.objects.all()
        #    emaildata = '' if (len(emaildata) <= 0) else emaildata[0]
        #    if emaildata:
        #        passworddata = base64.b64decode(emaildata.email_host_password)
        #    EMAIL_HOST = emaildata.email_host
        #    EMAIL_HOST_USER = emaildata.email_host_user
        #    EMAIL_HOST_PASSWORD = passworddata
        #    EMAIL_PORT = emaildata.email_port

        try:
            from django.core.mail import EmailMessage, SMTPConnection, send_mail
            from settings import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_USE_TLS
        finally:
            try:
                if(EMAIL_HOST_USER != ''):
                    from_email = EMAIL_HOST_USER
                #connection = SMTPConnection(EMAIL_HOST, EMAIL_PORT, from_email, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS)
                connection = mail.get_connection()
                # Manually open the connection
                connection.open()
                #print 'copyc test god',copyc, len(copyc)
                subject = subject.replace('\t', '  ')
                subject = subject.replace('\n', '  ')
                message = message.replace('\t', '  ')
                message = message.replace('\n', '<br>')
                
                if(copyc != '' and len(copyc) > 0):
                    emailMessage = EmailMessage(subject, message, from_email, recipients, cc=copyc)
                else:
                    emailMessage = EmailMessage(subject, message, from_email, recipients)
                emailMessage.content_subtype = contenttype
                if attach.strip() != '':
                    emailMessage.attach_file(attach)
                if trigger_count < 2:
                    try:
                        connection.send_messages([emailMessage])
                    except:
                        if sys.exc_info()[1] == 'Connection unexpectedly closed':
                            logging.info('connection_closed:True')
                        trigger_count += 1
                        errMessage = ERROR_MESSAGE % (sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
                        logging.info('mailsend: connection_closed_error : ' + errMessage)
                        time.sleep(70)
                        self.send_email(subject, message, recipients, \
                            contenttype=contenttype, attach=attach, from_email=from_email, copyc=copyc, trigger_count=trigger_count)
                # We need to manually close the connection.
                connection.close()
            except:
                errMessage = ERROR_MESSAGE % (sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
                logging.info('mailsend Error : ' + errMessage)


def GetDateType(dateString, format=None):
    if(format == None):
        format = settings.DATE_FORMAT
        format = format.replace('d', '%d')
        format = format.replace('m', '%m')
        format = format.replace('Y', '%Y')
    try:
        return datetime.strptime(dateString, format).date()
    except:
        return datetime.strptime('2000-01-01', "%Y-%m-%d").date()


def get_jtm_user(request):
    return request.session.get('jtm_user', None)


def flatten(lst):
    for elem in lst:
        if type(elem) in (tuple, list, QuerySet):
            for i in flatten(elem):
                yield i
        else:
            yield elem


def getfilepath(request, filename, folder='files'):
    fileUploaded = request.FILES[filename]
    check = 0
    filename = fileUploaded.name
    currentdir = settings.MEDIA_ROOT
    currentosdir = currentdir + '/' + folder
    currentdir = os.listdir(currentdir)
    for each in currentdir:
        if each == folder:
            check = 1

    if(check != 1):
        os.mkdir(currentosdir)

    fd = open('%s/%s' % (currentosdir, filename), 'wb')
    for chunk in fileUploaded.chunks():
        fd.write(chunk)
    fd.close()
    filepath = settings.MEDIA_ROOT + '/' + folder + '/' + filename if filename != '' else ''
    return filepath

#class CustomDelete():
#    def __init__(self):
#        return
#
#    def get_deleted_objects(self, objs, opts, user, admin_site, using):
#        """
#        Find all objects related to ``objs`` that should also be deleted. ``objs``
#        must be a homogenous iterable of objects (e.g. a QuerySet).
#
#        Returns a nested list of strings suitable for display in the
#        template with the ``unordered_list`` filter.
#
#        """
#        collector = NestedObjects(using=using)
#        collector.collect(objs)
#        perms_needed = set()
#
#        def format_callback(obj):
#            has_admin = obj.__class__ in admin_site._registry
#            opts = obj._meta
#
#            if has_admin:
#                admin_url = reverse('%s:%s_%s_change'
#                                    % (admin_site.name,
#                                       opts.app_label,
#                                       opts.object_name.lower()),
#                                    None, (quote(obj._get_pk_val()),))
#                p = '%s.%s' % (opts.app_label,
#                               opts.get_delete_permission())
#                if not user.has_perm(p):
#                    perms_needed.add(opts.verbose_name)
#                # Display a link to the admin page.
#                return mark_safe(u'%s: <a href="%s">%s</a>' %
#                                 (escape(capfirst(opts.verbose_name)),
#                                  admin_url,
#                                  escape(obj)))
#            else:
#                # Don't display link to edit, because it either has no
#                # admin or is edited inline.
#                return u'%s: %s' % (capfirst(opts.verbose_name),
#                                    force_unicode(obj))
#
#        to_delete = collector.nested(format_callback)
#
#        protected = [format_callback(obj) for obj in collector.protected]
#
#        return to_delete, perms_needed, protected
#
#
#class NestedObjects(Collector):
#    def __init__(self, *args, **kwargs):
#        super(NestedObjects, self).__init__(*args, **kwargs)
#        self.edges = {} # {from_instance: [to_instances]}
#        self.protected = set()
#
#    def add_edge(self, source, target):
#        self.edges.setdefault(source, []).append(target)
#
#    def collect(self, objs, source_attr=None, **kwargs):
#        for obj in objs:
#            if source_attr:
#                self.add_edge(getattr(obj, source_attr), obj)
#            else:
#                self.add_edge(None, obj)
#        try:
#            return super(NestedObjects, self).collect(objs, source_attr=source_attr, **kwargs)
#        except models.ProtectedError, e:
#            self.protected.update(e.protected_objects)
#
#    def related_objects(self, related, objs):
#        qs = super(NestedObjects, self).related_objects(related, objs)
#        return qs.select_related(related.field.name)
#
#    def _nested(self, obj, seen, format_callback):
#        if obj in seen:
#            return []
#        seen.add(obj)
#        children = []
#        level = 1
#        for child in self.edges.get(obj, ()):
#            if(level == 1):
#                children.extend(self._nested(child, seen, format_callback))
#                level += 1
#        if format_callback:
#            ret = [format_callback(obj)]
#        else:
#            ret = [obj]
#        if children:
#            ret.append(children)
#        return ret
#
#    def nested(self, format_callback=None):
#        """
#        Return the graph as a nested list.
#
#        """
#        seen = set()
#        roots = []
#        for root in self.edges.get(None, ()):
#            roots.extend(self._nested(root, seen, format_callback))
#        return roots
