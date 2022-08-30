from textwrap import wrap
from turtle import width
from django.shortcuts import render
from django.http.response import HttpResponseNotAllowed
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from .models import User
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from core.matching import match_missions_vs_users
from reportlab.lib.units import cm


def mission_matching_view(request):
    if request.method == 'GET':
        all_matches = match_missions_vs_users()
        return render(request, "admin/mission/mission_matching.html", context={'matches': all_matches, })
    return HttpResponseNotAllowed(permitted_methods=['GET', ])


def profile_pdf(request, id):
    year_experience = {0: "Jeune diplômé", 1: "0 à 3 ans d'expériences",
                       2: "4 à 8 ans d'expériences", 3: "plus de 8 ans d'expériences"}
    if request.method == 'GET':
        user = User.objects.get(pk=id)
        # see the reportlab doc : https://www.reportlab.com/docs/reportlab-userguide.pdf
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()
        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        height = 2*cm
        width = height*285/138
        p.drawImage('media/Nomad_Social_Logo.png',
                    16*cm, 27*cm, width=width, height=height, mask='auto')
        textobject = p.beginText()
        textobject.setFont("Times-Roman", 12)
        textobject.setLeading(20)  # space between the lines
        textobject.setTextOrigin(0.5*cm, 28*cm)
        textobject.textLine(f"Prénom : {user.first_name}")
        if user.driving_license:
            textobject.textLine(f"Permis de conduire : Oui")
        else:
            textobject.textLine(f"Permis de conduire : Non")
        textobject.textLine(
            f"Année(s) d'expérience : {year_experience[user.year_experience]}")

        textobject.textLine(f"Compétences : ")
        textobject.moveCursor(80, -20)
        coord = list(textobject.getCursor())
        for feature in user.features.all():
            textobject.setFont("Times-Roman", 10)
            wraped_text = "\n".join(wrap(f"-{feature}", 80))
            textobject.textLines(f"{wraped_text}")
            # message_style = ParagraphStyle('Normal')
            # message = Paragraph(f"-{feature}", message_style)
            # message.wrapOn(p, 15*cm, 27*cm)
            # message.drawOn(p, coord[0], coord[1])
            # coord[1] = coord[1]-25
        textobject.setFont("Times-Roman", 12)
        textobject.moveCursor(-80, 10)
        textobject.textLines(f"Description : {user.description}")

        p.drawText(textobject)
        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'{user.last_name}_profile.pdf')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', ])
