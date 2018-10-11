from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView
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


class PersonDetailView(DetailView):
    model = Person
