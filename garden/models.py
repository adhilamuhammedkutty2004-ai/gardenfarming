from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    def __str__(self): return self.user.username

class Garden(models.Model):
    SOIL = [('sandy','Sandy'),('clay','Clay'),('loamy','Loamy'),('silty','Silty')]
    SUN = [('full','Full sun'),('partial','Partial sun'),('shade','Shade')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=255)
    size = models.FloatField(help_text='Square feet')
    soil_type = models.CharField(max_length=50, choices=SOIL)
    sunlight = models.CharField(max_length=50, choices=SUN)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Plant(models.Model):
    name = models.CharField(max_length=150)
    scientific_name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    plant_type = models.CharField(max_length=100)
    suitable_soil = models.CharField(max_length=100)
    sunlight_requirement = models.CharField(max_length=100)
    water_requirement = models.CharField(max_length=100)
    suitable_season = models.CharField(max_length=100)
    temperature_min = models.FloatField(default=18)
    temperature_max = models.FloatField(default=35)
    def __str__(self): return self.name

class GardenPlant(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name='garden_plants')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    planted_date = models.DateField()
    status = models.CharField(max_length=50, default='Healthy')
    notes = models.TextField(blank=True)
    def __str__(self): return f'{self.plant} in {self.garden}'

class GardenTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    task_type = models.CharField(max_length=50, default='Watering')
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    def __str__(self): return self.title

class Disease(models.Model):
    name = models.CharField(max_length=200)
    symptoms = models.TextField()
    prevention = models.TextField()
    treatment = models.TextField()
    def __str__(self): return self.name

class Fertilizer(models.Model):
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=100)
    description = models.TextField()
    instructions = models.TextField()
    def __str__(self): return self.name

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.plant} recommendation for {self.user}'

# Create your models here.
