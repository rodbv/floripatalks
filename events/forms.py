"""
Forms for events app.
"""

from django import forms

from events.models import Event, Topic


class TopicForm(forms.ModelForm):
    """
    Form for creating and editing topics.
    """

    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        required=True,
        widget=forms.HiddenInput(),
        to_field_name="slug",
    )

    class Meta:
        model = Topic
        fields = ["title", "description", "event"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "maxlength": "200",
                    "required": True,
                    "placeholder": "Título do tópico (máximo 200 caracteres)",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "maxlength": "2000",
                    "rows": 5,
                    "placeholder": "Descrição do tópico (opcional, máximo 2000 caracteres)",
                }
            ),
        }
        labels = {
            "title": "Título",
            "description": "Descrição",
        }
        help_texts = {
            "title": "Máximo 200 caracteres",
            "description": "Opcional, máximo 2000 caracteres",
        }

    def clean_title(self) -> str:
        """Validate title field."""
        title = self.cleaned_data.get("title", "").strip()
        if not title:
            raise forms.ValidationError("O título é obrigatório.")
        if len(title) > 200:
            raise forms.ValidationError("O título deve ter no máximo 200 caracteres.")
        return title

    def clean_description(self) -> str:
        """Validate description field."""
        description = self.cleaned_data.get("description", "").strip()
        if description and len(description) > 2000:
            raise forms.ValidationError("A descrição deve ter no máximo 2000 caracteres.")
        return description
