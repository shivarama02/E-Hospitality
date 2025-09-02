from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_billing_prescription_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
