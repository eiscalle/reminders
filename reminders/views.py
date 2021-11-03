from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.views.generic.detail import SingleObjectMixin

from reminders.forms import ReminderCreateForm, ReminderUpdateForm
from reminders.models import Reminder, ReminderStatuses
from users.tasks import send_reminder


class ReminderListView(LoginRequiredMixin, ListView):
    model = Reminder
    template_name = 'reminders/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        qs = qs.filter(Q(author=user) | Q(users=user))
        return qs


class ReminderDetailView(LoginRequiredMixin, DetailView):
    model = Reminder
    template_name = 'reminders/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        qs = qs.filter(Q(author=user) | Q(users=user))
        return qs


class ReminderCreateView(LoginRequiredMixin, CreateView):
    model = Reminder
    form_class = ReminderCreateForm
    template_name = 'base_form.html'
    success_url = reverse_lazy('reminder_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        task_id = send_reminder.apply_async([self.object.pk], eta=self.object.publish_at)
        self.object.task_id = task_id
        self.object.save(update_fields=['task_id'])
        return response


class ReminderUpdateView(LoginRequiredMixin, UpdateView):
    model = Reminder
    form_class = ReminderUpdateForm
    template_name = 'base_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('reminder_detail', args=[self.object.pk])

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.revoke_task()
        task_id = send_reminder.apply_async([self.object.pk], eta=self.object.publish_at)
        self.object.task_id = task_id
        self.object.save(update_fields=['task_id'])
        return response


class ReminderDeleteView(LoginRequiredMixin, DeleteView):
    model = Reminder
    success_url = reverse_lazy('reminder_list')
    template_name = 'reminders/delete.html'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        self.object.revoke_task()
        return super().get_success_url()


class ReminderMarkCompleteView(LoginRequiredMixin, SingleObjectMixin, View):
    http_method_names = ['post']
    model = Reminder

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.revoke_task()
        self.object.status = ReminderStatuses.sent.value
        self.object.save(update_fields=['status'])
        return HttpResponseRedirect(reverse('reminder_detail', args=[self.object.pk]))
