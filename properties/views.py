from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)  # still cache the full response for 15 min
def property_list(request):
    properties = get_all_properties()
    return render(request, "properties/property_list.html", {"properties": properties})
