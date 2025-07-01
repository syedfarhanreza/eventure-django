from  django.urls import path
from  events.views import show_event

urlpatterns = [
    path('show-event/',show_event)
]
