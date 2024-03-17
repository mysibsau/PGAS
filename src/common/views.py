import pdfkit
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'


def handler404(request, *args, **kwargs):
    return render(request, '404.html', status=404)


def handler500(request, *args, **kwargs):
    return render(request, '500.html', status=500)


def handler403(request, *args, **kwargs):
    return render(request, '403.html', status=403)


class PDFView(TemplateView):
    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        response.render()
        data = response.content.decode('utf-8')

        options = {
            "enable-local-file-access": "",
            "margin-top": "0",
            "margin-bottom": "0",
            "margin-left": "0",
            "margin-right": "0",
            'page-size': 'Letter',
            'encoding': "UTF-8",
        }

        response = HttpResponse(content=pdfkit.from_string(data, options=options))
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' \
                                          % 'whatever'
        return response
