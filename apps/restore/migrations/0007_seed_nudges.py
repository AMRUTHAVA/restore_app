from django.db import migrations

def seed_nudges(apps, schema_editor):
  # Use apps.get_model instead of importing directly — this gives you
  # the model as it existed at this point in the migration history
  Nudge = apps.get_model('restore', 'Nudge')

  nudges = [
    {'nudge_text': 'How is your energy right now?', 'nudge_options': {'values': ['low', 'okay', 'high']}, 'nudge_type': 'calibration'},
    {'nudge_text': 'How demanding was today mentally?', 'nudge_options': {'values': ['light', 'moderate', 'heavy']}, 'nudge_type': 'strain'},
    {'nudge_text': 'Did you get at least a 20-30 minute break today?', 'nudge_options': {'values': ['yes', 'somewhat', 'no']}, 'nudge_type': 'recovery'},
    {'nudge_text': 'How manageable does tomorrow\'s workload feel?', 'nudge_options': {'values': ['managable', 'tight', 'overwhelming']}, 'nudge_type': 'strain'},
    {'nudge_text': 'Did you get enough sleep last night?', 'nudge_options': {'values': ['yes', 'mostly', 'no']}, 'nudge_type': 'calibration'},
    {'nudge_text': 'Did you have caffeine after 2 pm this week?', 'nudge_options': {'values': ['yes', 'unsure', 'no']}, 'nudge_type': 'caffeine'},
    {'nudge_text': 'Did you get morning sunlight within 1 hour of waking yesterday?', 'nudge_options': {'values': ['yes', 'unsure', 'no']}, 'nudge_type': 'light'},
    {'nudge_text': 'How do you usually respond to a poor night\'s sleep?', 'nudge_options': {'values': ['no_effect', 'okay', 'i_cannot_function']}, 'nudge_type': 'calibration'},
    {'nudge_text': 'How rested do you feel?', 'nudge_options': {'values': ['well_rested', 'somewhat', 'very_tired']}, 'nudge_type': 'recovery'},
    {'nudge_text': 'How confident do you feel to complete tomorrow’s workload?', 'nudge_options': {'values': ['confident', 'neutral', 'concerned']}, 'nudge_type': 'strain'},
    {'nudge_text': 'How did you sleep last night?', 'nudge_options': {'values': ['well', 'okay', 'poorly']}, 'nudge_type': 'sleep'},
  ]

  for nudge in nudges:
    Nudge.objects.create(**nudge)

def reverse_seed(apps, schema_editor):
  Nudge = apps.get_model('restore', 'Nudge')
  Nudge.objects.all().delete()

class Migration(migrations.Migration):
  initial = True
  
  dependencies = [
    ('restore', '0006_create_nudges'),
  ]

  operations = [
    migrations.RunPython(seed_nudges, reverse_seed),
  ]