from .models import Subscription
import random

def get_subscribed():
    subs = Subscription.objects.all()
    users = []
    if len(subs) > 0:
        for sub in subs:
            users.append(sub.user)
    return users

def generate_code():
    t = random.choices(['1', '5', '96', '70', '0'], k=3)
    s = random.choices(['q', 'w', 'e', 'r', 't', 'y', 'z', 'x', 'c', 'v'], k=3)
    t.extend(s)
    random.shuffle(t)
    return ''.join(t)