from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try to get properties from Redis cache
    properties = cache.get('all_properties')
    if not properties:
        # If not found in cache, fetch from DB
        properties = Property.objects.all()
        # Store queryset in cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    return properties
