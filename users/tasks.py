import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from core.celery import app
from reminders.models import Reminder, ReminderStatuses

logger = logging.getLogger(__name__)
User = get_user_model()


@app.task()
def send_reminder(
    reminder_id: int
):
    reminder = Reminder.objects.get(pk=reminder_id)

    subject = f'Новое напоминание: {reminder.title}'
    all_users = [reminder.author] + list(reminder.users.all())
    body = f'''
        У вас новое напоминание: {reminder.title} \n
        Описание: {reminder.description} \n
        Место: {reminder.place} \n
        Участники: {', '.join([x.username + ' - ' + x.email for x in all_users])} \n
    '''
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_EMAIL_FROM,
            [x.email for x in all_users],
            fail_silently=False,
        )
        reminder.status = ReminderStatuses.sent.value
        logger.info("Отправлено напоминание", extra={'id': reminder_id})
    except Exception:
        logger.error('Ошибка при отправке напоминания', exc_info=True)
        reminder.status = ReminderStatuses.error.value

    reminder.save(update_fields=['status'])
