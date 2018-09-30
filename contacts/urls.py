from django.urls import path
from . import views
from .views import UserContactsListView


urlpatterns = [
    path('', views.home,  name='contacts-home'),
    path('contacts/', UserContactsListView.as_view(),  name='contacts-user-contacts'),
]
