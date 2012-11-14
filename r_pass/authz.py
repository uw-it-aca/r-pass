
# XXX - this needs to branch out to implementations, based on config.
# For instance, at the uw, we want this to connect to the group web service

class AuthZ():
    def has_access_to_service(self, user_name, service):
        return True
