# Generated by Django 5.0.1 on 2024-02-05 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoProject', '0006_remove_polls_student_id_remove_sessions_poll_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='polls',
            name='status',
        ),
        migrations.AlterField(
            model_name='polls',
            name='advancement',
            field=models.IntegerField(max_length=100),
        ),
    ]
