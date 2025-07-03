from django import forms

from .models import Event, Participant, Category


class TailwindModelForm(forms.ModelForm):
    """Base form that injects Tailwind classes into widgets."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (
                f"{css} bg-gray-800 border border-gray-600 rounded w-full px-3 py-2 text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-teal-500"
            )


class EventForm(TailwindModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "date",
            "time",
            "location",
            "category",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }


class ParticipantForm(TailwindModelForm):
    class Meta:
        model = Participant
        fields = ["name", "email", "events"]
        widgets = {
            "events": forms.CheckboxSelectMultiple(),
        }


class CategoryForm(TailwindModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}
