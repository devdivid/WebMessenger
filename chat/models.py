from django.conf import settings
from django.db import models


class Conversation(models.Model):

    class ConversationType(models.TextChoices):
        PRIVATE = "PRIVATE", "Private"
        GROUP = "GROUP", "Group"
        CHANNEL = "CHANNEL", "Channel"

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="conversations"
    )

    conversation_type = models.CharField(
        max_length=10,
        choices=ConversationType.choices,
        default=ConversationType.PRIVATE,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_conversation_type_display()} ({self.pk})"


class Message(models.Model):

    class MessageType(models.TextChoices):
        TEXT = "TEXT", "Text"
        IMAGE = "IMAGE", "Image"
        VIDEO = "VIDEO", "Video"
        FILE = "FILE", "File"
        VOICE = "VOICE", "Voice"

    class DeleteStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        DELETED = "DELETED", "Deleted"

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    text = models.TextField(
        blank=True,
        null=True
    )

    message_type = models.CharField(
        max_length=10,
        choices=MessageType.choices,
        default=MessageType.TEXT
    )

    reply_to = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="replies"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    is_edited = models.BooleanField(
        default=False
    )

    delete_status = models.CharField(
        max_length=10,
        choices=DeleteStatus.choices,
        default=DeleteStatus.ACTIVE
    )

    def __str__(self):
        if self.text:
            return f"{self.sender}: {self.text[:30]}"
        return f"{self.sender}: {self.message_type}"
    

class Attachment(models.Model):

    class AttachmentType(models.TextChoices):
        IMAGE = "IMAGE", "Image"
        VIDEO = "VIDEO", "Video"
        FILE = "FILE", "File"
        VOICE = "VOICE", "Voice"

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="attachments"
    )

    file = models.FileField(
        upload_to="messages/"
    )

    attachment_type = models.CharField(
        max_length=10,
        choices=AttachmentType.choices
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.message.id} - {self.attachment_type}"
    
class Reaction(models.Model):

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="reactions"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="message_reactions"
    )

    emoji = models.CharField(
        max_length=10
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "message",
            "user",
        )

    def __str__(self):
        return f"{self.user} - {self.emoji}"