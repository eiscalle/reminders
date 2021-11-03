import pytz
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.conf import settings
from django.contrib.auth import get_user_model

from reminders.models import Reminder


User = get_user_model()


class ReminderManyToManyChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, instance):
        return f'{instance.username} - {instance.email}'


class ReminderCreateForm(forms.ModelForm):
    users = ReminderManyToManyChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Участники'
    )

    class Meta:
        model = Reminder
        fields = ('title', 'description', 'place', 'users', 'publish_at')
        widgets = {
            'publish_at': forms.TextInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.exclude(pk=user.pk)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Создать'))


class ReminderUpdateForm(ReminderCreateForm):

    class Meta(ReminderCreateForm.Meta):
        model = Reminder
        fields = ('title', 'description', 'place', 'users', 'publish_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tz = pytz.timezone(settings.TIME_ZONE)
        self.initial['publish_at'] = self.instance.publish_at.astimezone(tz).\
            strftime('%Y-%m-%dT%H:%M:%S')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Обновить'))
