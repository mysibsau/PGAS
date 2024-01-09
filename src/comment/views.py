from django.urls import reverse
from django.views.generic import CreateView

from .models import Comment


class CommentCreateView(CreateView):
    model = Comment
    fields = ["text"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        class_name = self.request.POST['object_name']
        result = super().form_valid(form)
        getattr(self.object, f"{class_name}_set").add(self.request.POST['object_pk'])
        return result

    def get_success_url(self):
        statement = self.request.POST['statement']

        return reverse("statement:detail", kwargs={"pk": statement})
