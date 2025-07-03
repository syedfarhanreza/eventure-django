from django.db import models

# Create your models here.

class Category(models.Model):
    """Represents a category of events (e.g. Conference, Workshop)."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Event(models.Model):
    """Represents an event organised by the platform."""
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    # Using DateField and TimeField to keep them separate as required
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events")

    class Meta:
        ordering = ["-date", "time"]
        indexes = [
            models.Index(fields=["date"]),
            models.Index(fields=["category", "date"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.date})"

    @property
    def is_past(self):
        """Returns True if the event has already happened."""
        from django.utils import timezone

        return timezone.now().date() > self.date


class Participant(models.Model):
    """Individual who can register for one or many events."""
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    events = models.ManyToManyField(Event, related_name="participants", blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} <{self.email}>"
