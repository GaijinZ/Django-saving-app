from django.contrib import admin
from .models import Profile
from .models import Outgoings
from .models import YourGoal
from .models import MoneyBox
from .models import Obligations


admin.site.register(Profile)
admin.site.register(Outgoings)
admin.site.register(YourGoal)
admin.site.register(MoneyBox)
admin.site.register(Obligations)
