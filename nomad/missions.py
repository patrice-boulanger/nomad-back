from django.conf import settings
from django.utils import timezone
import os
from pydoc import describe
import sys
import django
import random
import string
from datetime import timedelta

sys.path.append('.')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nomad.settings.dev")
django.setup()

from core.models import Company, Mission


T = ["Cadre Social H/F", "Intervant Social H/F", "Ntervenant Social H/F",
     "Travaileur Social H/F", "Gestionnaire Social H/F", "Formateur en Social H/F"]
D = ["Vous mettez en oeuvre le plan d'actions de prévention sanitaire et sociale de l'établissement.", "Vous mettez en oeuvre le plan d'actions de prévention sanitaire et sociale de l'établissement.",
     "Ses activités intérim/recrutement sont structurées en 4 branches : tertiaire (DOMINO STAFF), médico-social", "Ses activités intérim/recrutement sont structurées en 4 branches : tertiaire (DOMINO STAFF), médico-social"]


all_zipcodes = list(settings.ZIPCODE_JSON.keys())

for i in range(200):
    start = timezone.now().date() + timedelta(days=random.randint(0, 3))
    end = start + timedelta(days=random.randint(1, 6))
    zipcode = random.choice(all_zipcodes)
    company = random.choice(Company.objects.all())
    description = random.choice(D)
    titre = random.choice(T)

    Mission.objects.create(title=titre, description=description,
                           start=start, end=end, zipcode=zipcode, company=company)
