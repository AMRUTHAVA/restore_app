from django.db import migrations

def seed_energy_schedules(apps, schema_editor):
  # Use apps.get_model instead of importing directly — this gives you
  # the model as it existed at this point in the migration history
  EnergySchedule = apps.get_model('restore', 'EnergySchedule')

  energy_schedules = [
    { "chronotype": "horizon", "time": "6 am", "time_num": 6, "color": "#80ABF9" },
    { "chronotype": "horizon", "time": "7 am", "time_num": 7, "color": "#3875F6" },
    { "chronotype": "horizon", "time": "8 am", "time_num": 8, "color": "#3875F6" },
    { "chronotype": "horizon", "time": "9 am", "time_num": 9, "color": "#3875F6" },
    { "chronotype": "horizon", "time": "10 am", "time_num": 10, "color": "#3875F6" },
    { "chronotype": "horizon", "time": "11 am", "time_num": 11, "color": "#80ABF9" },
    { "chronotype": "horizon", "time": "12 pm", "time_num": 12, "color": "#B3CEFB" },
    { "chronotype": "horizon", "time": "1 pm", "time_num": 13, "color": "#80ABF9" },
    { "chronotype": "horizon", "time": "2 pm", "time_num": 14, "color": "#3875F6" },
    { "chronotype": "horizon", "time": "3 pm", "time_num": 15, "color": "#3875F6" },
    { "chronotype": "horizon", "time": "4 pm", "time_num": 16, "color": "#3875F6" },
    { "chronotype": "horizon", "time": "5 pm", "time_num": 17, "color": "#3875F6" },
    { "chronotype": "horizon", "time": "6 pm", "time_num": 18, "color": "#80ABF9" },
    { "chronotype": "horizon", "time": "7 pm", "time_num": 19, "color": "#B3CEFB" },
    { "chronotype": "horizon", "time": "8 pm", "time_num": 20, "color": "#D9E6FD" },
    { "chronotype": "horizon", "time": "9 pm", "time_num": 21, "color": "#F0F6FE" },
    { "chronotype": "horizon", "time": "10 pm", "time_num": 22, "color": "#F0F6FE" },
    { "chronotype": "horizon", "time": "11 pm", "time_num": 23, "color": "#F0F6FE" },

    { "chronotype": "apex", "time": "6 am", "time_num": 6, "color": "#F0F6FE" },
    { "chronotype": "apex", "time": "7 am", "time_num": 7, "color": "#D9E6FD" },
    { "chronotype": "apex", "time": "8 am", "time_num": 8, "color": "#B3CEFB" },
    { "chronotype": "apex", "time": "9 am", "time_num": 9, "color": "#80ABF9" },
    { "chronotype": "apex", "time": "10 am", "time_num": 10, "color": "#4984F7" },
    { "chronotype": "apex", "time": "11 am", "time_num": 11, "color": "#3875F6" },
    { "chronotype": "apex", "time": "12 pm", "time_num": 12, "color": "#3875F6" },
    { "chronotype": "apex", "time": "1 pm", "time_num": 13, "color": "#3875F6" },
    { "chronotype": "apex", "time": "2 pm", "time_num": 14, "color": "#80ABF9" },
    { "chronotype": "apex", "time": "3 pm", "time_num": 15, "color": "#B3CEFB" },
    { "chronotype": "apex", "time": "4 pm", "time_num": 16, "color": "#80ABF9" },
    { "chronotype": "apex", "time": "5 pm", "time_num": 17, "color": "#3875F6" },
    { "chronotype": "apex", "time": "6 pm", "time_num": 18, "color": "#3875F6" },
    { "chronotype": "apex", "time": "7 pm", "time_num": 19, "color": "#3875F6" },
    { "chronotype": "apex", "time": "8 pm", "time_num": 20, "color": "#80ABF9" },
    { "chronotype": "apex", "time": "9 pm", "time_num": 21, "color": "#B3CEFB" },
    { "chronotype": "apex", "time": "10 pm", "time_num": 22, "color": "#D9E6FD" },
    { "chronotype": "apex", "time": "11 pm", "time_num": 23, "color": "#F0F6FE" },

    { "chronotype": "aurora", "time": "6 am", "time_num": 6, "color": "#F0F6FE" },
    { "chronotype": "aurora", "time": "7 am", "time_num": 7, "color": "#D9E6FD" },
    { "chronotype": "aurora", "time": "8 am", "time_num": 8, "color": "#B3CEFB" },
    { "chronotype": "aurora", "time": "9 am", "time_num": 9, "color": "#80ABF9" },
    { "chronotype": "aurora", "time": "10 am", "time_num": 10, "color": "#3875F6" },
    { "chronotype": "aurora", "time": "11 am", "time_num": 11, "color": "#3875F6" },
    { "chronotype": "aurora", "time": "12 pm", "time_num": 12, "color": "#3875F6" },
    { "chronotype": "aurora", "time": "1 pm", "time_num": 13, "color": "#4984F7" },
    { "chronotype": "aurora", "time": "2 pm", "time_num": 14, "color": "#80ABF9" },
    { "chronotype": "aurora", "time": "3 pm", "time_num": 15, "color": "#B3CEFB" },
    { "chronotype": "aurora", "time": "4 pm", "time_num": 16, "color": "#80ABF9" },
    { "chronotype": "aurora", "time": "5 pm", "time_num": 17, "color": "#4984F7" },
    { "chronotype": "aurora", "time": "6 pm", "time_num": 18, "color": "#3875F6" },
    { "chronotype": "aurora", "time": "7 pm", "time_num": 19, "color": "#3875F6" },
    { "chronotype": "aurora", "time": "8 pm", "time_num": 20, "color": "#3875F6" },
    { "chronotype": "aurora", "time": "9 pm", "time_num": 21, "color": "#80ABF9" },
    { "chronotype": "aurora", "time": "10 pm", "time_num": 22, "color": "#B3CEFB" },
    { "chronotype": "aurora", "time": "11 pm", "time_num": 23, "color": "#D9E6FD" }
  ]

  for energy_schedule in energy_schedules:
    EnergySchedule.objects.create(**energy_schedule)

def reverse_seed(apps, schema_editor):
  EnergySchedule = apps.get_model('restore', 'EnergySchedule')
  EnergySchedule.objects.all().delete()

class Migration(migrations.Migration):
  initial = True
  
  dependencies = [
    ('restore', '0013_energyschedule'),
  ]

  operations = [
    migrations.RunPython(seed_energy_schedules, reverse_seed),
  ]