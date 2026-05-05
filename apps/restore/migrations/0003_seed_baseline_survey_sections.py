from django.db import migrations

def seed_baseline_survey_sections(apps, schema_editor):
  # Use apps.get_model instead of importing directly — this gives you
  # the model as it existed at this point in the migration history
  BaselineSurveySection = apps.get_model('restore', 'BaselineSurveySection')

  sections = [
    {'key': 'general_info', 'sort': 1},
    {'key': 'workday_sleep', 'sort': 2},
    {'key': 'nonworkday_sleep', 'sort': 3},
    {'key': 'work_and_energy', 'sort': 4},
    {'key': 'rhythms_and_habits', 'sort': 5},
    {'key': 'caffeine_and_food', 'sort': 6},
    {'key': 'nudges', 'sort': 7},
  ]

  for section in sections:
    BaselineSurveySection.objects.create(**section)

def reverse_seed(apps, schema_editor):
  BaselineSurveySection = apps.get_model('restore', 'BaselineSurveySection')
  BaselineSurveySection.objects.all().delete()


class Migration(migrations.Migration):
  initial = True
  
  dependencies = [
    ('restore', '0002_create_baselinesurveytables'),
  ]

  operations = [
    migrations.RunPython(seed_baseline_survey_sections, reverse_seed),
  ]
