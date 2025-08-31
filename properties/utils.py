from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    properties = cache.get('all_properties')
    if not properties:
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)
    return properties


def get_redis_cache_metrics():
    """Get Redis keyspace hits, misses, and hit ratio."""
    # Connect to Redis
    redis_client = cache.client.get_client()
    info = redis_client.info("stats")

    # Retrieve hits and misses
    keyspace_hits = info.get("keyspace_hits", 0)
    keyspace_misses = info.get("keyspace_misses", 0)

    # Calculate hit ratio
    total_requests = keyspace_hits + keyspace_misses
    hit_ratio = keyspace_hits / total_requests if total_requests > 0 else 0

    # Log metrics
    logger.info(f"Redis metrics - hits: {keyspace_hits}, misses: {keyspace_misses}, hit_ratio: {hit_ratio}")

    # Return dictionary
    return {
        "hits": keyspace_hits,
        "misses": keyspace_misses,
        "hit_ratio": hit_ratio
    }
