# Generated by Django 5.1.6 on 2025-04-13 04:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='treatmenthistory',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='available_time_slots',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='taken_time_slots',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='dentist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='treatmenthistory',
            name='treatment_date',
            field=models.DateTimeField(),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('date_of_birth', models.DateField()),
                ('phone_number', models.TextField()),
                ('address', models.TextField()),
                ('image_file', models.ImageField(blank=True, upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='project.patient'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='treatmenthistory',
            name='patient',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='treatments', to='project.patient'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
