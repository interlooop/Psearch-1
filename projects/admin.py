from django.contrib import admin

# Register your models here.
from .models import Project,Review,Tag,Category

admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields ={'slug':('name',)}