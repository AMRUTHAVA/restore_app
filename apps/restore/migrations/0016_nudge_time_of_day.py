from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('restore', '0015_user_energy_schedule_message_shown_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='nudge',
            name='time_of_day',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
