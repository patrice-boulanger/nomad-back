

from django.db.models import Q
from django.utils import timezone
from asyncio.log import logger
from django.conf import settings
import os
import sys
import django
from django.http import HttpResponse
from django.shortcuts import render

sys.path.append('.')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nomad.settings.dev")
django.setup()

from core.models import User, Mission

date = timezone.now()


def match_all_missions(request):
    resultat = dict()
    queryset = Mission.objects.all()
    # : exclude all missions we don't want to match
    queryset = queryset.exclude(is_matchable=False)
    # : exclude all missions that are expired
    queryset = queryset.exclude(start__lte=date)

    for q in queryset:
        # : add in list all features of the mission
        Features = list(q.features.all())
        Taille = len(Features)  # : set the length of the list
        queryset2 = User.objects.all()
        if q.driving_license_required:  # : if the driving license is required then exclude all user which don't have the driving license
            queryset2 = queryset2.exclude(driving_license=False)

        # : exclude users that didn't add their availabilities
        queryset2 = queryset2.exclude(availabilities=None)
        # : exclude users that didn't add their locations
        queryset2 = queryset2.exclude(locations=None)
        # : exclude users that don't have at least one feature in common with the mission
        if Taille != 0:
            queryset2 = queryset2.filter(
                features__in=[z.pk for z in Features]).order_by('email')
        Indep = list(queryset2)
        if Taille != 0:
            for x in Indep:
                if f'{q.title} M-{q.pk}' not in resultat:
                    # : add to a dict the email and the percentage of matching
                    resultat[f'{q.title} M-{q.pk}'] = {
                        x.email: f"{int(round(Indep.count(x)*100/Taille))}%"}
                if f'{q.title} M-{q.pk}' in resultat:
                    if not isinstance(resultat[f'{q.title} M-{q.pk}'], list):
                        # If type is not list then make it list
                        resultat[f'{q.title} M-{q.pk}'] = [resultat[f'{q.title} M-{q.pk}']]
                        # Append the email in list
                    # : add in a same mission if there is more than one user matching
                    if {x.email: f"{int(round(Indep.count(x)*100/Taille,0))}%"} != resultat[f'{q.title} M-{q.pk}'][-1]:

                        resultat[f'{q.title} M-{q.pk}'].append(
                            {x.email: f"{int(round(Indep.count(x)*100/Taille,0))}%"})
        else:
            for x in Indep:
                if f'{q.title} M-{q.pk}' not in resultat:
                    # : add to a dict the email and the percentage of matching
                    resultat[f'{q.title} M-{q.pk}'] = {
                        x.email: f"100%"}
                if f'{q.title} M-{q.pk}' in resultat:
                    if not isinstance(resultat[f'{q.title} M-{q.pk}'], list):
                        # If type is not list then make it list
                        resultat[f'{q.title} M-{q.pk}'] = [resultat[f'{q.title} M-{q.pk}']]
                        # Append the email in list
                    # : add in a same mission if there is more than one user matching
                    if {x.email: f"100%"} != resultat[f'{q.title} M-{q.pk}'][-1]:

                        resultat[f'{q.title} M-{q.pk}'].append(
                            {x.email: f"100%"})

    return render(request, 'admin/mission/matching.html', {'resultat': resultat})


if __name__ == "__main__":
    match_all_missions()
