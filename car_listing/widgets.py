# widgets.py
from django.forms.widgets import ClearableFileInput

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

    def format_value(self, value):
        """Return the file list as a list of HTML."""
        if not value:
            return ''
        if isinstance(value, list):
            return [super().format_value(v) for v in value]
        return super().format_value(value)
