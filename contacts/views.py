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
from .forms import PhoneFormSet, EmailFormSet
from .models import Person, Address, ContactGroup
from django.db.models import Count


def home(request):
    return render(request, 'contacts/home.html')


def is_user_a_creator(obj):
    """  function used in test_func() is views which inherits UserPassesTestMixin """
    person = obj.get_object()
    if obj.request.user.pk == person.creator_id:
        return True
    return False


class PersonListView(LoginRequiredMixin, ListView):
    model = Person
    context_object_name = 'persons'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        orderby = self.request.GET.get('orderby', 'last_name')
        order = self.request.GET.get('order', 'asc')
        order = {'asc': '', 'desc': '-'}.get(order, '')
        return Person.objects.filter(creator=user.profile).order_by(order+orderby)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        params = {
            'orderby': self.request.GET.get('orderby', 'last_name'),
            'order': self.request.GET.get('order', 'asc')
        }
        context_data.update(params)
        return context_data


class PersonDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Person

    def test_func(self):
        return is_user_a_creator(self)


class PersonCreateView(LoginRequiredMixin, CreateView):
    model = Person
    fields = ['first_name', 'last_name', 'description', 'address', 'groups']

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['address'].queryset = Address.objects.filter(creator=self.request.user.pk)
        form.fields['groups'].queryset = ContactGroup.objects.filter(creator=self.request.user.pk)
        return form

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        phone_form = PhoneFormSet()
        email_form = EmailFormSet()
        return self.render_to_response(
            self.get_context_data(
                    form=form,
                    phone_form=phone_form,
                    email_form=email_form))

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
        email_form = EmailFormSet(self.request.POST)
        if form.is_valid() and phone_form.is_valid() and email_form.is_valid():
            return self.form_valid(form, phone_form, email_form)
        else:
            return self.form_invalid(form, phone_form, email_form)

    def form_valid(self, form, phone_form, email_form):
        self.object = form.save(commit=False)
        self.object.creator_id = self.request.user.pk
        self.object = form.save()
        phone_form.instance = self.object
        phone_form.save()
        email_form.instance = self.object
        email_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, phone_form, email_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  phone_form=phone_form,
                                  email_form=email_form))


class PersonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Person
    fields = ['first_name', 'last_name', 'description', 'address', 'groups']

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['address'].queryset = Address.objects.filter(creator=self.request.user.pk)
        form.fields['groups'].queryset = ContactGroup.objects.filter(creator=self.request.user.pk)
        return form

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        phone_form = PhoneFormSet(instance=self.object)
        email_form = EmailFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(
                    form=form,
                    phone_form=phone_form,
                    email_form=email_form
            ))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        phone_form = PhoneFormSet(self.request.POST, instance=self.object)
        email_form = EmailFormSet(self.request.POST, instance=self.object)
        if form.is_valid() and phone_form.is_valid() and email_form.is_valid():
            return self.form_valid(form, phone_form, email_form)
        else:
            return self.form_invalid(form, phone_form, email_form)

    def form_valid(self, form, phone_form, email_form):
        self.object = form.save(commit=False)
        self.object.creator_id = self.request.user.pk
        self.object = form.save()
        phone_form.instance = self.object
        phone_form.save()
        email_form.instance = self.object
        email_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, phone_form, email_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  phone_form=phone_form,
                                  email_form=email_form))

    def test_func(self):
        return is_user_a_creator(self)


class PersonDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Person
    success_url = '/'

    def test_func(self):
        return is_user_a_creator(self)


class AddressListView(LoginRequiredMixin, ListView):
    model = Address
    context_object_name = 'addresses'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        orderby = self.request.GET.get('orderby', 'city')
        order = self.request.GET.get('order', 'asc')
        order = {'asc': '', 'desc': '-'}.get(order, '')
        return Address.objects.filter(creator=user.profile).annotate(
            inhabitants=Count('person', distinct=True)
            ).order_by(order+orderby)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        params = {
            'orderby': self.request.GET.get('orderby', 'city'),
            'order': self.request.GET.get('order', 'asc')
        }
        context_data.update(params)
        return context_data


class AddressDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Address

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data.update({
            'inhabitants': Person.objects.filter(address=self.get_object())
        })
        return context_data

    def test_func(self):
        address = self.get_object()
        if self.request.user.pk == address.creator_id:
            return True
        return False


class AddressDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Address
    success_url = '/'

    def test_func(self):
        return is_user_a_creator(self)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    fields = ['city', 'street', 'building_number', 'flat_number']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator_id = self.request.user.pk
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class AddressUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Address
    fields = ['city', 'street', 'building_number', 'flat_number']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator_id = self.request.user.pk
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        return is_user_a_creator(self)


class ContactGroupListView(LoginRequiredMixin, ListView):
    model = ContactGroup
    context_object_name = 'groups'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        orderby = self.request.GET.get('orderby', 'name')
        order = self.request.GET.get('order', 'asc')
        order = {'asc': '', 'desc': '-'}.get(order, '')
        return ContactGroup.objects.filter(creator=user.profile).annotate(
            members=Count('person', distinct=True)
            ).order_by(order+orderby)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        params = {
            'orderby': self.request.GET.get('orderby', 'name'),
            'order': self.request.GET.get('order', 'asc')
        }
        context_data.update(params)
        return context_data


class ContactGroupDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ContactGroup

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        group = self.get_object()
        context_data.update({
            'members': group.person_set.all()
        })
        return context_data

    def test_func(self):
        return is_user_a_creator(self)


class ContactGroupDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ContactGroup
    success_url = '/'

    def test_func(self):
        return is_user_a_creator(self)


class ContactGroupCreateView(LoginRequiredMixin, CreateView):
    model = ContactGroup
    fields = ['name', 'description']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator_id = self.request.user.pk
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class ContactGroupUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ContactGroup
    fields = ['name', 'description']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator_id = self.request.user.pk
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        return is_user_a_creator(self)
