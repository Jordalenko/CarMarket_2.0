from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0006_auto_20260607_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='approved_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
