from django.apps import apps
from django.urls import path

from .views.general import CreateView, DeleteView, UpdateView, AddNewElement

app_name = "achievements"


def generate_urls(model):
    creatview = type(f"Create{model.__name__}View", (CreateView,), {"model": model})
    editview = type(f"Edit{model.__name__}View", (UpdateView,), {"model": model})
    deleteview = type(f"Delete{model.__name__}View", (DeleteView,), {"model": model})
    model_name = model._meta.model_name

    return [
        path(f"<uuid:pk>/{model_name}/", creatview.as_view(), name=f"create_{model_name}"),
        path(f"{model_name}s/<uuid:pk>/edit", editview.as_view(), name=f"{model_name}_edit"),
        path(f"{model_name}s/<uuid:pk>/delete", deleteview.as_view(), name=f"{model_name}_delete"),
    ]


urlpatterns = [
    path("<uuid:pk>/add", AddNewElement.as_view(), name="new_achievement"),
]

for model in apps.get_app_config("achievement").get_models():
    urlpatterns.extend(generate_urls(model))
