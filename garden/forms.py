from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Garden, GardenPlant, GardenTask, Plant, Disease, Fertilizer

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(label='Full name')
    class Meta:
        model = User
        fields = ('first_name','username','email','password1','password2')

class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or email')
    def clean(self):
        identifier = self.cleaned_data.get('username')
        if identifier and '@' in identifier:
            user = User.objects.filter(email__iexact=identifier).first()
            if user:
                self.cleaned_data['username'] = user.username
        return super().clean()

class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = ('name','location','size','soil_type','sunlight')

class GardenPlantForm(forms.ModelForm):
    class Meta:
        model = GardenPlant
        fields = ('garden','plant','planted_date','status','notes')

class TaskForm(forms.ModelForm):
    class Meta:
        model = GardenTask
        fields = ('garden','title','task_type','due_date')
        widgets = {'due_date': forms.DateInput(attrs={'type':'date'})}

class PlantCatalogForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ('name', 'scientific_name', 'plant_type', 'description', 'suitable_soil', 'sunlight_requirement', 'water_requirement', 'suitable_season', 'temperature_min', 'temperature_max')

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ('name', 'symptoms', 'prevention', 'treatment')

class FertilizerForm(forms.ModelForm):
    class Meta:
        model = Fertilizer
        fields = ('name', 'type', 'description', 'instructions')
