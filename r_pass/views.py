from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from r_pass.models import Service, AccessToken, Host, Group
from r_pass.forms import ServiceForm
from r_pass.authz import AuthZ
import logging

@login_required
def home(request):
    data = {}
    data["services"] = []
    authz = AuthZ()
    services = Service.objects.all()
    for service in services:
        if authz.has_access_to_service(request.user, service):
            data["services"].append({
                "title": service.title,
                "url": service.view_url(),
                "description": service.description,
            })
    return render_to_response('services.html', data)

@login_required
def create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            hosts = form.cleaned_data["hosts"].split()
            groups = form.cleaned_data["groups"].split()

            service = Service()
            service.title = form.cleaned_data["title"]
            service.description = form.cleaned_data["description"]
            service.save()

            for host in hosts:
                model, create = Host.objects.get_or_create(cname=host)
                service.hosts.add(model)

            for group in groups:
                model, create = Group.objects.get_or_create(source_id=group)
                service.groups.add(model)

            access_token = AccessToken()
            access_token.name = form.cleaned_data["access_name"]
            access_token.description = form.cleaned_data["access_description"]
            access_token.user = form.cleaned_data["access_user"]
            access_token.access_token= form.cleaned_data["access_token"]
            access_token.service = service

            access_token.save()

            _log(request, "Created service id: %s, name: %s" % (service.pk, service.title))
            return HttpResponseRedirect(service.view_url())
    else:
        form = ServiceForm()

    context = {}
    context.update(csrf(request))
    context["form"] = form
    return render_to_response('create.html', context)

@login_required
def service(request, service_id):

    service = None
    try:
        service = Service.objects.get(pk=service_id)
    except ObjectDoesNotExist:
        return HttpResponse("Not Found", status=404,)

    authz = AuthZ()
    if not authz.has_access_to_service(request.user, service):
        _log(request, "Tried to view service - no access.  id: %s, name: %s" % (service.pk, service.title))
        return HttpResponse(status=403)

    _log(request, "Viewed service id: %s, name: %s" % (service.pk, service.title))
    data = {}
    data["service"] = service
    data["hosts"] = service.hosts.all()
    data["tokens"] = AccessToken.objects.filter(service=service)

    data["groups"] = []
    for group in service.groups.all():
        data["groups"].append({
            "display": authz.group_display_name(group.source_id),
            "id": group.source_id,
        })
    return render_to_response("service_details.html", data)


def _log(request, message):
    logger = logging.getLogger('r_pass.data_log')
    logger.info("%s: %s", request.user, message)

