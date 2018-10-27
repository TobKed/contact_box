from django.urls import path
from . import views
from .views import (
    PersonListView,
    PersonDetailView,
    PersonCreateView,
    PersonUpdateView,
    PersonDeleteView,

    AddressListView,
    AddressDetailView,
    AddressCreateView,
    AddressUpdateView,
    AddressDeleteView,

    ContactGroupListView,
    ContactGroupDetailView,
    ContactGroupCreateView,
    ContactGroupUpdateView,
    ContactGroupDeleteView,
)


urlpatterns = [
    path('', views.home,  name='contacts-home'),
    path('contacts/', PersonListView.as_view(), name='person-list'),
    path('person/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),
    path('person/<int:pk>/update/', PersonUpdateView.as_view(), name='person-update'),
    path('person/<int:pk>/delete/', PersonDeleteView.as_view(), name='person-delete'),
    path('person/new/', PersonCreateView.as_view(), name='person-new'),
    
    path('contacts/address', AddressListView.as_view(), name='address-list'),
    path('contacts/address/<int:pk>/', AddressDetailView.as_view(), name='address-detail'),
    path('contacts/address/<int:pk>/update/', AddressUpdateView.as_view(), name='address-update'),
    path('contacts/address/<int:pk>/delete/', AddressDeleteView.as_view(), name='address-delete'),
    path('contacts/address/new/', AddressCreateView.as_view(), name='address-new'),
    
    path('contacts/group', ContactGroupListView.as_view(), name='group-list'),
    path('contacts/group/<int:pk>/', ContactGroupDetailView.as_view(), name='group-detail'),
    path('contacts/group/<int:pk>/update/', ContactGroupUpdateView.as_view(), name='group-update'),
    path('contacts/group/<int:pk>/delete/', ContactGroupDeleteView.as_view(), name='group-delete'),
    path('contacts/group/new/', ContactGroupCreateView.as_view(), name='group-new'),
]
