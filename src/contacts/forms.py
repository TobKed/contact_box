from django.forms.models import inlineformset_factory
from .models import Person, PhoneNumber, Email


PhoneFormSet = inlineformset_factory(Person, PhoneNumber, fields='__all__', extra=1)
EmailFormSet = inlineformset_factory(Person, Email, fields='__all__', extra=1)
