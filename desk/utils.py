from .models import Subscription

def get_subscribed():
    subs = Subscription.objects.all()
    users = []
    if len(subs) > 0:
        for sub in subs:
            users.append(sub.user)
    return users