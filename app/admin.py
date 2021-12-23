from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Category, Event, PopularCategory
from .forms import CategoryForm


class CategoryAdmin(admin.ModelAdmin):
   form = CategoryForm
admin.site.register(Category, CategoryAdmin)


class PopularCategoryAdmin(admin.ModelAdmin):
   def has_add_permission(self, request):
      num_objects = self.model.objects.count()
      return num_objects == 0
   def get_actions(self, request):
      actions = super().get_actions(request)
      if 'delete_selected' in actions:
         del actions['delete_selected']
      return actions
admin.site.register(PopularCategory, PopularCategoryAdmin)


class EventAdmin(admin.ModelAdmin):
   fields = (
      'name', 'description', 'time', ('people_required', 'people_joined'),
      'place', 'price', 'categories', 'creator',
   )
admin.site.register(Event, EventAdmin)