from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from authz_group import Group

class AuthZ():

    def group_membership_url(self, group):
        return Group().group_membership_url(group)

    def is_member_of_group(self, user_name, group):
        return Group().is_member_of_group(user_name, group)

    def has_access_to_service(self, user_name, service):
        backend = Group()
        for group in service.groups.all():
            if backend.is_member_of_group(user_name, group.source_id):
                return True
        return False

    def group_display_name(self, group_source_id):
        return Group().group_display_name(group_source_id)

