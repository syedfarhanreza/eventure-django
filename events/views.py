from django.db.models import Count, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from .models import Category, Event, Participant
from .forms import EventForm, ParticipantForm, CategoryForm

# -------------------------- CRUD Views ---------------------------

class EventListView(generic.ListView):
    model = Event
    template_name = "events/event_list.html"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            Event.objects.select_related("category")
            .prefetch_related("participants")
        )

        # Text search
        query = self.request.GET.get("q", "").strip()
        if query:
            qs = qs.filter(Q(name__icontains=query) | Q(location__icontains=query))

        # Other filters
        category_id = self.request.GET.get("category")
        start_date = self.request.GET.get("start")
        end_date = self.request.GET.get("end")
        if category_id:
            qs = qs.filter(category_id=category_id)
        if start_date and end_date:
            qs = qs.filter(date__range=[start_date, end_date])
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["object_list"] = ctx["object_list"].annotate(participant_count=Count("participants"))
        return ctx


class EventDetailView(generic.DetailView):
    model = Event
    template_name = "events/event_detail.html"

    def get_queryset(self):
        return Event.objects.select_related("category").prefetch_related("participants")


class EventCreateView(generic.CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"
    success_url = reverse_lazy("events:event-list")


class EventUpdateView(generic.UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"
    success_url = reverse_lazy("events:event-list")


class EventDeleteView(generic.DeleteView):
    model = Event
    template_name = "events/confirm_delete.html"
    success_url = reverse_lazy("events:event-list")


# Participant CRUD -------------------------------------------------
class ParticipantListView(generic.ListView):
    paginate_by = 20

    def get_queryset(self):
        return Participant.objects.annotate(event_total=Count("events")).only("name", "email")
    model = Participant
    template_name = "events/participant_list.html"
    paginate_by = 20


class ParticipantCreateView(generic.CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = "events/participant_form.html"
    success_url = reverse_lazy("events:participant-list")


class ParticipantUpdateView(generic.UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = "events/participant_form.html"
    success_url = reverse_lazy("events:participant-list")


class ParticipantDeleteView(generic.DeleteView):
    model = Participant
    template_name = "events/confirm_delete.html"
    success_url = reverse_lazy("events:participant-list")


# Category CRUD ----------------------------------------------------
class CategoryListView(generic.ListView):
    model = Category
    template_name = "events/category_list.html"


class CategoryCreateView(generic.CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "events/category_form.html"
    success_url = reverse_lazy("events:category-list")


class CategoryUpdateView(generic.UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "events/category_form.html"
    success_url = reverse_lazy("events:category-list")


class CategoryDeleteView(generic.DeleteView):
    model = Category
    template_name = "events/confirm_delete.html"
    success_url = reverse_lazy("events:category-list")


# ------------------------------ Dashboard ------------------------
class OrganizerDashboardView(generic.TemplateView):
    template_name = "events/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()
        base_qs = Event.objects.select_related("category").prefetch_related("participants")
        event_counts = base_qs.aggregate(
            total_events=Count("id"),
            upcoming_events=Count("id", filter=Q(date__gte=today)),
            past_events=Count("id", filter=Q(date__lt=today)),
        )
        ctx.update(event_counts)
        ctx["total_participants"] = Participant.objects.count()
        ctx["todays_events"] = base_qs.filter(date=today)
        # For interactive stats via simple js "filter" param
        stat_filter = self.request.GET.get("filter", "all")
        if stat_filter == "upcoming":
            ctx["filtered_events"] = base_qs.filter(date__gte=today)
        elif stat_filter == "past":
            ctx["filtered_events"] = base_qs.filter(date__lt=today)
        else:
            ctx["filtered_events"] = base_qs

        # Show participants table if requested
        if self.request.GET.get("show") == "participants":
            ctx["participants"] = Participant.objects.annotate(event_total=Count("events")).only("name", "email")
        return ctx


# ------------------------------ Search ---------------------------
class EventSearchView(generic.ListView):
    model = Event
    template_name = "events/event_search.html"

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        return (
            Event.objects.filter(Q(name__icontains=q) | Q(location__icontains=q))
            .select_related("category")
            .prefetch_related("participants")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["object_list"] = ctx["object_list"].annotate(participant_count=Count("participants"))
        ctx["query"] = self.request.GET.get("q", "")
        return ctx