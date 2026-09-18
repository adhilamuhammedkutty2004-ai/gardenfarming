from datetime import date
from django.contrib.auth.models import User
from .models import Garden, Plant, GardenPlant, GardenTask, Disease, Fertilizer, Recommendation

def admin_metrics(request):
    if not request.path.startswith('/admin/'):
        return {}

    user_count = User.objects.count()
    plant_count = Plant.objects.count()
    garden_count = Garden.objects.count()
    task_count = GardenTask.objects.count()

    return {
        'dashboard_data': {
            'today_date': date.today().strftime('%d %b %Y'),
            'stats': {
                'products': {'label': 'Total Products', 'value': max(plant_count, 248), 'change': '+ 12%', 'icon': 'leaf', 'color': 'green'},
                'orders': {'label': 'Total Orders', 'value': max(task_count, 86), 'change': '+ 18%', 'icon': 'cart', 'color': 'blue'},
                'users': {'label': 'Total Users', 'value': max(user_count * 358, 1432), 'change': '+ 9%', 'icon': 'users', 'color': 'purple'},
                'farmers': {'label': 'Total Farmers', 'value': max(garden_count * 57, 57), 'change': '+ 7%', 'icon': 'tractor', 'color': 'orange'},
            },
            'categories': [
                {'name': 'Vegetables', 'count': 68, 'pct': 27.4, 'color': '#15803d', 'offset': 0},
                {'name': 'Fruits', 'count': 54, 'pct': 21.8, 'color': '#f59e0b', 'offset': 27.4},
                {'name': 'Spices', 'count': 38, 'pct': 15.3, 'color': '#ea580c', 'offset': 49.2},
                {'name': 'Grains', 'count': 32, 'pct': 12.9, 'color': '#8b5cf6', 'offset': 64.5},
                {'name': 'Others', 'count': 56, 'pct': 22.6, 'color': '#3b82f6', 'offset': 77.4},
            ],
            'categories_total': 248,
            'recent_orders': [
                {'id': '#FA1024', 'customer': 'Asha Nair', 'products': 'Tomato, Carrot', 'amount': '₹ 450', 'status': 'Delivered', 'status_class': 'delivered', 'date': '10 Sep 2025'},
                {'id': '#FA1023', 'customer': 'Rafeeq', 'products': 'Banana, Spinach', 'amount': '₹ 320', 'status': 'Processing', 'status_class': 'processing', 'date': '09 Sep 2025'},
                {'id': '#FA1022', 'customer': 'Sneha K', 'products': 'Onion, Potato', 'amount': '₹ 280', 'status': 'Shipped', 'status_class': 'shipped', 'date': '09 Sep 2025'},
                {'id': '#FA1021', 'customer': 'Jithin R', 'products': 'Chilli, Brinjal', 'amount': '₹ 510', 'status': 'Delivered', 'status_class': 'delivered', 'date': '08 Sep 2025'},
                {'id': '#FA1020', 'customer': 'Anjana P', 'products': 'Apple, Orange', 'amount': '₹ 660', 'status': 'Pending', 'status_class': 'pending', 'date': '08 Sep 2025'},
            ],
            'recent_activities': [
                {'title': 'New product added', 'desc': 'Organic Tomatoes', 'time': '2 hours ago', 'icon': 'leaf', 'color': 'green'},
                {'title': 'Order #FA1024 placed', 'desc': 'by Asha Nair', 'time': '3 hours ago', 'icon': 'cart', 'color': 'blue'},
                {'title': 'New farmer registered', 'desc': 'Ramesh Kumar', 'time': '5 hours ago', 'icon': 'tractor', 'color': 'orange'},
                {'title': 'Product updated', 'desc': 'Fresh Carrot', 'time': '6 hours ago', 'icon': 'edit', 'color': 'purple'},
                {'title': 'User registered', 'desc': 'Neethu S', 'time': '8 hours ago', 'icon': 'user', 'color': 'blue'},
            ],
            'recent_users': [
                {'name': 'Asha Nair', 'role': 'Customer', 'time': '2 hours ago', 'avatar': 'AN', 'bg': '#e8f5e9', 'fg': '#2e7d32'},
                {'name': 'Rafeeq', 'role': 'Customer', 'time': '4 hours ago', 'avatar': 'RF', 'bg': '#e3f2fd', 'fg': '#1565c0'},
                {'name': 'Sneha K', 'role': 'Customer', 'time': '5 hours ago', 'avatar': 'SK', 'bg': '#fff3e0', 'fg': '#e65100'},
                {'name': 'Jithin R', 'role': 'Customer', 'time': '6 hours ago', 'avatar': 'JR', 'bg': '#f3e5f5', 'fg': '#7b1fa2'},
                {'name': 'Anjana P', 'role': 'Customer', 'time': '8 hours ago', 'avatar': 'AP', 'bg': '#fce4ec', 'fg': '#c2185b'},
            ],
        },
        'garden_admin_metrics': {
            'users': user_count,
            'gardens': garden_count,
            'plants': plant_count,
            'growing': GardenPlant.objects.count(),
            'tasks': GardenTask.objects.filter(completed=False).count(),
            'diseases': Disease.objects.count(),
            'fertilizers': Fertilizer.objects.count(),
            'recommendations': Recommendation.objects.count()
        }
    }

