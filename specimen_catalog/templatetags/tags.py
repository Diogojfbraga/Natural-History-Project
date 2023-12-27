from django import template
from datetime import datetime

register = template.Library()

@register.simple_tag
def current_datetime():
    now = datetime.now()
    formatted_date = now.strftime("%d-%m-%y %H:%M")
    return formatted_date
