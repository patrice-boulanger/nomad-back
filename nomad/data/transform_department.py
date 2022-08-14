#!/usr/bin/env python3

import sys
import json


def department_region_transform(filename):
    result = {}

    with open(filename, "rb") as fp:
        data = json.load(fp)

        for item in data:
            dpt = item['num_dep']
            try:
                int(dpt)
            except ValueError:
                print(f"non-numeric department {dpt}, ignored", file=sys.stderr)
                continue

            dpt_name = item['dep_name']
            region = item['region_name']

            result[str(dpt)] = { "name": dpt_name, "region": region, }

    json.dump(result, sys.stdout, indent=2)


if __name__ == '__main__':
    department_region_transform("departements-region.json")