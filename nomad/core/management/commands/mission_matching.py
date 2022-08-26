import io
import sys

from django.core.management import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from core.matching import match_missions_vs_users
from core.models import Mission


class Command(BaseCommand):

    help = "match user's vs. missions"

    def add_arguments(self, parser):
        parser.add_argument("-d", "--debug", help="show debug messages", required=False, action="store_true")
        parser.add_argument("-e", "--email", help="send the result to this email. Can be repeated multiple times",
                            required=False, action="append")

    def handle(self, *args, **options):
        debug = options['debug']

        all_matches = match_missions_vs_users(debug)
        if len(all_matches) == 0:
            sys.stdout.write("no matches\n")
            sys.exit(0)

        buffer = io.StringIO()
        buffer.write("Missions matching result:\r\n\r\n")

        for mission_pk, data in all_matches.items():
            mission = Mission.objects.get(pk=mission_pk)
            buffer.write(f"Mission {mission} ({mission.title}):\r\n")

            for user, percent in data:
                buffer.write(f"    {user.email} matches {percent}% of the required features\r\n")

            buffer.write('\r\n')

        if options['email']:
            send_mail(subject='Matching of missions',
                message=buffer.getvalue(),
                from_email='no-reply@nomadsocial.fr',
                recipient_list=options['email'],
                html_message=render_to_string(template_name="core/mission_matching_email.html", context={
                    'matches': all_matches,
                    'base_url': settings.BASE_URL,
                }))