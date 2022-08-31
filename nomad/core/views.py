from django.shortcuts import render
from django.http.response import HttpResponseNotAllowed
from .models import User, WorkLocation
from core.matching import match_missions_vs_users
from django.contrib.auth.mixins import LoginRequiredMixin
from django_renderpdf.views import PDFView
from django.conf import settings
import os.path


def mission_matching_view(request):
    if request.method == 'GET':
        all_matches = match_missions_vs_users()
        return render(request, "admin/mission/mission_matching.html", context={'matches': all_matches, })
    return HttpResponseNotAllowed(permitted_methods=['GET', ])


class ProfileInPdf(LoginRequiredMixin, PDFView):
    """Generate labels for some Shipments.

    A PDFView behaves pretty much like a TemplateView, so you can treat it as such.
    """
    template_name = 'core/profile_pdf.html'

    def get_context_data(self, *args, **kwargs):
        diplome = 2
        langue = 7
        experience = 4
        outil = 6
        """Pass some extra context to the template."""
        year_experience = {0: "Jeune diplômé", 1: "0 à 3 ans d'expériences",
                           2: "4 à 8 ans d'expériences", 3: "plus de 8 ans d'expériences"}

        ext = ['.jpg', '.png', '.jpeg', '.svg', '.bmp']
        user = User.objects.get(pk=kwargs['id'])
        worklocations = WorkLocation.objects.filter(user=user.pk)
        context = super().get_context_data(*args, **kwargs)
        context['first_name'] = user.first_name + " " + user.last_name[0]+"."
        context['driving_license'] = user.driving_license
        context['year_experience'] = year_experience[user.year_experience]
        for worklocation in worklocations:
            department = str(worklocation.department)
            if len(department) == 1:
                department = "0"+department
            try:

                context['worklocations'].add(department)
            except:
                context['worklocations'] = {department}

        for feature in user.features.filter(category=diplome):
            try:
                context['graduates'].append(feature)
            except:
                context['graduates'] = [feature]
        for feature in user.features.filter(category=langue):
            try:
                context['langues'].append(feature)
            except:
                context['langues'] = [feature]

        for feature in user.features.filter(category__in=[outil, experience]):
            try:
                context['competences'].append(feature)
            except:
                context['competences'] = [feature]
        context['description'] = user.description
        for file in user.files.all():
            if os.path.splitext(str(file.files))[1] in ext:
                context['pp'] = file.files

        return context
