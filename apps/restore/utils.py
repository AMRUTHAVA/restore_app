from .models import UserNudge, EnergyPlanSuggestion, UserEnergyPlanSuggestion

def get_section_responses(responses_qs, key):
  return (
    responses_qs.filter(baseline_survey_section__key=key)
    .values_list("responses", flat=True)
    .first() or {}
  )

def get_user_nudge(user_id_or_short_id, post_value=None):
  is_user_id = isinstance(user_id_or_short_id, int)
  sql = 'SELECT user_nudges.id, nudges.nudge_text, nudges.nudge_options FROM user_nudges INNER JOIN nudges ON nudges.id = user_nudges.nudge_id'

  if is_user_id:
    sql = sql + ' WHERE user_nudges.user_id = %s'
    id_to_use = user_id_or_short_id
  else:
    sql = sql + ' WHERE user_nudges.short_id = %s'
    id_to_use = str(user_id_or_short_id)

  if post_value == None:
    sql = sql + ' AND user_nudges.is_read = %s AND user_nudges.system_skipped = %s '
    values = [id_to_use, False, False]
  else:
    values = [id_to_use]
  sql = sql + ' LIMIT 1'

  user_nudge = UserNudge.objects.raw(sql, values)

  return user_nudge and user_nudge[0]

def generate_short_id():
  return uuid.uuid4().hex[:8]

def assign_user_suggestions(user):
  user_tier_a_suggestion_ids = []
  user_tier_b_suggestion_ids = []
  user_tier_c_suggestion_ids = []

  user_tier_a_suggestions = UserEnergyPlanSuggestion.objects.filter(user=user, energy_plan_suggestion__tier='A', is_done=False)
  user_tier_b_suggestions = UserEnergyPlanSuggestion.objects.filter(user=user, energy_plan_suggestion__tier='B', is_done=False)
  user_tier_c_suggestions = UserEnergyPlanSuggestion.objects.filter(user=user, energy_plan_suggestion__tier='C', is_done=False)

  for user_tier_a_suggestion in user_tier_a_suggestions:
    user_tier_a_suggestion.is_done = True
    user_tier_a_suggestion.save()
    user_tier_a_suggestion_ids.append(user_tier_a_suggestion.energy_plan_suggestion_id)

  for user_tier_b_suggestion in user_tier_b_suggestions:
    user_tier_b_suggestion.is_done = True
    user_tier_b_suggestion.save()
    user_tier_b_suggestion_ids.append(user_tier_b_suggestion.energy_plan_suggestion_id)

  for user_tier_c_suggestion in user_tier_c_suggestions:
    user_tier_c_suggestion.is_done = True
    user_tier_c_suggestion.save()
    user_tier_c_suggestion_ids.append(user_tier_c_suggestion.energy_plan_suggestion_id)

  suggestions_sql = """
    SELECT distinct on (behavioral_cluster) id, tier, behavioral_cluster, suggestion_text 
    FROM public.energy_plan_suggestions ep
    WHERE tier = %s AND id != ALL(%s)
    ORDER BY behavioral_cluster, random()
    LIMIT 4
  """

  tier_a_suggestions = EnergyPlanSuggestion.objects.raw(suggestions_sql, ['A', user_tier_a_suggestion_ids])
  tier_b_suggestions = EnergyPlanSuggestion.objects.raw(suggestions_sql, ['B', user_tier_b_suggestion_ids])
  tier_c_suggestions = EnergyPlanSuggestion.objects.raw(suggestions_sql, ['C', user_tier_c_suggestion_ids])

  for tier_a_suggestion in tier_a_suggestions:
    user.energy_plan_suggestions.create(energy_plan_suggestion=tier_a_suggestion, is_selected=False, is_done=False)
  
  for tier_b_suggestion in tier_b_suggestions:
    user.energy_plan_suggestions.create(energy_plan_suggestion=tier_b_suggestion, is_selected=False, is_done=False)

  for tier_c_suggestion in tier_c_suggestions:
    user.energy_plan_suggestions.create(energy_plan_suggestion=tier_c_suggestion, is_selected=False, is_done=False)