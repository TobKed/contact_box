from django.urls import path
from . import views
from .views import (
    PersonListView,
    PersonDetailView,
    PersonCreateView,
    PersonUpdateView
)


urlpatterns = [
    path('', views.home,  name='contacts-home'),
    path('contacts/', PersonListView.as_view(), name='person-list'),
    path('person/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),
    path('person/<int:pk>/update/', PersonUpdateView.as_view(), name='person-update'),
    path('person/new/', PersonCreateView.as_view(), name='person-new'),
]
