import string

from django.conf import settings


def zipcode_extract(zipcode):
    """ Returns a tuple (city, department, department name, region, latitude, longitude) from a zipcode. """

    if len(zipcode) != 5:
        raise ValueError("a zipcode must have exactly 5 characters")

    if any([c not in string.digits for c in zipcode]):
        raise ValueError("a zipcode must contain only digits")

    city = ""
    latitude = None
    longitude = None

    if len(settings.ZIPCODE_JSON):
        for item in settings.ZIPCODE_JSON:
            if item['fields']['code_postal'] == zipcode:
                city = item['fields']['nom_de_la_commune']
                coords = item['fields']['coordonnees_gps']
                latitude = coords[0]
                longitude = coords[1]
                break
    else:
        print("WARNING, zipcode database is empty")

    dpt_name = ""
    region = ""

    # If the first two digits are > 95, then the department is the first 3 digits (DOM-TOM), else only the
    # first two digits are relevant.
    dpt = int(zipcode[:2])
    if dpt > 95:
        dpt = int(zipcode[:3])

    if len(settings.DPT_AND_REGIONS_JSON):
        for item in settings.DPT_AND_REGIONS_JSON:
            if item['num_dep'] == dpt:
                dpt_name = item['dep_name']
                region = item['region_name']
                break
    else:
        print("WARNING, department and regions database is empty")

    return city, dpt, dpt_name, region, latitude, longitude