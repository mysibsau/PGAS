from django.db.transaction import atomic
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView

from .models import Statement


class StatementListView(ListView):
    model = Statement
    context_object_name = "statements"
    template_name = "list.html"
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset().all().order_by("-create_at__year", "create_at__month")
        if self.request.user.is_staff:
            return queryset.select_related("user")
        tmp = queryset.filter(user=self.request.user)
        return [statement for statement in tmp if not statement.active]


class StatementCreateView(CreateView):
    model = Statement
    template_name = "create.html"
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["old_statement"] = Statement.objects.filter(user=self.request.user).last()
        return context

    def get(self, request, *args, **kwargs):
        if statement := Statement.objects.all().filter(user=request.user).current_year().first():
            return redirect("statement:detail", pk=statement.pk)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        result = super().form_valid(form)
        if self.request.POST.get("copy", 'false').lower() == 'true':
            old_statement = Statement.objects.filter(user=self.request.user).exclude(pk=self.object.pk).last()
            for achievements in old_statement.achievements().values():
                for achievement in achievements:
                    print(achievement, achievement.actual, flush=True)
                    if not achievement.actual:
                        continue
                    achievement.pk = None
                    achievement.statement = self.object
                    achievement.save()
        return result

    def get_success_url(self):
        return reverse("statement:detail", kwargs={"pk": self.object.pk})


class StatementDetailView(DetailView):
    template_name = "detail.html"
    context_object_name = "statement"

    def get_queryset(self):
        queryset = Statement.objects.all().prefetch_related(
            "user", "olympiads", "olympiads__documents", "olympiads__comments"
        )
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)


class RatingListView(ListView):
    model = Statement
    context_object_name = "statements"
    template_name = "rating.html"
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset().current_year()
        result = list(sorted(queryset, key=lambda x: x.score, reverse=True))
        for i, statement in enumerate(result):
            statement.is_top = False
            if i <= 0:
                statement.is_top = True

        return result
