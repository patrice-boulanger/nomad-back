from django.shortcuts import render

from core.matching import match_missions_vs_users


def mission_matching_view(request):
    all_matches = match_missions_vs_users()
    return render(request, "admin/mission/mission_matching.html", context={'matches': all_matches,})
