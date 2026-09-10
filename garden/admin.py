from django.contrib import admin
from .models import Profile, Garden, Plant, GardenPlant, GardenTask, Disease, Fertilizer, Recommendation

admin.site.site_header = 'Smart Garden Administration'
admin.site.site_title = 'Smart Garden Admin'
admin.site.index_title = 'Garden administration'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'phone')
    search_fields = ('user__username', 'user__email', 'city')

@admin.register(Garden)
class GardenAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'location', 'soil_type', 'sunlight', 'size')
    list_filter = ('soil_type', 'sunlight')
    search_fields = ('name', 'location', 'user__username')
    fieldsets = (('Garden basics', {'fields': ('user', 'name', 'location', 'size')}), ('Growing conditions', {'fields': ('soil_type', 'sunlight')}))

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'plant_type', 'suitable_soil', 'sunlight_requirement', 'water_requirement')
    list_filter = ('plant_type', 'suitable_soil', 'sunlight_requirement')
    search_fields = ('name', 'scientific_name', 'plant_type')
    fieldsets = (('Plant identity', {'fields': ('name', 'scientific_name', 'plant_type', 'description')}), ('Best growing conditions', {'fields': ('suitable_soil', 'sunlight_requirement', 'water_requirement', 'suitable_season')}), ('Temperature range in °C', {'fields': ('temperature_min', 'temperature_max')}))

@admin.register(GardenPlant)
class GardenPlantAdmin(admin.ModelAdmin):
    list_display = ('plant', 'garden', 'planted_date', 'status')
    list_filter = ('status', 'garden')
    search_fields = ('plant__name', 'garden__name')

@admin.register(GardenTask)
class GardenTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'garden', 'task_type', 'due_date', 'completed')
    list_filter = ('completed', 'task_type', 'due_date')
    search_fields = ('title', 'garden__name')

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'symptoms')
    search_fields = ('name', 'symptoms')
    fieldsets = (('Disease information', {'fields': ('name', 'symptoms')}), ('Care guidance', {'fields': ('prevention', 'treatment')}))

@admin.register(Fertilizer)
class FertilizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')
    list_filter = ('type',)
    search_fields = ('name', 'type', 'description')
    fieldsets = (('Fertilizer details', {'fields': ('name', 'type', 'description'), 'description': 'Add a simple name and explain what this fertilizer is best used for.'}), ('How gardeners should use it', {'fields': ('instructions',), 'description': 'Write clear application amount, frequency and safety guidance.'}))

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('plant', 'user', 'garden', 'score', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('plant__name', 'user__username', 'garden__name')
    readonly_fields = ('created_at',)
    fieldsets = (('Recommendation', {'fields': ('user', 'garden', 'plant', 'score')}), ('Why it was recommended', {'fields': ('reason',)}), ('Record details', {'fields': ('created_at',)}))
