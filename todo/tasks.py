from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.mail import send_mail
from django.conf import settings

from todo.models import Todo, Notify


logger = get_task_logger(__name__)


@shared_task()
def send_todo_email(notify_id):
    notify = Notify.objects.get(id=notify_id)
    user = notify.user
    status = notify.status

    todos = [
        (todo.title, todo.content)
        for todo in Todo.objects.filter(user=user, status=status)
    ]
    email = notify.user.email

    content = ''
    for todo in todos:
        content += (
            f'\n{todo[0]}\n{todo[1]}\n'
            + '***************************************************************'
        )

    logger.info(
        f"\nemail: {email}"
        f"\n{content}"
    )

    content = content
    subject = f'{notify.title}'
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [notify.user.email]

    return send_mail(
        subject, content, email_from, recipent_list, fail_silently=False
    )
