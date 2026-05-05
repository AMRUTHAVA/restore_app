from __future__ import annotations
from datetime import datetime, timedelta

class Apex():

  def to_dict(self):
    return {k: v for k, v in vars(self.__class__).items() if not k.startswith("_") and not k == 'to_dict'}

  name = "apex"
  label = "Apex"
  label_alt = "an Apex"
  tag_line = "You are aligned with the sun."
  short_description = "You have a neutral preference for when you feel most alert and don’t have a strong preference for morning or evening activities."
  long_description = "Your energy builds gradually and finds its stride as the day progresses. Late morning to early afternoon is often when you feel most in flow, which makes it perfect for problem-solving and deep work that blends logic and creativity. In the morning, you’re at your best preparing, organizing, or laying the groundwork for what’s ahead. As evening approaches, shifting toward check in calls or administrative work allows you to wind down while still feeling engaged and productive."
  image_file_primary = "apex_primary.svg"
  download_file_primary = "apex_primary.pdf"
  image_file_gray = "apex_gray.svg"
  download_file_gray = "apex_gray.pdf"

  peak_performance_hours = {
    "primary": "9 am - 11:30 am",
    "secondary": "3:30 pm - 6 pm",
  }

  low_performance_hours = {
    "primary_label": "Afternoon Dip",
    "secondary_label": "Evening Decline",
    "primary": "1 - 3 pm ",
    "secondary": "8 - 10:30 pm",
  }

  strategic_rest_periods = {
    "nap_window": "between 1 - 2:30 pm for 10 - 20 min",
    "micro_resets": "2 - 3 min every 90 - 120 min today",
  }

class Horizon():

  def to_dict(self):
    return {k: v for k, v in vars(self.__class__).items() if not k.startswith("_") and not k == 'to_dict'}

  name = "horizon"
  label = "Horizon"
  label_alt = "a Horizon"
  tag_line = "You work best in the morning."
  short_description = "You have a natural tendency to be alert, energetic, and productive in the early part of the day, preferring to wake up early and go to bed early. You’ve shared enough for Restore to provide some early recommendations."
  long_description = "You thrive in the early hours when the world is quiet and ideas are fresh. Your energy is strongest before noon, making it an ideal time for focused, creative, or strategic work that benefits from clarity and momentum. As the day unfolds, you transition naturally into administrative tasks or check in calls that keep your productivity steady. Gentle starts and intentional pauses help you sustain balance and presence throughout the day."
  image_file_primary = "horizon_primary.svg"
  download_file_primary = "horizon_primary.pdf"
  image_file_gray = "horizon_gray.svg"
  download_file_gray = "horizon_gray.pdf"

  peak_performance_hours = {
    "primary": "7:30 am - 10 am",
    "secondary": "2 pm - 4:30 pm",
  }

  low_performance_hours = {
    "primary_label": "Afternoon Dip",
    "secondary_label": "Evening Decline",
    "primary": "10:30 am - 1:30 pm",
    "secondary": "6 pm - 9 pm",
  }

  strategic_rest_periods = {
    "nap_window": "between 12:30 am - 2 pm for 10 - 20 min",
    "micro_resets": "2 - 3 min every 90 - 120 min today",
  }

class Aurora():

  def to_dict(self):
    return {k: v for k, v in vars(self.__class__).items() if not k.startswith("_") and not k == 'to_dict'}

  name = "aurora"
  label = "Aurora"
  label_alt = "an Aurora"
  tag_line = "You work best in the afternoon."
  short_description = "You have a preference for being more alert in the evening and later at night. You also tend to sleep and wake up later in the day."
  long_description = "You come alive as the light softens and the pace slows later in the day. Your creativity and focus build steadily throughout the day, often peaking in the evening when reflection and imagination meet. Mornings are best for gentle, grounding tasks that help you ease into your rhythm. Later in the day, you’re most attuned to work that calls for insight, deep focus, and innovation. Your natural rhythm is restorative, steady, and intuitive rather than rushed."
  image_file_primary = "aurora_primary.svg"
  download_file_primary = "aurora_primary.pdf"
  image_file_gray = "aurora_gray.svg"
  download_file_gray = "aurora_gray.pdf"

  peak_performance_hours = {
    "primary": "10:30 am - 1 pm",
    "secondary": "6 - 8:30 pm",
  }

  low_performance_hours = {
    "primary_label": "Ramp Up",
    "secondary_label": "Afternoon Decline",
    "primary": "Wakeup - 10:30 am",
    "secondary": "2 - 5 pm",
  }

  strategic_rest_periods = {
    "nap_window": "between 2 - 4 pm for 10 - 20 min",
    "micro_resets": "2 - 3 min every 90 - 120 min today",
  }

class Chronotype:
  APEX = "apex"
  HORIZON = "horizon"
  AURORA = "aurora"
  WORKDAY_SECTION = 2
  NONWORKDAY_SECTION = 3
  ENERGY_SCHEDULE_DEFAULT_START = {
    APEX: 6,
    HORIZON: 7,
    AURORA: 8
  }

  CLASS_MAP = {
    APEX: Apex,
    HORIZON: Horizon,
    AURORA: Aurora,
  }

  def __init__(self, user_baseline_survey_detail):
    self.survey_detail = user_baseline_survey_detail
    responses = user_baseline_survey_detail.user_baseline_survey_responses
    workday_sleep_responses = responses.filter(baseline_survey_section_id=self.WORKDAY_SECTION).first().responses
    nonworkday_sleep_responses = responses.filter(baseline_survey_section_id=self.NONWORKDAY_SECTION).first().responses
    self.workday_sleep_start = workday_sleep_responses['workday_sleep_time']
    self.workday_time_to_sleep = workday_sleep_responses['workday_time_to_sleep']
    self.workday_wakeup = workday_sleep_responses['workday_wakeup_time']
    self.workday_sleepin = workday_sleep_responses['workday_sleepin_time']
    self.nonworkday_sleep_start = nonworkday_sleep_responses['nonworkday_sleep_time']
    self.nonworkday_time_to_sleep = nonworkday_sleep_responses['nonworkday_time_to_sleep']
    self.nonworkday_wakeup = nonworkday_sleep_responses['nonworkday_wakeup_time']
    self.nonworkday_sleepin = nonworkday_sleep_responses['nonworkday_sleepin_time']
    self.chronotype = None
    self.msw = None
    self.msf = None
    self.msf_sc = None

  @classmethod
  def instance_of(self, chronotype) -> Apex | Horizon | Aurora:
    cls = self.CLASS_MAP[chronotype]
    return cls()

  def _calculate_sleep_duration(self, sleep_start: str, time_to_sleep_mins: float, wake_up_time: str, sleep_in_mins: float) -> float:
    """
    Calculate actual sleep duration in hours.
    sleep_start:        time you got into bed        e.g. "10:30 PM"
    time_to_sleep_mins: minutes to fall asleep       e.g. 20
    wake_up_time:       time you woke up             e.g. "6:30 AM"
    sleep_in_mins:      minutes spent lying in bed   e.g. 15
                        after waking before getting up
    returns: sleep duration in hours e.g. 7.58
    """
    fmt = "%I:%M %p"
    sleep_start_dt = datetime.strptime(sleep_start.strip(), fmt)
    wake_up_dt = datetime.strptime(wake_up_time.strip(), fmt)

    # handle crossing midnight
    if wake_up_dt <= sleep_start_dt:
        wake_up_dt += timedelta(days=1)

    # actual sleep onset = bedtime + time to fall asleep
    sleep_onset = sleep_start_dt + timedelta(minutes=time_to_sleep_mins)

    # actual wake time = wake up time - time spent lying in bed
    actual_wake = wake_up_dt - timedelta(minutes=sleep_in_mins)

    duration = (actual_wake - sleep_onset).total_seconds() / 3600

    return round(duration, 2)

  def _to_24h(self, time_str: str) -> float:
    """Convert time string to float hour e.g. '11:30 PM' -> 23.5"""
    dt = datetime.strptime(time_str.strip(), "%I:%M %p")
    hour = dt.hour + dt.minute / 60
    # normalize late night times e.g. 1:00 AM -> 25.0 for correct MSF calculation
    if hour < 6:
        hour += 24
    return hour

  def _calculate(self) -> float:
    # workday
    workday_sleep_onset = self._to_24h(self.workday_sleep_start)
    workday_sleep_duration = self._calculate_sleep_duration(self.workday_sleep_start, float(self.workday_time_to_sleep), self.workday_wakeup, float(self.workday_sleepin))
    # non-workday
    nonworkday_sleep_onset = self._to_24h(self.nonworkday_sleep_start)
    nonworkday_sleep_duration = self._calculate_sleep_duration(self.nonworkday_sleep_start, float(self.nonworkday_time_to_sleep), self.nonworkday_wakeup, float(self.nonworkday_sleepin))
    # calculate msw and msf
    self.msw = workday_sleep_onset + 0.5 * workday_sleep_duration
    self.msf = nonworkday_sleep_onset + 0.5 * nonworkday_sleep_duration
    average_sleep_duration = (workday_sleep_duration + nonworkday_sleep_duration) / 2
    # calculate msf_sc (corrected)
    self.msf_sc = self.msf - ((nonworkday_sleep_duration - average_sleep_duration) / 2)
    return self.msf_sc

  def determine_social_jetlag(self) -> float:
    if not self.msf_sc or not self.msw:
      self._calculate()
    jet_lag = self.msf_sc - self.msw
    return jet_lag

  def determine_chronotype(self) -> str:
    msf_sc = self.msf_sc or self._calculate()
    if msf_sc < 27.0: # before 3:00 AM
        self.chronotype = self.HORIZON
    elif msf_sc > 29.5: # before 5:30 AM
        self.chronotype = self.APEX
    else: # after 5:30 AM
        self.chronotype = self.AURORA
    # update the users chronotype
    return self.chronotype

  def get_instance(self, my_chronotype=None) -> Apex | Horizon | Aurora:
    chronotype = my_chronotype or self.chronotype
    if not chronotype:
      chronotype = self.determine_chronotype()
    cls = self.CLASS_MAP[chronotype]
    return cls()