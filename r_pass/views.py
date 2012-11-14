from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from r_pass.models import Service, AccessToken
from r_pass.authz import AuthZ

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
def service(request, service_id):

    service = None
    try:
        service = Service.objects.get(pk=service_id)
    except ObjectDoesNotExist:
        return HttpResponse("Not Found", status=404,)

    authz = AuthZ()
    if not authz.has_access_to_service(request.user, service):
        return HttpResponse(status=403)

    data = {}
    data["service"] = service
    data["hosts"] = service.hosts.all()
    data["tokens"] = AccessToken.objects.filter(service=service)

    return render_to_response("service_details.html", data)


