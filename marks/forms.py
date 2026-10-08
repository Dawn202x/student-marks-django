from django import forms
from .models import Mark

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ["name", "subject", "marks"]