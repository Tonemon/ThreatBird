
from django.http import HttpRequest
from django.contrib.auth.models import Group

from intel.models import *



#### DATABASE INITIALIZATION FUNCTIONS - MOVE TO MANAGEMENT ####
from django.contrib.auth.models import Group, User
from django.conf import settings

def initialize_threatbird():
    """ Initializes the database with the right groups, users and settings. """

    all_existing_users = User.objects.all()

    for systemgroup in settings.SYSTEM_GROUP_NAMES.keys():
        try:
            newgroup = Group.objects.create(name=systemgroup)

            if newgroup and systemgroup.startswith("notifications-"):
                for existinguser in all_existing_users:
                    existinguser.groups.add(newgroup)
                    existinguser.save()

        except Exception as e:   # we should except if already exists (find out which error)
            pass

#### END INITIALIZATION FUNCTIONS ####



# Notification system related functions
def get_current_user_from_group(request: HttpRequest, group: str = ""):
    """
    Tries to get the user from the `HttpRequest` from the group. This is used for checking
    if a `User` is in a specific notifications `Group` and should receive a notification
    from a specific notification group/stream.
    """

    try:
        thegroup = Group.objects.get(name=group)
        if thegroup.user_set.contains(request.user):
            return request.user

    except Group.DoesNotExist:
        return None

