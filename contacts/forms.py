from django.forms.models import inlineformset_factory
from .models import Person, PhoneNumber


PhoneFormSet = inlineformset_factory(Person, PhoneNumber, fields=['number', 'type'], extra=1)
