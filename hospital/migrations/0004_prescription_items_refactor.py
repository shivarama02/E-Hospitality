from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_rename_name_patient_pname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='medication_name',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='dosage',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='duration',
        ),
        migrations.AddField(
            model_name='prescription',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='prescription',
            name='patient_age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='prescription',
            name='visit_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='PrescriptionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_name', models.CharField(max_length=255)),
                ('dosage', models.CharField(max_length=100)),
                ('schedule', models.CharField(blank=True, max_length=20)),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='hospital.prescription')),
            ],
        ),
    ]
