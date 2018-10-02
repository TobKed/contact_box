from django.urls import path
from . import views
from .views import UserContactsListView, PersonDetailView


urlpatterns = [
    path('', views.home,  name='contacts-home'),
    path('contacts/', UserContactsListView.as_view(),  name='contacts'),
    path('person/<int:pk>/', PersonDetailView.as_view(), name='person-detail')
]
