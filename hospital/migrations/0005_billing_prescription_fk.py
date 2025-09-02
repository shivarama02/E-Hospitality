from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0004_prescription_items_refactor'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='prescription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.prescription'),
        ),
    ]
