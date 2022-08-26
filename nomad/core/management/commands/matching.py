from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils import timezone
from asyncio.log import logger
from django.conf import settings
import os
import sys
import django
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail

sys.path.append('.')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nomad.settings.dev")
django.setup()

from core.models import User, Mission

date = timezone.now()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        resultat = dict()
        mission=""
        text=""
        queryset = Mission.objects.all()
        # : exclude all missions we don't want to match
        queryset = queryset.exclude(is_matchable=False)
        # : exclude all missions that are expired
        queryset = queryset.exclude(start__lte=date)

        for q in queryset:
            # : add in list all features of the mission
            Features = list(q.features.all())
            Features_indep = []
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
                for z in Features:
                    Features_indep.append(z.pk) 
                queryset2 = queryset2.filter(features__in=Features_indep).order_by('email')
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

        
        for key, values in resultat.items():
            mission=mission+"  "+key
            for value in values:
                for indep, pourcentage in value.items():
                    mission=mission+'  '+indep+' : '+pourcentage
            # self.stdout.write(mission)
        
        send_mail(
            'Matching missions',
            f'{mission}',
            'selim.djeghdir@gmail.com',
            ['selim.djeghdir@gmail.com'],
            fail_silently=False,
        )
