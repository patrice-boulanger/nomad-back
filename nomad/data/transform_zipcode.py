import sys
import json


def zipcode_transform(filename):


    with open(filename, "rb") as fp:
        data = json.load(fp)

        results = {}
        records = 0

        for item in data:
            try:
                zipcode = item['fields']['code_postal']
            except KeyError:
                print(f"missing zipcode field, ignored", file=sys.stderr)
                continue

            try:
                city = item['fields']['nom_de_la_commune']
            except KeyError:
                city = ""

            try:
                gps = item['fields']['coordonnees_gps']
            except KeyError as e:
                gps = [0., 0.]

            record = { 'city': city, 'latitude': gps[0], 'longitude': gps[1], }

            try:
                results[str(zipcode)].append(record)
            except Exception:
                results[str(zipcode)] = [ record, ]

            records += 1

        print(f"{records} records imported", file=sys.stderr)
        json.dump(results, sys.stdout, indent=2)


if __name__ == '__main__':
    zipcode_transform("laposte_hexasmal.json")
