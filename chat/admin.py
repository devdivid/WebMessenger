from django.contrib import admin
from .models import Conversation, Message, Attachment, Reaction

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1

class ReactionInline(admin.TabularInline):
    model = Reaction
    extra = 1
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conversation_type",
        "created_at",
        "last_activity",
    )

    list_filter = (
        "conversation_type",
    )

    search_fields = (
        "id",
    )
    inlines = [
        MessageInline,
    ]



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sender",
        "conversation",
        "message_type",
        "created_at",
        "delete_status",
    )

    list_filter = (
        "message_type",
        "delete_status",
    )

    search_fields = (
        "text",
    )

    inlines = [
        AttachmentInline,
    ]
    inlines = [
    AttachmentInline,
    ReactionInline,
    ]

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "message",
        "user",
        "emoji",
        "created_at",
    )

    list_filter = (
        "emoji",
    )

    search_fields = (
        "user__username",
        "emoji",
    )


