import django.db.models.deletion
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from auditlog.registry import auditlog

class User(AbstractUser):
  username = models.CharField(unique=True, max_length=200)
  email = models.EmailField(unique=True)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  timezone = models.ForeignKey(
    "restore.Timezone",
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name="users",
    db_column="timezone_id",
  )
  energy_schedule_start = models.IntegerField(null=True, blank=True)
  energy_schedule_message_shown_at = models.DateTimeField(null=True, blank=True)


  class Meta:
    db_table = 'users'

  def __str__(self):
    return self.email

auditlog.register(User, serialize_data=True)


class BaselineSurveySection(models.Model):
  key = models.CharField(max_length=255)
  sort = models.IntegerField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'baseline_survey_sections'
    ordering = ['sort']

  def __str__(self):
    return self.key

auditlog.register(BaselineSurveySection, serialize_data=True)


class UserBaselineSurveyDetail(models.Model):
  user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=django.db.models.deletion.CASCADE,
    related_name='baseline_survey_detail',
  )
  chronotype = models.CharField(max_length=255, null=True, blank=True)
  completed_at = models.DateTimeField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'users_baseline_survey_details'

  def __str__(self):
    return f'UserBaselineSurveyDetail(user={self.user_id})'

auditlog.register(UserBaselineSurveyDetail, serialize_data=True)


class UserBaselineSurveySectionResponse(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=django.db.models.deletion.CASCADE,
    related_name='baseline_survey_section_responses',
  )
  user_baseline_survey_detail = models.ForeignKey(
    UserBaselineSurveyDetail,
    on_delete=django.db.models.deletion.CASCADE,
    related_name='user_baseline_survey_responses',
  )
  baseline_survey_section = models.ForeignKey(
    BaselineSurveySection,
    on_delete=django.db.models.deletion.CASCADE,
    related_name='baseline_survey_section_responses',
  )
  responses = models.JSONField(default=dict)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'users_baseline_survey_section_responses'
    unique_together = [['user', 'user_baseline_survey_detail', 'baseline_survey_section']]

  def __str__(self):
    return f'UserBaselineSurveySectionResponse(user={self.user_id}, section={self.baseline_survey_section_id})'

auditlog.register(UserBaselineSurveySectionResponse, serialize_data=True)


class Timezone(models.Model):
  offset = models.CharField(max_length=10)
  observe_dst = models.BooleanField(default=False)
  timezone = models.CharField(max_length=100, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "timezones"
    ordering = ["id"]

  def __str__(self):
    return f"{self.timezone} ({self.offset})"

auditlog.register(Timezone, serialize_data=True)


class Nudge(models.Model):
  nudge_text = models.CharField(max_length=255)
  nudge_options = models.JSONField(default=dict)
  nudge_type = models.CharField(max_length=255)
  time_of_day = models.CharField(max_length=255, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'nudges'

  def __str__(self):
    return self.nudge_text

auditlog.register(Nudge, serialize_data=True)


class UserNudge(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=django.db.models.deletion.CASCADE,
    related_name='nudges',
  )
  nudge = models.ForeignKey(
    Nudge,
    on_delete=django.db.models.deletion.CASCADE,
    related_name='user_nudges',
  )
  nudge_response = models.CharField(max_length=100)
  is_read = models.BooleanField(default=False)
  system_skipped = models.BooleanField(default=False)
  sent_to = ArrayField(models.CharField(max_length=100))
  sent_at = models.DateTimeField()
  responded_at = models.DateTimeField()
  short_id = models.CharField(max_length=50)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'user_nudges'

  def __str__(self):
    return str(self.is_read)

auditlog.register(UserNudge, serialize_data=True)


class EnergyPlanSuggestion(models.Model):
  tier = models.CharField(max_length=255)
  behavioral_cluster = models.CharField(max_length=255)
  suggestion_text = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'energy_plan_suggestions'

  def __str__(self):
    return self.suggestion_text

auditlog.register(EnergyPlanSuggestion, serialize_data=True)


class UserEnergyPlanSuggestion(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=django.db.models.deletion.CASCADE,
    related_name='energy_plan_suggestions',
  )
  energy_plan_suggestion = models.ForeignKey(
    EnergyPlanSuggestion,
    on_delete=django.db.models.deletion.CASCADE,
    related_name='user_energy_plan_suggestions',
  )
  is_selected = models.BooleanField(default=False)
  is_done = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'user_energy_plan_suggestions'

  def __str__(self):
    return str(self.is_selected)

auditlog.register(UserEnergyPlanSuggestion, serialize_data=True)

class EnergySchedule(models.Model):
  chronotype = models.CharField(max_length=255)
  time_num = models.IntegerField()
  time = models.CharField(max_length=255)
  color = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'energy_schedules'

  def __str__(self):
    return self.color

auditlog.register(EnergySchedule, serialize_data=True)

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category_code = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name
class Product(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField(null=True, blank=True)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  sku = models.CharField(max_length=100, unique=True, null=True, blank=True)
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  expires_at = models.DateTimeField(null=True, blank=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

  class Meta:
    db_table = 'products'

  def __str__(self):
    return self.name
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
  
    def __str__(self):
        return self.name
 
class Order(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=50, default="Pending")

  def __str__(self):
   return f"Order {self.id} - {self.customer.name}"

class OrderItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
  price = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)
  quantity = models.IntegerField(default=1)
  def __str__(self):
    return f"OrderItem {self.id} - Order {self.order.id}"
 

# auditlog.register(Product, serialize_data=True)

