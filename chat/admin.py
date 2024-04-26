# admin.py
from django.contrib import admin
from .models import Thread, Message


class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "participants_list", "created", "updated")

    def participants_list(self, obj):
        return ", ".join([str(user) for user in obj.participants.all()])

    participants_list.short_description = "Participants"


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "thread", "text", "created", "is_read")
    list_filter = ("thread",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sender":
            kwargs["queryset"] = db_field.remote_field.model.objects.filter(
                thread=request.GET.get("thread_id")
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)
