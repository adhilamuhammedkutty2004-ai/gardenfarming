from datetime import date
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Garden, Plant, GardenPlant, GardenTask, Disease, Fertilizer
from .forms import RegisterForm, GardenForm, GardenPlantForm, TaskForm, EmailOrUsernameAuthenticationForm, PlantCatalogForm, DiseaseForm, FertilizerForm

def home(request): return render(request, 'home.html')

def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(); user.email = form.cleaned_data['email']; user.save(); login(request, user); return redirect('dashboard')
    return render(request, 'form.html', {'form':form, 'title':'Create your Smart Garden account', 'button':'Register', 'is_registration':True})

class GardenLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = EmailOrUsernameAuthenticationForm

@login_required
def dashboard(request):
    gps = GardenPlant.objects.filter(garden__user=request.user)
    tasks = GardenTask.objects.filter(user=request.user).order_by('completed','due_date')[:5]
    return render(request, 'dashboard.html', {'plants':gps, 'tasks':tasks, 'healthy':gps.filter(status='Healthy').count(), 'attention':gps.exclude(status='Healthy').count()})

@login_required
def gardens(request): return render(request, 'gardens.html', {'gardens':Garden.objects.filter(user=request.user)})
@login_required
def garden_add(request):
    form=GardenForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        g=form.save(commit=False); g.user=request.user; g.save()
        return redirect(request.GET.get('next') or 'gardens')
    return render(request,'form.html',{'form':form,'title':'Add a garden','button':'Save garden'})
def plants(request):
    q=request.GET.get('q',''); items=Plant.objects.filter(Q(name__icontains=q)|Q(plant_type__icontains=q)) if q else Plant.objects.all()
    return render(request,'plants.html',{'plants':items,'q':q})
@login_required
def plant_add(request):
    user_gardens = Garden.objects.filter(user=request.user)
    if not user_gardens.exists():
        return redirect('/gardens/add/?next=plant_add')
    form=GardenPlantForm(request.POST or None); form.fields['garden'].queryset=user_gardens
    if request.method=='POST' and form.is_valid(): form.save(); return redirect('dashboard')
    return render(request,'form.html',{'form':form,'title':'Add a plant to your garden','button':'Add plant'})
@login_required
def recommendations(request):
    garden=Garden.objects.filter(user=request.user).first(); result=[]
    if garden:
        for p in Plant.objects.all():
            score=30*(p.suitable_soil.lower()==garden.soil_type)+25*(garden.sunlight in p.sunlight_requirement.lower())+20
            if score>=50: result.append((p, min(score+15,98)))
        result.sort(key=lambda x:x[1], reverse=True)
    return render(request,'recommendations.html',{'garden':garden,'recommendations':result})
@login_required
def disease_detection(request):
    result = 'Tomato Early Blight' if request.method=='POST' else None
    return render(request,'disease.html',{'result':result})
@login_required
def watering(request): return render(request,'advisory.html',{'title':'Smart Watering Advisory','icon':'💧','headline':'Water moderately today','amount':'1.5 litres per plant','detail':'Rain is possible tomorrow, so reduce the usual amount by half. Water early, at 6:00–8:00 AM.'})
@login_required
def fertilizer(request): return render(request,'advisory.html',{'title':'Fertilizer & Nutrient Advisory','icon':'🌿','headline':'NPK 5-10-10 recommended','amount':'25 g per plant','detail':'Apply every 14 days during flowering. Water the soil after application and avoid over-fertilizing.'})
@login_required
def weather(request): return render(request,'weather.html')
@login_required
def tasks(request): return render(request,'tasks.html',{'tasks':GardenTask.objects.filter(user=request.user).order_by('completed','due_date')})
@login_required
def task_add(request):
    form=TaskForm(request.POST or None); form.fields['garden'].queryset=Garden.objects.filter(user=request.user)
    if request.method=='POST' and form.is_valid(): t=form.save(commit=False); t.user=request.user; t.save(); return redirect('tasks')
    return render(request,'form.html',{'form':form,'title':'Schedule a garden task','button':'Add task'})
@login_required
def complete_task(request,pk):
    task=GardenTask.objects.get(pk=pk,user=request.user); task.completed=True; task.save(); return redirect('tasks')
@login_required
def assistant(request):
    question=request.POST.get('question',''); answer='Ask me about watering, yellow leaves, soil, pests, or plant care.'
    if question:
        q=question.lower(); answer='Yellow leaves can be caused by overwatering, poor drainage, nutrient deficiency, or disease. Check soil moisture first and inspect leaves for spots.' if 'yellow' in q else 'Keep soil evenly moist, give the plant enough sunlight, and check leaves weekly for pests. I can help you make a care plan.'
    return render(request,'assistant.html',{'question':question,'answer':answer})
@login_required
def reports(request):
    total=GardenPlant.objects.filter(garden__user=request.user).count(); complete=GardenTask.objects.filter(user=request.user,completed=True).count(); pending=GardenTask.objects.filter(user=request.user,completed=False).count()
    return render(request,'reports.html',{'total':total,'healthy':GardenPlant.objects.filter(garden__user=request.user,status='Healthy').count(),'complete':complete,'pending':pending})

staff_only = user_passes_test(lambda user: user.is_staff)

@staff_only
def garden_manager(request):
    return render(request, 'garden_manager.html', {'stats': {'users': __import__('django.contrib.auth.models', fromlist=['User']).User.objects.count(), 'plants': Plant.objects.count(), 'diseases': Disease.objects.count(), 'fertilizers': Fertilizer.objects.count(), 'tasks': GardenTask.objects.filter(completed=False).count()}})

@staff_only
def manager_collection(request, kind):
    options = {
        'plants': (Plant, PlantCatalogForm, 'Plant library', 'Add a plant', ('name', 'plant_type', 'suitable_soil')),
        'diseases': (Disease, DiseaseForm, 'Disease advice', 'Add disease advice', ('name', 'symptoms')),
        'fertilizers': (Fertilizer, FertilizerForm, 'Fertilizer guide', 'Add a fertilizer', ('name', 'type', 'description')),
    }
    if kind not in options: return redirect('garden_manager')
    model, form_class, title, button, columns = options[kind]
    form = form_class(request.POST or None)
    if request.method == 'POST' and form.is_valid(): form.save(); return redirect('manager_collection', kind=kind)
    return render(request, 'manager_collection.html', {'form': form, 'items': model.objects.all().order_by('name'), 'title': title, 'button': button, 'columns': columns, 'kind': kind})
