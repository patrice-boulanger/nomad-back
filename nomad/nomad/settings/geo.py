import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#: Absolute path to the JSON file for departments and regions (https://www.data.gouv.fr/fr/datasets/departements-et-leurs-regions/)
DPT_AND_REGIONS_FILENAME = os.path.join(BASE_DIR, "data/departments.json")

#: Data from the departments and regions file
DPT_AND_REGIONS_JSON = []
with open(DPT_AND_REGIONS_FILENAME, "rb") as fp:
    try:
        DPT_AND_REGIONS_JSON = json.load(fp)
    except Exception as e:
        print(f"WARNING, cannot load {DPT_AND_REGIONS_FILENAME}: {str(e)}")

#: Absolute path to the JSON file for zipcodes (https://www.data.gouv.fr/fr/datasets/base-officielle-des-codes-postaux/#resources)
ZIPCODE_FILENAME = os.path.join(BASE_DIR, "data/zipcodes.json")

#: Data from the zipcodes file
ZIPCODE_JSON = []
with open(ZIPCODE_FILENAME, "rb") as fp:
    try:
        ZIPCODE_JSON = json.load(fp)
    except Exception as e:
        print(f"WARNING, cannot load {ZIPCODE_FILENAME}: {str(e)}")