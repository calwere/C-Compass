

# Register your models here.
from django.contrib import admin
from .models import House, Amenity, Agent, SearchHistory, Mover

admin.site.register(House)
admin.site.register(Amenity)
admin.site.register(Agent)
admin.site.register(SearchHistory)
admin.site.register(Mover)
