import requests, os, shortuuid 
from datetime import datetime, UTC
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from .models import Nudge, UserBaselineSurveySectionResponse
from .utils import assign_user_suggestions

User = get_user_model()

def send_nudges(time_of_day):
  """Runs three times day (8am, 1pm, 6pm) and sends nudges."""
  nudge_baseline_survey_section_id = 7
  frequency_mapping = {
    '3': [0, 2, 4],
    '5': [0, 1, 3, 4],
    '7': [0, 1, 2, 3, 4]
  }
  context_nudges = ['caffeine', 'sleep']
  current_weekday = datetime.now(UTC).weekday()
  users = User.objects.all()
  for user in users:
    user_nudge = user.baseline_survey_section_responses.filter(baseline_survey_section_id=nudge_baseline_survey_section_id).first()
    if not user_nudge:
      continue
    user_nudge_responses = user_nudge.responses
    channels = user_nudge_responses['channels']
    frequency = user_nudge_responses['frequency']
    user_time_of_day = user_nudge_responses['time_of_day']
    frequency_week_days = frequency_mapping[frequency]
    if (current_weekday in frequency_week_days and time_of_day == user_time_of_day):
      short_id = shortuuid.uuid()
      most_recent_nudge = user.nudges.order_by('-sent_at').first()
      if most_recent_nudge and not most_recent_nudge.is_read:
        most_recent_nudge.system_skipped = True
        most_recent_nudge.save()
      if current_weekday == 0:
        if most_recent_nudge:
          next_nudge = Nudge.objects.filter(nudge_type__in=context_nudges).exclude(id=most_recent_nudge.nudge_id).order_by('?').first()
        else:
          next_nudge = Nudge.objects.filter(nudge_type__in=context_nudges).order_by('?').first()
      else:
        if most_recent_nudge:
          next_nudge = Nudge.objects.exclude(id=most_recent_nudge.nudge_id).order_by('?').first()
        else:
          next_nudge = Nudge.objects.order_by('?').first()

      user.nudges.create(nudge=next_nudge, sent_to=channels, sent_at=datetime.now(UTC), is_read=False, system_skipped=False, short_id=short_id)

      if 'email' in channels:
        nudge_text = next_nudge.nudge_text
        nudge_options = next_nudge.nudge_options
        template = get_template('emails/_nudge.html')
        template_file_path = template.origin.name
        with open(template_file_path, 'r', encoding='utf-8') as template_file:
          email_template_html = template_file.read()
        host_url = os.environ.get('HOST_URL')
        nudge_url = f'{host_url}/nudge?id={short_id}'
        email_template_html = email_template_html.replace('{HOST_URL}', host_url)
        email_template_html = email_template_html.replace('{NUDGE_URL}', nudge_url)
        email_template_html = email_template_html.replace('{NUDGE_TEXT}', nudge_text)
        options_html = ''
        for nudge_option in nudge_options['values']:
          option_html = '<tr><td style="padding: 6px 0;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="width: 20px; height: 20px; vertical-align: middle; cursor: pointer"><a href="{OPTION_URL}"><div style="width: 20px; height: 20px; border-radius: 50%; border: 2px solid #d0d0d0; background-color: #ffffff;" class="button"></div></a></td><td style="padding-left: 12px; font-size: 15px; color: #1a1a1a; vertical-align: middle; cursor: pointer"><a href="{OPTION_URL}" style="color: #1a1a1a; text-decoration: none">{OPTION_TEXT}</a></td></tr></table></td></tr>'
          option_html = option_html.replace('{OPTION_TEXT}', nudge_option.replace('_', ' ').capitalize())
          option_html = option_html.replace('{OPTION_URL}', f'{nudge_url}&val={nudge_option}')
          options_html = options_html + option_html
        email_template_html = email_template_html.replace('{NUDGE_OPTIONS}', options_html)

        mailgun_url = os.environ.get('MAILGUN_URL')
        mailgun_api_key = os.environ.get('MAILGUN_API_KEY')
        requests.post(
          mailgun_url,
          auth=(
            "api", mailgun_api_key
          ),
          data={
            "from": "RESTORE <support@restorecalendar.com>",
            "to": user.email,
            "subject": "Energy Pulse",
            "html": email_template_html
          }
        )
        print(f'{datetime.now(UTC)}: Nudge sent to {user.email} ({user.id}) with nudge id {next_nudge.id} and to {channels}')


def assign_suggestions():
  """Runs once a day (2am) and assigns user suggestions."""
  users = User.objects.all()
  for user in users:
    assign_user_suggestions(user)

    print(f'{datetime.now(UTC)}: Suggestions created for {user.email} ({user.id})')
