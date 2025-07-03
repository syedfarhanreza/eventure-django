from django.contrib.postgres.indexes import GinIndex
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="event",
            index=GinIndex(
                name="event_name_trgm",
                fields=["name"],
                opclasses=["gin_trgm_ops"],
            ),
        ),
        migrations.AddIndex(
            model_name="event",
            index=GinIndex(
                name="event_location_trgm",
                fields=["location"],
                opclasses=["gin_trgm_ops"],
            ),
        ),
    ]
