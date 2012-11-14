# This class requires the uw's restclients app.  here mainly as an example
# pacakge

from restclients.gws import GWS

class UWGroupService():
    def has_access_to_service(self, user_name, service):
        gws = GWS()
        for group in service.groups.all():
            if gws.is_effective_member(group.source_id, user_name):
                return True

        return False

    def group_display_name(self, source_id):
        return source_id
