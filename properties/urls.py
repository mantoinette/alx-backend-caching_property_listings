from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """Fetch all properties, using Redis cache."""
    properties = cache.get('all_properties')
    if not properties:
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)  # cache for 1 hour
    return properties


def get_redis_cache_metrics():
    """Get Redis keyspace hits, misses, and hit ratio."""
    try:
        # Get raw Redis client from django-redis
        redis_client = cache.client.get_client()
        info = redis_client.info("stats")  # fetch Redis stats

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses
        hit_ratio = (hits / total) if total > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio
        }

        logger.info(f"Redis cache metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error fetching Redis metrics: {e}")
        return {"hits": 0, "misses": 0, "hit_ratio": 0}
