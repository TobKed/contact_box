from django.forms.models import inlineformset_factory
from .models import Person, PhoneNumber, Email


PhoneFormSet = inlineformset_factory(Person, PhoneNumber, fields=['number', 'type'], extra=1)
EmailFormSet = inlineformset_factory(Person, Email, fields=['address', 'type'], extra=1)
