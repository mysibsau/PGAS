from django.apps import apps
from django.urls import reverse
from django.views import generic
from django.core.exceptions import PermissionDenied

from statement.models import Statement


class AddNewElement(generic.TemplateView):
    template_name = "general/select_new_element.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["types"] = self.get_exists_achievements()
        context["statement"] = Statement.objects.get(pk=self.kwargs["pk"])
        return context

    def get_exists_achievements(self) -> list[tuple[str, str]]:
        models = apps.get_app_config("achievement").get_models()
        result = []
        for model in models:
            url = reverse(f"achievements:create_{model._meta.model_name}", kwargs=self.kwargs)
            result.append((url, model._meta.verbose_name))
        return result


class GeneralView:
    def get_success_url(self):
        return reverse("statement:detail", kwargs={"pk": self.object.statement.pk})

    @property
    def fields(self):
        fields = self.model._meta.fields
        exclude = ["id", "statement", "author", "created_at", "updated_at", "status"]
        return [field.name for field in fields if field.name not in exclude]


class CreateView(GeneralView, generic.CreateView):
    template_name = "general/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statement"] = Statement.objects.get(pk=self.kwargs["pk"])
        context["model_name"] = self.model._meta.model_name
        context["verbose_name"] = self.model._meta.verbose_name.lower()
        return context

    def form_valid(self, form):
        form.instance.statement = Statement.objects.get(pk=self.kwargs["pk"])
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateView(GeneralView, generic.UpdateView):
    template_name = "general/edit.html"
    template_name_field = "object"

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.author != self.request.user:
            raise PermissionDenied("You can't edit this object")
        if not object.statement.active:
            raise PermissionDenied("You can't edit this object")
        return object

    def get_success_url(self):
        return reverse("statement:detail", kwargs={"pk": self.object.statement.pk})


class DeleteView(generic.DeleteView):

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        if object.author != self.request.user:
            raise PermissionError("You can't delete this object")
        if not object.statement.active:
            raise PermissionError("You can't delete this object")
        return object

    def get_success_url(self):
        return reverse("statement:detail", kwargs={"pk": self.object.statement.pk})
