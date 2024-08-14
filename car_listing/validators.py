# validators.py
import re
from django.core.exceptions import ValidationError

def validate_vin(value):
    if not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', value):
        raise ValidationError('Invalid VIN number.')
