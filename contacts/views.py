from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from .models import Person


def home(request):
    return render(request, 'contacts/base.html')


class PersonListView(LoginRequiredMixin, ListView):
    model = Person
    context_object_name = 'persons'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Person.objects.filter(creator=user.profile).order_by('last_name')


class PersonDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Person

    def test_func(self):
        person = self.get_object()
        if self.request.user.pk == person.creator_id:
            return True
        return False


class PersonCreateView(LoginRequiredMixin, CreateView):
    model = Person
    fields = ['first_name', 'last_name', 'description']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator_id = self.request.user.pk
        return super().form_valid(form)


class PersonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Person
    fields = ['first_name', 'last_name', 'description']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator_id = self.request.user.pk
        return super().form_valid(form)

    def test_func(self):
        person = self.get_object()
        if self.request.user.pk == person.creator_id:
            return True
        return False
