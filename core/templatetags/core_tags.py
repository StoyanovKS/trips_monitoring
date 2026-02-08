from django import template

register = template.Library()


@register.filter
def bgn(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value

    formatted = f"{value:,.2f}".replace(",", " ")
    return f"{formatted} лв."


@register.simple_tag(takes_context=True)
def has_group(context, group_name):
    user = context.get("request").user
    if not user or not user.is_authenticated:
        return False

    return user.groups.filter(name=group_name).exists()
