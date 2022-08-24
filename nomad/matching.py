from django.db.models import Q
from django.utils import timezone
from asyncio.log import logger
from django.conf import settings
import os
import sys
import django
import random
from django.db.models import Prefetch

sys.path.append('.')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nomad.settings.dev")
django.setup()

from core.models import User, Mission
resultat = dict()

date = timezone.now()
def match_all_missions():
    queryset = Mission.objects.all()
    queryset = queryset.exclude(is_matchable=False) #: exclude all missions we don't want to match
    queryset = queryset.exclude(start__lte=date) #: exclude all missions that are expired
    
    
    for q in queryset:
        
        Features = list(q.features.all()) #: add in list all features of the mission
        Taille = len(Features) #: set the length of the list
        queryset2 = User.objects.all()
        if q.driving_license_required: #: if the driving license is required then exclude all user which don't have the driving license
            queryset2 = queryset2.exclude(driving_license=False)

        queryset2 = queryset2.exclude(availabilities=None) #: exclude users that didn't add their availabilities
        queryset2 = queryset2.exclude(locations=None) #: exclude users that didn't add their locations
        queryset2 = queryset2.filter(features__in=[z.pk for z in Features]).order_by('email') #: exclude users that don't have at least one feature in common with the mission
        Indep = list(queryset2)
        for x in Indep:
            if q not in resultat:
                resultat[q]={x.email:f"{int(round(Indep.count(x)*100/Taille))}%"} #: add to a dict the email and the percentage of matching
            if q in resultat:
                if not isinstance(resultat[q], list):
                    # If type is not list then make it list
                    resultat[q] = [resultat[q]]
                    # Append the email in list
                if {x.email:f"{int(round(Indep.count(x)*100/Taille,0))}%"} != resultat[q][0]: #: add in a same mission if there is more than one user matching

                    resultat[q].append({x.email:f"{int(round(Indep.count(x)*100/Taille,0))}%"})


        

    return resultat


if __name__ == "__main__":
    print(match_all_missions())
