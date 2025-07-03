from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    # Dashboard
    path("dashboard/", views.OrganizerDashboardView.as_view(), name="dashboard"),

    # Event CRUD & search 
    path("", views.EventListView.as_view(), name="event-list"),
    path("search/", views.EventSearchView.as_view(), name="event-search"),
    path("event/add/", views.EventCreateView.as_view(), name="event-add"),
    path("event/<int:pk>/", views.EventDetailView.as_view(), name="event-detail"),
    path("event/<int:pk>/edit/", views.EventUpdateView.as_view(), name="event-edit"),
    path("event/<int:pk>/delete/", views.EventDeleteView.as_view(), name="event-delete"),

    # Participant CRUD
    path("participants/", views.ParticipantListView.as_view(), name="participant-list"),
    path("participant/add/", views.ParticipantCreateView.as_view(), name="participant-add"),
    path("participant/<int:pk>/edit/", views.ParticipantUpdateView.as_view(), name="participant-edit"),
    path("participant/<int:pk>/delete/", views.ParticipantDeleteView.as_view(), name="participant-delete"),

    # Category CRUD
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("category/add/", views.CategoryCreateView.as_view(), name="category-add"),
    path("category/<int:pk>/edit/", views.CategoryUpdateView.as_view(), name="category-edit"),
    path("category/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category-delete"),
]
