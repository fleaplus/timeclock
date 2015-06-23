from django.forms import ModelForm, SplitDateTimeField, BooleanField, MultiWidget, DateInput, TimeInput
from django.forms.utils import to_current_timezone

from .models import Event


class UikitSplitDateTimeWidget(MultiWidget):
    """
    A custom SplitDateTimeWidget that adds Uikit attributes to its fields.
    """
    supports_microseconds = False

    def __init__(self, attrs={}, date_format=None, time_format=None):
        widgets = (DateInput(attrs=dict({'data-uk-datepicker': "{format:'YYYY-MM-DD'}", 'class': 'uk-form-large uk-form-width-small'}, **attrs), format=date_format),
                   TimeInput(attrs=dict({'data-uk-timepicker': "", 'class': 'uk-form-large uk-form-width-small'}, **attrs), format='%H:%M'))
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            return [value.date(), value.time()]
        return [None, None]


class EventForm(ModelForm):
    time = SplitDateTimeField(widget=UikitSplitDateTimeWidget)
    billable = BooleanField(required=False, initial=True)

    class Meta:
        model = Event
        fields = ['time', 'billable']
