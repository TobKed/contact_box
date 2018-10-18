from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .forms import PhoneFormSet, PhoneFormSetFunc
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

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        phone_form = PhoneFormSet()
        return self.render_to_response(
            self.get_context_data(
                    form=form,
                    phone_form=phone_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        phone_form = PhoneFormSet(self.request.POST)
        if form.is_valid() and phone_form.is_valid():
            return self.form_valid(form, phone_form)
        else:
            return self.form_invalid(form, phone_form)

    def form_valid(self, form, phone_form):
        self.object = form.save(commit=False)
        self.object.creator_id = self.request.user.pk
        self.object = form.save()
        phone_form.instance = self.object
        phone_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, phone_form,):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  phone_form=phone_form))


class PersonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Person
    fields = ['first_name', 'last_name', 'description']


    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # TODO FIXME
        PhoneFormSet = PhoneFormSetFunc(extra=4)
        phone_form = PhoneFormSet(initial=[
             {'number': 123,
              'type': "dom",},
            {'number': 123,
             'type': "dome", },
            {'number': 123,
             'type': "dom", },
            {'number': 123,
             'type': "dom", },
            ])

        return self.render_to_response(
            self.get_context_data(
                    form=form,
                    phone_form=phone_form
            ))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        phone_form = PhoneFormSet(self.request.POST)
        if form.is_valid() and phone_form.is_valid():
            return self.form_valid(form, phone_form)
        else:
            return self.form_invalid(form, phone_form)

    def form_valid(self, form, phone_form):
        self.object = form.save(commit=False)
        self.object.creator_id = self.request.user.pk
        self.object = form.save()
        phone_form.instance = self.object
        phone_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, phone_form,):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  phone_form=phone_form))

    def test_func(self):
        person = self.get_object()
        if self.request.user.pk == person.creator_id:
            return True
        return False


class PersonDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Person
    success_url = '/'

    def test_func(self):
        person = self.get_object()
        if self.request.user.pk == person.creator_id:
            return True
        return False


