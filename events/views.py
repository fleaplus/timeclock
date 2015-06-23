from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Event, Period
from .forms import EventForm

from accounts.models import TimeclockUser


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('new_event')

    def get_initial(self):
        """
        Prepopulates date and time with current values for new event creation
        """
        initial = super().get_initial()

        initial['time'] = timezone.now().replace(second=0, microsecond=0)
        return initial

    def form_valid(self, form):
        """
        Sets the user of a new event to the logged in user
        """
        event = form.save(commit=False)
        event.user = TimeclockUser.objects.get(email=self.request.user)
        event.save(billable=form.cleaned_data['billable'])

        return HttpResponseRedirect(self.success_url)


class PeriodIndex(ListView):
    model = Period
