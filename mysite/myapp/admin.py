from django.contrib import admin
from .models import Location,Database,Random,Neworder_database
# Register your models here.
admin.site.register(Location)
admin.site.register(Database)
admin.site.register(Random)
admin.site.register(Neworder_database)