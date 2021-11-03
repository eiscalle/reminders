from django.urls import path

from reminders.views import ReminderCreateView, ReminderListView, ReminderUpdateView, ReminderDeleteView, \
    ReminderDetailView, ReminderMarkCompleteView

urlpatterns = [
    path('', ReminderListView.as_view(), name='reminder_list'),
    path('create/', ReminderCreateView.as_view(), name='reminder_create'),
    path('<int:pk>/', ReminderDetailView.as_view(), name='reminder_detail'),
    path('<int:pk>/update/', ReminderUpdateView.as_view(), name='reminder_update'),
    path('<int:pk>/delete/', ReminderDeleteView.as_view(), name='reminder_delete'),
    path('<int:pk>/complete/', ReminderMarkCompleteView.as_view(), name='reminder_mark_complete'),
]
