# Generated by Django 3.0.9 on 2020-08-06 17:16

from django.db import migrations
import json
from os.path import dirname, join
import os
from django.contrib.gis.geos import fromstr


def load_from_data_tourism(apps, schema_editor):
    PointOfInterest = apps.get_model('tourism', 'PointOfInterest')
    flux_dir = "flux-7559-202008041002"
    root_dir = join(dirname(dirname(__file__)), 'data/tourism', flux_dir, 'objects')

    i = 0
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            i += 1
            with open(join(subdir, file)) as f:
                obj = json.load(f)
            if 'PointOfInterest' in obj['@type']:
                attributes = {}
                # Required attributes
                try:
                    dt_id = obj["@id"]
                    name = obj['rdfs:label']['fr'][0]
                    latitude = obj['isLocatedAt'][0]['schema:geo']['schema:latitude']
                    longitude = obj['isLocatedAt'][0]['schema:geo']['schema:longitude']
                    location = fromstr(f'Point({longitude} {latitude})', srid=4326)
                except:
                    continue

                # Optionnal attributes
                try:
                    attributes['street_address'] = '\n'.join(obj['isLocatedAt'][0]["schema:address"][0]["schema:streetAddress"])
                    attributes['city'] = obj['isLocatedAt'][0]["schema:address"][0]["schema:addressLocality"]
                except:
                    pass
                print(i, '\t', name)
                PointOfInterest(name=name, location=location, datatourism_id=dt_id, **attributes).save()

def delete_data_tourism(apps, schema_editor):
    PointOfInterest = apps.get_model('tourism', 'PointOfInterest')
    db_alias = schema_editor.connection.alias
    PointOfInterest.objects.using(db_alias).exclude(datatourism_id="").delete()
    
class Migration(migrations.Migration):
    dependencies = [
        ('tourism', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_from_data_tourism, delete_data_tourism)
    ]