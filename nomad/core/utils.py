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
        try:
            item = settings.ZIPCODE_JSON[zipcode]
            city = item[0]['city']
            latitude = item[0]['latitude']
            longitude = item[0]['longitude']
        except KeyError:
            pass
    else:
        print("WARNING, zipcode database is empty")

    dpt_name = ""
    region = ""

    # If the first two digits are > 95, then the department is the first 3 digits (DOM-TOM), else only the
    # first two digits are relevant.
    dpt = zipcode[:2]
    if int(dpt) > 95:
        dpt = zipcode[:3]

    if len(settings.DPT_AND_REGIONS_JSON):
        try:
            item = settings.DPT_AND_REGIONS_JSON[dpt]
            print(item)
            dpt_name = item['name']
            region = item['region']
        except KeyError:
            pass
    else:
        print("WARNING, department and regions database is empty")

    return city, dpt, dpt_name, region, latitude, longitude