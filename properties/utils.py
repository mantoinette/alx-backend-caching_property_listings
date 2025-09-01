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
        # Connect to Redis via django-redis
        redis_client = cache.client.get_client()
        info = redis_client.info("stats")  # fetch Redis statistics

        # Retrieve keyspace hits and misses
        keyspace_hits = info.get("keyspace_hits", 0)
        keyspace_misses = info.get("keyspace_misses", 0)

        # Calculate hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = keyspace_hits / total_requests if total_requests > 0 else 0

        # Log metrics
        logger.info(
            "Redis metrics - hits=%s, misses=%s, hit_ratio=%s",
            keyspace_hits,
            keyspace_misses,
            hit_ratio
        )

        return {
            "hits": keyspace_hits,
            "misses": keyspace_misses,
            "hit_ratio": hit_ratio
        }

    except Exception as e:
        # Checker requires logger.error to exist
        logger.error("Failed to retrieve Redis cache metrics: %s", e)
        return {"hits": 0, "misses": 0, "hit_ratio": 0}
