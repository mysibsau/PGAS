from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"


def handler404(request, *args, **kwargs):
    return render(request, "404.html", status=404)


def handler500(request, *args, **kwargs):
    return render(request, "500.html", status=500)


def handler403(request, *args, **kwargs):
    return render(request, "403.html", status=403)
