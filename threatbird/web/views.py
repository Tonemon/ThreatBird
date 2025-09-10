from django.shortcuts import render
from django.template import loader
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse, reverse_lazy


# Views
@login_required(login_url=reverse_lazy('login'))
def web_overview(request: HttpRequest):
    """ Overview page. """

    variables = {
        'page': "Overview",
    }

    template = loader.get_template('web-overview.html')
    return HttpResponse(template.render(variables, request))


@login_required(login_url=reverse_lazy('login'))
def web_notifications(request: HttpRequest):
    """ Notifications page. """

    variables = {
        'page': "Notifications",
    }

    template = loader.get_template('web-overview.html')
    return HttpResponse(template.render(variables, request))


# Other views
def example(request: HttpRequest):
    """ example page. """

    variables = {
        'page': "Example page",
    }

    template = loader.get_template('example.html')
    return HttpResponse(template.render(variables, request))
