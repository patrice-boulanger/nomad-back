import sys

from django.utils import timezone

from core.models import Mission, User


def match_missions_vs_users(debug=False):
    """ Compare all missions versus all entrepreneur users to find those who have the better matching.

        :returns: a dictionary whose key is a mission primary key and value is a list of
                  tuples (users, percentage of matching). The percentage of matching is the ratio
                  of user's features matching mission's features.
        :rtype: dict

    """
    today = timezone.now()
    all_matches = {}

    # Limit the scope to matchable missions not yet started
    for mission in Mission.objects.filter(is_matchable=True, start__gte=today):
        # Only check active entrepreneur users
        users = User.objects.filter(type=User.ENTREPRENEUR, is_active=True)

        for user in users:
            # check driving license
            if mission.driving_license_required and not user.driving_license:
                if debug:
                    sys.stderr.write(
                        f"{user}: driving license doesn't match\n")
                continue

            # check user's locations
            if mission.zipcode not in user.locations.all().values_list('zipcode', flat=True):
                if debug:
                    sys.stderr.write(f"{user}: zipcode doesn't match\n")
                continue

            # check user's availabilities
            availabilities = user.availabilities.filter(
                start__date__lte=mission.start, end__date__gte=mission.end)
            if not availabilities:
                if debug:
                    sys.stderr.write(f"{user}: availability doesn't match\n")
                continue

            # check experience
            if user.year_experience < mission.year_experience_required:
                if debug:
                    sys.stderr.write(f"{user}: experience doesn't match\n")
                continue

            # check user's features, the user is excluded only if he has no features matching the mission
            mission_features = set(mission.features.all())
            common_features = set(
                user.features.all()).intersection(mission_features)
            if common_features == set():
                if debug:
                    sys.stderr.write(f"{user}: no common features\n")
                continue

            # compute the percentage of matching (even it doesn't mean nothing :-)
            percent = int(100.0 * len(common_features) / len(mission_features))

            # user has matched, add it
            try:
                all_matches[mission.pk].append((user, percent))
            except KeyError:
                all_matches[mission.pk] = [(user, percent), ]

        # finally, sort all matches according to percentage of matching
        for k, v in all_matches.items():
            all_matches[k] = sorted(all_matches[k], key=lambda x: -x[1])

    return all_matches
