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
def _create_or_edit(request, service):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            hosts = form.cleaned_data["hosts"].split()
            groups = form.cleaned_data["groups"].split()

            can_view_new_service = False
            authz = AuthZ()
            # Check to make sure the user will have access to the
            # credential they're creating
            for group in groups:
                if authz.is_member_of_group(request.user, group):
                    can_view_new_service = True
                    break

            if can_view_new_service:
                service.title = form.cleaned_data["title"]
                service.description = form.cleaned_data["description"]
                service_is_new = True
                if service.pk:
                    service_is_new = False
                service.save()

                for host in hosts:
                    model, create = Host.objects.get_or_create(cname=host)
                    service.hosts.add(model)

                for group in groups:
                    model, create = Group.objects.get_or_create(source_id=group)
                    service.groups.add(model)

                AccessToken.objects.filter(service=service).delete()
                access_token = AccessToken()
                access_token.name = form.cleaned_data["access_name"]
                access_token.description = form.cleaned_data["access_description"]
                access_token.user = form.cleaned_data["access_user"]
                access_token.access_token= form.cleaned_data["access_token"]
                access_token.service = service

                access_token.save()

                if service_is_new:
                    _log(request, "Created service id: %s, name: %s" % (service.pk, service.title))
                else:
                    _log(request, "Edited service id: %s, name: %s" % (service.pk, service.title))
                return HttpResponseRedirect(service.view_url())
            else:
                form._errors["groups"] = form.error_class(["You don't have access to this service with the groups given"])

    else:
        data = None
        if service:
            data = {}
            data["title"] = service.title
            data["description"] = service.description

            groups = service.groups.all()
            data["groups"] = "\n".join(map(lambda x: x.source_id, groups))
            hosts = service.hosts.all()
            data["hosts"] = "\n".join(map(lambda x: x.cname, hosts))

            access_tokens = AccessToken.objects.filter(service=service)
            if len(access_tokens):
                token = access_tokens[0]
                data["access_name"] = token.name
                data["access_description"] = token.description
                data["access_user"] = token.user
                data["access_token"] = token.access_token
        form = ServiceForm(data)

    if service and service.pk:
        submit_url = service.edit_url()
    else:
        submit_url = "/r-pass/create"

    context = {}
    context.update(csrf(request))
    context["form"] = form
    context["submit_url"] = submit_url
    return render_to_response('create_edit.html', context)

@login_required
def create(request):
    return _create_or_edit(request, Service())

@login_required
def edit(request, service_id):
    service = None
    try:
        service = Service.objects.get(pk=service_id)
    except ObjectDoesNotExist:
        return HttpResponse("Not Found", status=404,)

    authz = AuthZ()
    if not authz.has_access_to_service(request.user, service):
        _log(request, "Tried to view service - no access.  id: %s, name: %s" % (service.pk, service.title))
        return HttpResponse(status=403)

    return _create_or_edit(request, service)

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
            "membership_url": authz.group_membership_url(group.source_id),
        })

    data["edit_url"] = service.edit_url()
    return render_to_response("service_details.html", data)


def _log(request, message):
    logger = logging.getLogger('r_pass.data_log')
    logger.info("%s: %s", request.user, message)

