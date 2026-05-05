import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
  initial = True

  dependencies = [
    ('restore', '0008_alter_nudge_options_alter_timezone_options_and_more'),
  ]

  operations = [
    migrations.CreateModel(
      name='EnergyPlanSuggestion',
      fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('tier', models.CharField(max_length=255)),
        ('behavioral_cluster', models.CharField(max_length=255)),
        ('suggestion_text', models.CharField(max_length=255)),
        ('created_at', models.DateTimeField(auto_now_add=True)),
        ('updated_at', models.DateTimeField(auto_now=True)),
      ],
      options={
        'db_table': 'energy_plan_suggestions',
        'ordering': ['id'],
      },
    ),
    migrations.CreateModel(
      name='UserEnergyPlanSuggestion',
      fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        (
          'user',
          models.ForeignKey(
            on_delete=django.db.models.deletion.CASCADE,
            related_name='energy_plan_suggestions',
            to=settings.AUTH_USER_MODEL,
          ),
        ),
        (
          'energy_plan_suggestion',
          models.ForeignKey(
            on_delete=django.db.models.deletion.CASCADE,
            related_name='user_energy_plan_suggestions',
            to='restore.energyplansuggestion',
          ),
        ),
        ('is_selected', models.BooleanField(default=False, null=True, blank=True)),
        ('is_done', models.BooleanField(default=False, null=True, blank=True)),
        ('created_at', models.DateTimeField(auto_now_add=True)),
        ('updated_at', models.DateTimeField(auto_now=True)),
      ],
      options={
        'db_table': 'user_energy_plan_suggestions',
        'ordering': ['user_id', '-created_at'],
      },
    ),
  ]