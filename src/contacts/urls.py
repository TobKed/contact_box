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
    AddressDeleteView
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
    path('contacts/address//<int:pk>/delete/', AddressDeleteView.as_view(), name='address-delete'),
]
