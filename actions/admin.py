from django.contrib import admin
from actions.models import Action

# Register your models here.

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("user","verb","target","created")
    search_fields = ("verb",)



