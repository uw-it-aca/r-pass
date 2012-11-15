from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from r_pass.authz_implementation.all_ok import AllOK
from r_pass.authz_implementation.all_fail import AllFail

class AuthZ():
    def __init__(self):
        self._backend = self._get_backend_module()

    def is_member_of_group(self, user_name, group):
        return self._backend.is_member_of_group(user_name, group)

    def has_access_to_service(self, user_name, service):
        for group in service.groups.all():
            if self.is_member_of_group(user_name, group.source_id):
                return True
        return False

    def group_display_name(self, group_source_id):
        if hasattr(self._backend, "group_display_name"):
            return self._backend.group_display_name(group_source_id)
        return group_source_id

    def _get_backend_module(self):
        if hasattr(settings, "R_PASS_GROUP_BACKEND"):
            # This is all taken from django's static file finder
            module, attr = getattr(settings, "R_PASS_GROUP_BACKEND").rsplit('.', 1)
            try:
                mod = import_module(module)
            except ImportError, e:
                raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                           (module, e))
            try:
                authz_module = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a '
                                   '"%s" class' % (module, attr))
            return authz_module()
        else:
            if settings.DEBUG:
                print "You should set an R_PASS_GROUP_BACKEND in you settings.py"
                return AllOK()
            else:
                print "You need to set an R_PASS_GROUP_BACKEND in you settings.py"
                return AllFail()


