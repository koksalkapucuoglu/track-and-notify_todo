import json

from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

from django_celery_beat.models import CrontabSchedule, PeriodicTask


User = get_user_model()


class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    order = models.PositiveIntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'order'],
            name="user_order_unique")
        ]


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-id']


class Notify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    minute = models.CharField(max_length=20, default='0')
    hour = models.CharField(max_length=20, default='7')
    day_of_month = models.CharField(max_length=20, default='*')
    month_of_year = models.CharField(max_length=20, default='*')
    day_of_week = models.CharField(max_length=20, default='1')
    title = models.CharField(max_length=255, default='Notify my tasks')
    task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    @property
    def get_crontab_schedule(self):
        try:
            crontab_schedule = CrontabSchedule.objects.get(
                                    minute=self.minute,
                                    hour=self.hour,
                                    day_of_week=self.day_of_week,
                                    day_of_month=self.day_of_month,
                                    month_of_year=self.month_of_year,
                                )
        except CrontabSchedule.DoesNotExist:
            crontab_schedule = CrontabSchedule.objects.create(
                minute=self.minute,
                hour=self.hour,
                day_of_week=self.day_of_week,
                day_of_month=self.day_of_month,
                month_of_year=self.month_of_year,
            )
        return crontab_schedule

    def delete(self, *args, **kwargs):
        if self.task is not None:
            self.task.delete()

        return super(self.__class__, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.task is None:
            self._create_periodic_task()

    def _create_periodic_task(self):
        notify = Notify.objects.get(id=self.id)
        notify.task = PeriodicTask.objects.create(
            name=f'{self.title}-{self.id}',
            task='todo.tasks.send_todo_email',
            crontab=self.get_crontab_schedule,
            kwargs=json.dumps({"notify_id": self.id}),
            start_time=timezone.now()
        )
        notify.save()
