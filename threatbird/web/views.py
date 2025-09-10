from django.shortcuts import render
from django.template import loader
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse, reverse_lazy

from notifications.signals import notify
from django.contrib.auth.models import User, Group
from intel.models import APTGroup
from intel.models import Technique
from web.utils import *

# Views
@login_required(login_url=reverse_lazy('login'))
def overview(request: HttpRequest):
    """ Overview page. """

    variables = {
        'page': "Overview",
    }

    template = loader.get_template('web-overview.html')
    return HttpResponse(template.render(variables, request))


@login_required(login_url=reverse_lazy('login'))
def notifications(request: HttpRequest):
    """ Notifications page. """

    allnotifications = request.user.notifications.all()

    variables = {
        'page': "Notifications",
        'allnotifications': allnotifications,
    }

    template = loader.get_template('web-notifications.html')
    return HttpResponse(template.render(variables, request))


# Other views
def example(request: HttpRequest):
    """ example page. """

    variables = {
        'page': "Example page",
    }

    template = loader.get_template('example.html')
    return HttpResponse(template.render(variables, request))
