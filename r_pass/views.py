from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from r_pass.models import Service, AccessToken, Host, Group
from r_pass.forms import ServiceForm
from authz_group import Group as AuthZ
import logging
import markdown2


def has_access_to_service(user, service):
    for group in service.groups.all():
        if AuthZ().is_member_of_group(user, group.source_id):
            return
    raise PermissionDenied


@login_required
def home(request):
    context = {}
    context["services"] = []
    md = markdown2.Markdown(safe_mode="escape")
    for service in Service.objects.all():
        try:
            has_access_to_service(request.user, service)
            context["services"].append({
                "title": service.title,
                "url": service.view_url(),
                "description": md.convert(service.description),
            })
        except PermissionDenied:
            pass
    return render(request, "services.html", context)


@login_required
def _create_or_edit(request, service):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            hosts = form.cleaned_data["hosts"].split()
            groups = form.cleaned_data["groups"].split()

            # Check to make sure the user will have access to the
            # credential they're creating
            can_view_new_service = False
            for group in groups:
                if AuthZ().is_member_of_group(request.user, group):
                    can_view_new_service = True
                    break

            if can_view_new_service:
                service_is_new = False if (service.pk) else True
                service.title = form.cleaned_data["title"]
                service.description = form.cleaned_data["description"]
                service.save()

                service.hosts.clear()
                for host in hosts:
                    model, create = Host.objects.get_or_create(cname=host)
                    service.hosts.add(model)

                service.groups.clear()
                for group in groups:
                    model, create = Group.objects.get_or_create(
                        source_id=group)
                    service.groups.add(model)

                AccessToken.objects.filter(service=service).delete()
                access_token = AccessToken()
                access_token.name = form.cleaned_data["access_name"]
                access_token.description = (
                    form.cleaned_data["access_description"])
                access_token.user = form.cleaned_data["access_user"]
                access_token.access_token = form.cleaned_data["access_token"]
                access_token.service = service
                access_token.save()

                if service_is_new:
                    _log(request, "Created service id: %s, name: %s" % (
                        service.pk, service.title))
                else:
                    _log(request, "Edited service id: %s, name: %s" % (
                        service.pk, service.title))
                return HttpResponseRedirect(service.view_url())
            else:
                form._errors["groups"] = form.error_class(
                    ["You don't have access to this service with "
                     "the groups given"])

    else:
        data = None
        if (service and service.pk):
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

    if (service and service.pk):
        submit_url = service.edit_url()
    else:
        submit_url = "/r-pass/create"

    context = {}
    context["form"] = form
    context["submit_url"] = submit_url
    return render(request, "create_edit.html", context)


@login_required
def create(request):
    return _create_or_edit(request, Service())


@login_required
def edit(request, service_id):
    try:
        service = Service.objects.get(pk=service_id)
        has_access_to_service(request.user, service)
    except Service.DoesNotExist:
        return HttpResponse("Not Found", status=404)
    except PermissionDenied:
        _log(request, "Unauthorized to view service. id: %s, name: %s" % (
            service.pk, service.title))
        return HttpResponse("Unauthorized", status=403)

    return _create_or_edit(request, service)


@login_required
def service(request, service_id):
    try:
        service = Service.objects.get(pk=service_id)
        has_access_to_service(request.user, service)
    except Service.DoesNotExist:
        return HttpResponse("Not Found", status=404)
    except PermissionDenied:
        _log(request, "Unauthorized to view service. id: %s, name: %s" % (
            service.pk, service.title))
        return HttpResponse("Unauthorized", status=403)

    md = markdown2.Markdown(safe_mode="escape")

    context = {}
    context["service"] = service
    context["service_description"] = md.convert(service.description)
    context["hosts"] = service.hosts.all()

    context["tokens"] = AccessToken.objects.filter(service=service)
    for token in context["tokens"]:
        token.markdown_description = md.convert(token.description)

    context["groups"] = []
    for group in service.groups.all():
        context["groups"].append({
            "display": AuthZ().group_display_name(group.source_id),
            "id": group.source_id,
            "membership_url": AuthZ().group_membership_url(group.source_id),
        })

    context["edit_url"] = service.edit_url()

    _log(request, "Viewed service. id: %s, name: %s" % (
        service.pk, service.title))
    return render(request, "service_details.html", context)


def _log(request, message):
    logger = logging.getLogger(__name__)
    logger.info("%s: %s", request.user, message)
