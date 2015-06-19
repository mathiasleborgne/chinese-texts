from django.contrib.auth.models import User
from texts.models import Profile


user = User.objects.filter(username="mleborgne")[0]
profile = Profile(user=user, chinese_name="道濟")
profile.save()
