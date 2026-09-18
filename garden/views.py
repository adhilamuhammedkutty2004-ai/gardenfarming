from datetime import date
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Profile, Garden, Plant, GardenPlant, GardenTask, Disease, Fertilizer
from .forms import RegisterForm, GardenForm, GardenPlantForm, TaskForm, EmailOrUsernameAuthenticationForm, PlantCatalogForm, DiseaseForm, FertilizerForm

def home(request): return render(request, 'home.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.email = form.cleaned_data['email']
        user.first_name = form.cleaned_data.get('first_name', '')
        user.save()
        Profile.objects.get_or_create(user=user)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'form.html', {'form':form, 'title':'Create your Smart Garden account', 'button':'Register', 'is_registration':True})

class GardenLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = EmailOrUsernameAuthenticationForm

    def get_success_url(self):
        next_url = self.get_redirect_url()
        if self.request.user.is_staff or self.request.user.is_superuser:
            if next_url and next_url != '/dashboard/':
                return next_url
            return '/admin/'
        return next_url or '/dashboard/'

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
def get_assistant_response(question, user):
    q = question.strip().lower()

    # 1. Greetings & Pleasantries
    greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'howdy', 'hola', 'namaste']
    if any(q == g or q.startswith(g + ' ') or q.startswith(g + '!') or q.startswith(g + ',') for g in greetings):
        name = f" {user.first_name}" if user.is_authenticated and user.first_name else ""
        return (
            f"Hello{name}! 🌿 I am your Smart Garden Assistant.\n\n"
            "How can I help you today? You can ask me about:\n"
            "• Specific plants (e.g. 'How to grow tomatoes' or 'Tell me about mint')\n"
            "• Watering schedules & sunlight requirements\n"
            "• Soil preparation (loamy, sandy, clay) & fertilizers\n"
            "• Plant health (e.g. 'Why are leaves yellow?' or 'Early blight treatment')\n"
            "• Your current gardens and tasks (try 'Check my garden')"
        )

    # 2. Gratitude & Farewells
    if any(w in q for w in ['thank', 'thanks', 'thx', 'appreciate', 'bye', 'goodbye']):
        return "You're very welcome! 🌱 Keep your garden thriving, and feel free to reach out anytime you need more tips!"

    # 3. Assistant Identity
    if any(phrase in q for phrase in ['who are you', 'what are you', 'what can you do', 'help', 'features']):
        return (
            "I'm your intelligent garden companion! 🌿\n\n"
            "Here's what I can do:\n"
            "1. Plant Care Guides: Provide watering, soil, temperature, and sunlight needs for plants in your catalog.\n"
            "2. Health Diagnosis: Identify issues like yellow leaves, wilting, or pests and suggest organic treatments.\n"
            "3. Fertilizer Advice: Explain NPK balances and feeding schedules.\n"
            "4. Your Garden Tracking: Pull status and tasks directly from your registered gardens!"
        )

    # 4. User's Personal Garden Status
    if any(k in q for k in ['my garden', 'my plants', 'what am i growing', 'my task', 'my schedule']):
        user_gardens = Garden.objects.filter(user=user)
        if not user_gardens.exists():
            return "You haven't added any gardens yet! Head to 'My Gardens' to set up your growing space, and I'll give you personalized advice."

        user_plants = GardenPlant.objects.filter(garden__user=user)
        pending_tasks = GardenTask.objects.filter(user=user, completed=False)

        g_list = ", ".join([g.name for g in user_gardens])
        p_list = ", ".join([gp.plant.name for gp in user_plants]) if user_plants.exists() else "No plants recorded yet"

        msg = f"🌿 Your Garden Overview:\n• Garden: {g_list}\n• Plants Growing: {p_list}\n"
        if pending_tasks.exists():
            task_lines = "\n".join([f"  - {t.title} (due {t.due_date})" for t in pending_tasks[:3]])
            msg += f"• Upcoming Tasks:\n{task_lines}"
        else:
            msg += "• Tasks: All caught up! No pending tasks."
        return msg

    # 5. Plant Catalog Lookup
    for plant in Plant.objects.all():
        if plant.name.lower() in q:
            return (
                f"🌱 {plant.name} ({plant.scientific_name or 'Garden Plant'}):\n\n"
                f"• Type: {plant.plant_type}\n"
                f"• Soil: {plant.suitable_soil.capitalize()} soil\n"
                f"• Sunlight: {plant.sunlight_requirement.capitalize()}\n"
                f"• Watering: {plant.water_requirement}\n"
                f"• Season: {plant.suitable_season} (Optimal temp: {plant.temperature_min}°C – {plant.temperature_max}°C)\n"
                f"• Overview: {plant.description}"
            )

    # 6. Disease & Symptoms Lookup
    for d in Disease.objects.all():
        if d.name.lower() in q or any(term in q for term in d.name.lower().split()):
            return (
                f"⚠️ Disease Advisory — {d.name}:\n\n"
                f"• Symptoms: {d.symptoms}\n"
                f"• Prevention: {d.prevention}\n"
                f"• Treatment: {d.treatment}"
            )

    # 7. Yellowing Leaves / Wilting
    if any(k in q for k in ['yellow', 'curling', 'wilting', 'dying', 'brown spot', 'leaf spot']):
        return (
            "🍂 Yellow leaves diagnosis:\n"
            "Yellow leaves can be caused by overwatering, poor drainage, nutrient deficiency, or disease. Check soil moisture first and inspect leaves for spots.\n\n"
            "1. Overwatering vs Underwatering: Overwatered leaves are soft and floppy with damp soil; underwatered leaves are dry and crispy. Always check the top 2 inches of soil.\n"
            "2. Nitrogen Deficiency: If older lower leaves turn yellow while the rest remains green, feed with a balanced nitrogen-rich fertilizer.\n"
            "3. Sunlight Check: Make sure the plant receives its recommended daily sunlight hours.\n"
            "4. Fungal Infection: Inspect for dark concentric circles (Early Blight) or powdery white coating (Mildew). Remove affected foliage promptly."
        )

    # 8. Watering Guidance
    if any(k in q for k in ['water', 'watering', 'moisture', 'hydrate', 'irrigation']):
        return (
            "💧 Smart Watering Best Practices:\n\n"
            "• Timing: Water early in the morning (6:00 – 8:00 AM) so foliage dries quickly in the daytime sun.\n"
            "• Technique: Water at the soil base around the roots, avoiding wet leaves which can cause fungal disease.\n"
            "• Finger Test: Insert your finger 1–2 inches into the soil. If it feels dry, water thoroughly; if moist, hold off.\n"
            "• Drainage: Ensure pots and containers have drainage holes to prevent root rot."
        )

    # 9. Fertilizer & Nutrients
    if any(k in q for k in ['fertilizer', 'fertiliser', 'npk', 'nutrient', 'feed', 'compost', 'manure']):
        fert = Fertilizer.objects.first()
        fert_details = f"\n• Featured Fertilizer: {fert.name} ({fert.type}) — {fert.instructions}" if fert else ""
        return (
            f"🧪 Fertilizer & Nutrient Guide:\n\n"
            "• Nitrogen (N): Promotes lush, green foliage and leafy vegetative growth.\n"
            "• Phosphorus (P): Crucial for early root development, flowering, and fruit set.\n"
            "• Potassium (K): Strengthens stems and enhances disease resistance.\n"
            "• Recommendation: Apply organic compost or balanced NPK 5-10-10 every 2–3 weeks during active growth.{fert_details}"
        )

    # 10. Soil Types & Care
    if any(k in q for k in ['soil', 'sandy', 'clay', 'loam', 'loamy', 'silty']):
        return (
            "🪴 Soil Types & Care Guide:\n\n"
            "• Loamy Soil: Ideal for most vegetables and flowers; holds balanced moisture while draining well.\n"
            "• Sandy Soil: Very loose and quick-draining. Enrich with organic compost and coco peat to retain moisture.\n"
            "• Clay Soil: Rich in nutrients but prone to waterlogging and compaction. Aerate with compost or perlite.\n"
            "• Silty Soil: Fine texture with great fertility; avoid over-tilling to prevent compaction."
        )

    # 11. Pests & Organic Control
    if any(k in q for k in ['pest', 'bug', 'insect', 'aphid', 'caterpillar', 'mite', 'worm']):
        return (
            "🐛 Natural Pest Management:\n\n"
            "• Organic Neem Spray: Dilute 5ml cold-pressed neem oil + 2 drops mild soap in 1L warm water. Spray early morning or dusk.\n"
            "• Physical Removal: Blast aphids off with water spray or hand-pick larger caterpillars.\n"
            "• Companion Plants: Plant marigolds, mint, and basil nearby to naturally repel harmful insects.\n"
            "• Good Bugs: Ladybugs and hoverflies feed on aphids — protect beneficial insects!"
        )

    # Fallback
    return (
        "🌱 I'd love to help you with that!\n\n"
        "Could you tell me more details about your plant or question? For example:\n"
        "• 'How do I care for tomatoes?'\n"
        "• 'Why are my rose leaves turning yellow?'\n"
        "• 'What is the best soil for cucumbers?'\n"
        "• 'What should I water today?'"
    )

@login_required
def assistant(request):
    if request.GET.get('clear'):
        request.session['chat_history'] = []
        return redirect('assistant')

    chat_history = request.session.get('chat_history', [])
    if not chat_history:
        chat_history = [
            {
                'role': 'bot',
                'text': 'Hello! 🌿 I am your Smart Garden Assistant. Ask me anything about plant care, watering, fertilizers, pests, or your garden.'
            }
        ]

    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        if question:
            answer = get_assistant_response(question, request.user)
            chat_history.append({'role': 'user', 'text': question})
            chat_history.append({'role': 'bot', 'text': answer})
            request.session['chat_history'] = chat_history
            request.session.modified = True
            return render(request, 'assistant.html', {'chat_history': chat_history, 'question': question, 'answer': answer})

    return render(request, 'assistant.html', {'chat_history': chat_history})

@login_required
def reports(request):
    total=GardenPlant.objects.filter(garden__user=request.user).count(); complete=GardenTask.objects.filter(user=request.user,completed=True).count(); pending=GardenTask.objects.filter(user=request.user,completed=False).count()
    return render(request,'reports.html',{'total':total,'healthy':GardenPlant.objects.filter(garden__user=request.user,status='Healthy').count(),'complete':complete,'pending':pending})

staff_only = user_passes_test(lambda user: user.is_staff, login_url='/login/')

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
