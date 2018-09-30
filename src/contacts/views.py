from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.models import User
from .models import Person


def home(request):
    return render(request, 'contacts/base.html')


class UserContactsListView(ListView):
    model = Person
    template_name = 'contacts/home.html'
    context_object_name = 'persons'
    paginate_by = 5

    def get_queryset(self):
        print('TEST', self.request.user)
        user = get_object_or_404(User, username=self.request.user)
        return Person.objects.filter(creator=user.profile).order_by('last_name')
