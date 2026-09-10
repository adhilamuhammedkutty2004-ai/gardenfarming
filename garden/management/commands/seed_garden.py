from django.core.management.base import BaseCommand
from garden.models import Plant, Disease, Fertilizer

class Command(BaseCommand):
    help = 'Adds a small starter plant and advisory catalog.'
    def handle(self, *args, **options):
        plants = [
            ('Tomato','Solanum lycopersicum','A productive warm-season fruiting plant for sunny beds and containers.','Vegetable','loamy','full sun','Regular watering','Monsoon / winter'),
            ('Chilli','Capsicum annuum','A compact, heat-loving plant with a long harvesting season.','Vegetable','loamy','full sun','Moderate watering','All seasons'),
            ('Rose','Rosa','A flowering shrub that benefits from sun, airflow and regular pruning.','Flower','loamy','full sun','Regular watering','Winter'),
            ('Cucumber','Cucumis sativus','A climbing vegetable that grows quickly in warmth and moisture.','Vegetable','sandy','full sun','Frequent watering','Summer'),
            ('Mint','Mentha','A fragrant herb that grows well in containers with partial sun.','Herb','loamy','partial sun','Moderate watering','All seasons'),
            ('Snake Plant','Dracaena trifasciata','A resilient indoor plant that tolerates low light and dry soil.','Houseplant','sandy','shade','Low watering','All seasons'),
        ]
        for name,scientific,desc,kind,soil,sun,water,season in plants:
            Plant.objects.get_or_create(name=name, defaults={'scientific_name':scientific,'description':desc,'plant_type':kind,'suitable_soil':soil,'sunlight_requirement':sun,'water_requirement':water,'suitable_season':season})
        Disease.objects.get_or_create(name='Tomato Early Blight', defaults={'symptoms':'Brown spots, yellowing leaves and dark concentric rings.','prevention':'Improve airflow, rotate crops and avoid wetting leaves.','treatment':'Remove affected leaves and use a suitable fungicide if needed.'})
        Fertilizer.objects.get_or_create(name='NPK 5-10-10', defaults={'type':'Balanced granular fertilizer','description':'Suitable for flowering and fruiting stages.','instructions':'Apply 25 g per plant every 14 days, then water.'})
        self.stdout.write(self.style.SUCCESS('Starter garden catalog is ready.'))
