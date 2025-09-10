from django.shortcuts import render
from django.template import loader
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse, reverse_lazy


# Views
@login_required(login_url=reverse_lazy('login'))
def kb_overview(request: HttpRequest):
    """ Overview page. """

    variables = {
        'page': "Overview",
    }

    template = loader.get_template('kb-overview.html')
    return HttpResponse(template.render(variables, request))

