from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    # Check if dictionary is actually a dictionary
    if isinstance(dictionary, dict):
        return dictionary.get(key, [])
    # Otherwise, return an empty list
    return []