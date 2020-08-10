# Generated by Django 3.0.9 on 2020-08-10 15:20

from django.db import migrations
from django.contrib.gis.geos import fromstr

import datetime
import json
import os
from os.path import dirname, join

def parse_dt_date(dt_date):
    return datetime.date(*map(int, dt_date.split("T")[0].split("-")))

def modify_from_data_tourism(apps, schema_editor):
    PointOfInterest = apps.get_model('tourism', 'PointOfInterest')
    OpeningSchema = apps.get_model('tourism', 'OpeningHoursSchema')
    OpeningHours = apps.get_model('tourism', 'OpeningHours')

    flux_dir = "flux-7559-202008071000"
    root_dir = join(dirname(dirname(__file__)), 'data/tourism', flux_dir, 'objects')

    i = 0
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            i += 1
            with open(join(subdir, file)) as f:
                obj = json.load(f)
            if 'PointOfInterest' in obj['@type']:
                # Find the corresponding POI
                try:
                    poi = PointOfInterest.objects.get(dt_id = obj["@id"])
                    opening_hours_spec = obj['isLocatedAt'][0]["schema:openingHoursSpecification"]
                except (KeyError, TypeError, IndexError):
                    continue
                
                for opening_hours in opening_hours_spec:
                    o = OpeningSchema()
                    if "schema:validFrom" in opening_hours:
                        o.valid_from = parse_dt_date(opening_hours["schema:validFrom"])
                    if "schema:validThrough" in opening_hours:
                        o.valid_through = parse_dt_date(opening_hours["schema:validThrough"])
                    o.poi = poi
                    print(i, '\t', poi.name)
                    o.save()


def delete_data_tourism(apps, schema_editor):
    PointOfInterest = apps.get_model('tourism', 'PointOfInterest')
    OpeningSchema = apps.get_model('tourism', 'OpeningHoursSchema')
    OpeningHours = apps.get_model('tourism', 'OpeningHours')
    db_alias = schema_editor.connection.alias
    
    for oh in OpeningSchema.objects.using(db_alias).all():
        oh.delete()
    
class Migration(migrations.Migration):
    dependencies = [
        ('tourism', '0008_auto_20200810_1720'),
    ]

    operations = [
        migrations.RunPython(modify_from_data_tourism, delete_data_tourism)
    ]
