from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_percentage_cut(value):
    if value > 100:
        raise ValidationError( _("cannot set a price cut higher than 100%"), params={'value', value} )
