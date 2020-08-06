# Generated by Django 3.0.9 on 2020-08-06 16:27


from django.db import migrations
import json
from os.path import dirname, join
import os
from django.contrib.gis.geos import fromstr


def modify_from_data_tourism(apps, schema_editor):
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
                # Find the corresponding POI
                try:
                    poi = PointOfInterest.objects.get(datatourism_id = obj["@id"])
                except:
                    continue

                attributes = {}
                # Add attributes
                try:
                    attributes['categories'] = "\n".join(obj['@type'])
                    attributes['email'] = obj['hasContact'][0]['schema:email'][0]
                    attributes['phone'] = obj['hasContact'][0]['schema:telephone'][0]
                    attributes['website'] = obj['hasContact'][0]['foaf:homepage'][0]
                    attributes['description'] = '\n\n'.join(obj['hasDescription'][0]['shortDescription']['fr'])
                except:
                    pass
                print(i, '\t', poi.name)

                for k, v in attributes.items():
                    setattr(poi, k, v)
                poi.save()

def delete_data_tourism(apps, schema_editor):
    PointOfInterest = apps.get_model('tourism', 'PointOfInterest')
    db_alias = schema_editor.connection.alias
    for poi in PointOfInterest.objects.using(db_alias).exclude(datatourism_id=""):
        poi.categories = ""
        poi.email = ""
        poi.phone = ""
        poi.website = ""
        poi.description = ""
        poi.save()
    
class Migration(migrations.Migration):
    dependencies = [
        ('tourism', '0003_auto_20200806_1824'),
    ]

    operations = [
        migrations.RunPython(modify_from_data_tourism, delete_data_tourism)
    ]
