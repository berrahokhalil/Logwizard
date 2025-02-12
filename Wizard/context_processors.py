from .models import Notifications

def notifications_processor(request):
    notifications = Notifications.objects.all().order_by('-id')[:5]
    return {
        'notifications': notifications,
        'notifications_count': notifications.count(),
    }

