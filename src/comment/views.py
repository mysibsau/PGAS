from django.db.models import Q
from django.urls import reverse
from django.views.generic import CreateView, ListView
from login_required import LoginNotRequiredMixin

from .models import Comment


class CommentCreateView(CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        class_name = self.request.POST['object_name']
        result = super().form_valid(form)
        achievement = getattr(self.object, f'{class_name}_set').model.objects.get(pk=self.request.POST['object_pk'])
        if achievement.author != self.request.user:
            achievement.author.notify(
                f'К вашему достижению "{achievement.name}" был добавлен комментарий: "{self.object.text}"',
            )
        getattr(self.object, f'{class_name}_set').add(self.request.POST['object_pk'])
        return result

    def get_success_url(self):
        statement = self.request.POST['statement']

        return reverse('statement:detail', kwargs={'pk': statement})


class ListCommentsViews(ListView, LoginNotRequiredMixin):
    model = Comment
    context_object_name = 'comments'

    def get_queryset(self):
        all_fields = Comment._meta.get_fields()
        query = Q()
        for f in all_fields:
            if f.is_relation:
                query |= Q(**{f.name: self.kwargs['pk']})
        return Comment.objects.filter(query)
