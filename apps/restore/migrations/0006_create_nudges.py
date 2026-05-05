import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.contrib.postgres.fields import ArrayField

class Migration(migrations.Migration):
  initial = True

  dependencies = [
    ('restore', '0005_seed_timezones'),
  ]

  operations = [
    migrations.CreateModel(
      name='Nudge',
      fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('nudge_text', models.CharField(max_length=255)),
        ('nudge_options', models.JSONField(default=dict)),
        ('nudge_type', models.CharField(max_length=255)),
        ('created_at', models.DateTimeField(auto_now_add=True)),
        ('updated_at', models.DateTimeField(auto_now=True)),
      ],
      options={
        'db_table': 'nudges',
        'ordering': ['id'],
      },
    ),
    migrations.CreateModel(
      name='UserNudge',
      fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        (
          'user',
          models.ForeignKey(
            on_delete=django.db.models.deletion.CASCADE,
            related_name='nudges',
            to=settings.AUTH_USER_MODEL,
          ),
        ),
        (
          'nudge',
          models.ForeignKey(
            on_delete=django.db.models.deletion.CASCADE,
            related_name='user_nudges',
            to='restore.nudge',
          ),
        ),
        ('nudge_response', models.CharField(max_length=100, blank=True, null=True)),
        ('is_read', models.BooleanField(default=False, null=False, blank=False)),
        ('system_skipped', models.BooleanField(default=False, null=False, blank=False)),
        ('sent_to', ArrayField(models.CharField(max_length=100))),
        ('sent_at', models.DateTimeField()),
        ('responded_at', models.DateTimeField(blank=True, null=True)),
        ('short_id', models.CharField(max_length=50)),
        ('created_at', models.DateTimeField(auto_now_add=True)),
        ('updated_at', models.DateTimeField(auto_now=True)),
      ],
      options={
        'db_table': 'user_nudges',
        'ordering': ['user_id', '-sent_at'],
      },
    ),
  ]