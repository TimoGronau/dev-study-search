from django import template
from users.models import Message

register = template.Library()

@register.filter
def unread_messages_count(user):
    return Message.objects.filter(recipient=user.profile, is_read=False).count()
