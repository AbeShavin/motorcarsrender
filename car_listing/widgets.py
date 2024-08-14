# widgets.py
from django.forms.widgets import ClearableFileInput
from django import forms

class MultipleFileInput(forms.ClearableFileInput):
    template_name = 'widgets/multiple_file_input.html'
    
class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

    def format_value(self, value):
        """Return the file list as a list of HTML."""
        if not value:
            return ''
        if isinstance(value, list):
            return [super().format_value(v) for v in value]
        return super().format_value(value)
