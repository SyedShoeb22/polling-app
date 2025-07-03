# polls/forms.py
from django import forms

class PollGenerateForm(forms.Form):
    topics = forms.CharField(
        help_text="Comma-separated list, e.g. Python, OOP, Django",
        widget=forms.TextInput(attrs={"placeholder": "topic1, topic2, …"}),
    )
    n_questions  = forms.IntegerField(min_value=1, max_value=10, initial=3)
