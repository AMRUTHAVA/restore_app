from django.db import migrations

def seed_extra_nudges(apps, schema_editor):
  # Use apps.get_model instead of importing directly — this gives you
  # the model as it existed at this point in the migration history
  Nudge = apps.get_model('restore', 'Nudge')

  nudges = [
    {'nudge_text': 'How mentally demanding was your last work day?', 'nudge_options': {'values': ['light', 'moderate', 'heavy']}, 'nudge_type': 'strain', 'time_of_day': 'morning'},
    {'nudge_text': 'Did you get at least a 20-30 minute break on your last work day?', 'nudge_options': {'values': ['yes', 'somewhat', 'no']}, 'nudge_type': 'recovery', 'time_of_day': 'morning'},
    {'nudge_text': 'What is your perception of your current workload?', 'nudge_options': {'values': ['managable', 'tight', 'overwhelming']}, 'nudge_type': 'strain'},
    {'nudge_text': 'How confident do you feel about your recent workload?', 'nudge_options': {'values': ['confident', 'neutral', 'concerned']}, 'nudge_type': 'strain'},
  ]

  for nudge in nudges:
    Nudge.objects.create(**nudge)

def reverse_seed(apps, schema_editor):
  Nudge = apps.get_model('restore', 'Nudge')
  Nudge.objects.all().delete()

class Migration(migrations.Migration):
  initial = True
  
  dependencies = [
    ('restore', '0016_nudge_time_of_day'),
  ]

  operations = [
    migrations.RunPython(seed_extra_nudges, reverse_seed),
  ]