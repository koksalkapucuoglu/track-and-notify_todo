from django.db import models
from django.contrib.auth import get_user_model


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
