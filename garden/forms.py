from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Garden, GardenPlant, GardenTask, Plant, Disease, Fertilizer

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label='Full name', required=False)

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['username'].widget.attrs.pop('maxlength', None)
        if 'password1' in self.fields:
            self.fields['password1'].help_text = ''
        if 'password2' in self.fields:
            self.fields['password2'].help_text = ''

    def clean_username(self):
        username = (self.cleaned_data.get('username') or '').strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return username

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with that email already exists.')
        return email

class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['username'].widget.attrs.pop('maxlength', None)

    def clean(self):
        identifier = (self.cleaned_data.get('username') or '').strip()
        if identifier:
            if '@' in identifier:
                user = User.objects.filter(email__iexact=identifier).first()
            else:
                user = User.objects.filter(username__iexact=identifier).first()
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
