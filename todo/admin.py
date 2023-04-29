from django.contrib import admin

from todo.models import Todo, Status, Notify


class NotifyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'status'
    )
    list_select_related = ('user', 'status', 'task',)
    search_fields = ('title',)
    list_filter = (
        "user__email",
        "task__last_run_at"
    )


admin.site.register(Todo)
admin.site.register(Status)
admin.site.register(Notify, NotifyAdmin)
