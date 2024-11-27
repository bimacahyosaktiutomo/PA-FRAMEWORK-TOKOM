from django import template

register = template.Library()

@register.filter
def to(value, arg):
    """Return a range from value to arg"""
    return range(value, arg + 1)  # Adjusted to handle inclusive ranges

@register.filter
def get_percentage(rating_distribution, rating):
    total_reviews = sum(rating_distribution.values())
    if total_reviews == 0:
        return 0
    return (rating_distribution.get(rating, 0) / total_reviews) * 100

@register.filter
def get_count(rating_distribution, rating):
    return rating_distribution.get(rating, 0)
