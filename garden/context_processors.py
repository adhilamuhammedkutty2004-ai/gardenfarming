from django.contrib.auth.models import User
from .models import Garden, Plant, GardenPlant, GardenTask, Disease, Fertilizer, Recommendation

def admin_metrics(request):
    if not request.path.startswith('/admin/'):
        return {}
    return {'garden_admin_metrics': {'users': User.objects.count(), 'gardens': Garden.objects.count(), 'plants': Plant.objects.count(), 'growing': GardenPlant.objects.count(), 'tasks': GardenTask.objects.filter(completed=False).count(), 'diseases': Disease.objects.count(), 'fertilizers': Fertilizer.objects.count(), 'recommendations': Recommendation.objects.count()}}
