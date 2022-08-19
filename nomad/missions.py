import os
import sys
import django
import random
import string
from datetime import timedelta

sys.path.append('.')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nomad.settings.dev")
django.setup()

from django.utils import timezone
from django.conf import settings

from core.models import Company, Mission

all_zipcodes = list(settings.ZIPCODE_JSON.keys())

for i in range(200):
    start = timezone.now().date() + timedelta(days=random.randint(0, 3))
    end = start + timedelta(days=random.randint(1, 6))
    zipcode = random.choice(all_zipcodes)
    company = random.choice(Company.objects.all())

    Mission.objects.create(title=f"Titre {i}", description="blablabla",
                           start=start, end=end, zipcode=zipcode, company=company)


