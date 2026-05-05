from django.db import migrations

def seed_timezones(apps, schema_editor):
  # Use apps.get_model instead of importing directly — this gives you
  # the model as it existed at this point in the migration history
  Timezone = apps.get_model('restore', 'Timezone')

  timezones = [
    { 'offset': '-12:00', 'observe_dst': False, 'timezone': 'International Date Line West' },
    { 'offset': '-11:00', 'observe_dst': False, 'timezone': 'Midway Island, Samoa' },
    { 'offset': '-10:00', 'observe_dst': False, 'timezone': 'Hawaii' },
    { 'offset': '-09:00', 'observe_dst': True, 'timezone': 'Alaska' },
    { 'offset': '-08:00', 'observe_dst': True, 'timezone': 'Pacific Time (US & Canada)' },
    { 'offset': '-07:00', 'observe_dst': False, 'timezone': 'Arizona' },
    { 'offset': '-07:00', 'observe_dst': True, 'timezone': 'Mountain Time (US & Canada)' },
    { 'offset': '-06:00', 'observe_dst': False, 'timezone': 'Central America, Saskatchewan' },
    { 'offset': '-06:00', 'observe_dst': True, 'timezone': 'Central Time (US & Canada), Guadalajara, Mexico City' },
    { 'offset': '-05:00', 'observe_dst': False, 'timezone': 'Indiana, Bogota, Lima, Quito, Rio Branco' },
    { 'offset': '-05:00', 'observe_dst': True, 'timezone': 'Eastern Time (US & Canada)' },
    { 'offset': '-04:00', 'observe_dst': True, 'timezone': 'Atlantic Time (Canada), Manaus, Santiago' },
    { 'offset': '-04:00', 'observe_dst': False, 'timezone': 'Caracas, La Paz' },
    { 'offset': '-03:30', 'observe_dst': True, 'timezone': 'Newfoundland' },
    { 'offset': '-03:00', 'observe_dst': True, 'timezone': 'Greenland, Brasilia, Montevideo' },
    { 'offset': '-03:00', 'observe_dst': False, 'timezone': 'Buenos Aires, Georgetown' },
    { 'offset': '-02:00', 'observe_dst': True, 'timezone': 'Mid-Atlantic' },
    { 'offset': '-01:00', 'observe_dst': True, 'timezone': 'Azores' },
    { 'offset': '-01:00', 'observe_dst': False, 'timezone': 'Cape Verde Is.' },
    { 'offset': '00:00', 'observe_dst': False, 'timezone': 'Casablanca, Monrovia, Reykjavik' },
    { 'offset': '00:00', 'observe_dst': True, 'timezone': 'GMT: Dublin, Edinburgh, Lisbon, London' },
    { 'offset': '+01:00', 'observe_dst': True, 'timezone': 'Amsterdam, Berlin, Rome, Vienna, Prague, Brussels' },
    { 'offset': '+01:00', 'observe_dst': False, 'timezone': 'West Central Africa' },
    { 'offset': '+02:00', 'observe_dst': True, 'timezone': 'Amman, Athens, Istanbul, Beirut, Cairo, Jerusalem' },
    { 'offset': '+02:00', 'observe_dst': False, 'timezone': 'Harare, Pretoria' },
    { 'offset': '+03:00', 'observe_dst': True, 'timezone': 'Baghdad, Moscow, St. Petersburg, Volgograd' },
    { 'offset': '+03:00', 'observe_dst': False, 'timezone': 'Kuwait, Riyadh, Nairobi, Tbilisi' },
    { 'offset': '+03:30', 'observe_dst': False, 'timezone': 'Tehran' },
    { 'offset': '+04:00', 'observe_dst': False, 'timezone': 'Abu Dhadi, Muscat' },
    { 'offset': '+04:00', 'observe_dst': True, 'timezone': 'Baku, Yerevan' },
    { 'offset': '+04:30', 'observe_dst': False, 'timezone': 'Kabul' },
    { 'offset': '+05:00', 'observe_dst': True, 'timezone': 'Ekaterinburg' },
    { 'offset': '+05:00', 'observe_dst': False, 'timezone': 'Islamabad, Karachi, Tashkent' },
    { 'offset': '+05:30', 'observe_dst': False, 'timezone': 'Chennai, Kolkata, Mumbai, New Delhi, Sri Jayawardenepura' },
    { 'offset': '+05:45', 'observe_dst': False, 'timezone': 'Kathmandu' },
    { 'offset': '+06:00', 'observe_dst': False, 'timezone': 'Astana, Dhaka' },
    { 'offset': '+06:00', 'observe_dst': True, 'timezone': 'Almaty, Nonosibirsk' },
    { 'offset': '+06:30', 'observe_dst': False, 'timezone': 'Yangon (Rangoon)' },
    { 'offset': '+07:00', 'observe_dst': True, 'timezone': 'Krasnoyarsk' },
    { 'offset': '+07:00', 'observe_dst': False, 'timezone': 'Bangkok, Hanoi, Jakarta' },
    { 'offset': '+08:00', 'observe_dst': False, 'timezone': 'Beijing, Hong Kong, Singapore, Taipei' },
    { 'offset': '+08:00', 'observe_dst': True, 'timezone': 'Irkutsk, Ulaan Bataar, Perth' },
    { 'offset': '+09:00', 'observe_dst': True, 'timezone': 'Yakutsk' },
    { 'offset': '+09:00', 'observe_dst': False, 'timezone': 'Seoul, Osaka, Sapporo, Tokyo' },
    { 'offset': '+09:30', 'observe_dst': False, 'timezone': 'Darwin' },
    { 'offset': '+09:30', 'observe_dst': True, 'timezone': 'Adelaide' },
    { 'offset': '+10:00', 'observe_dst': False, 'timezone': 'Brisbane, Guam, Port Moresby' },
    { 'offset': '+10:00', 'observe_dst': True, 'timezone': 'Canberra, Melbourne, Sydney, Hobart, Vladivostok' },
    { 'offset': '+11:00', 'observe_dst': False, 'timezone': 'Magadan, Solomon Is., New Caledonia' },
    { 'offset': '+12:00', 'observe_dst': True, 'timezone': 'Auckland, Wellington' },
    { 'offset': '+12:00', 'observe_dst': False, 'timezone': 'Fiji, Kamchatka, Marshall Is.' },
    { 'offset': '+13:00', 'observe_dst': False, 'timezone': 'Nuku\'alofa' }
  ]

  for timezone in timezones:
    Timezone.objects.create(**timezone)

def reverse_seed(apps, schema_editor):
  Timezone = apps.get_model('restore', 'Timezone')
  Timezone.objects.all().delete()


class Migration(migrations.Migration):
  initial = True
  
  dependencies = [
    ('restore', '0003_seed_baseline_survey_sections'),
  ]

  operations = [
    migrations.RunPython(seed_timezones, reverse_seed),
  ]
