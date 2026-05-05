import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
  initial = True

  dependencies = [
    ('restore', '0001_initial'),
  ]

  operations = [
    migrations.CreateModel(
      name='BaselineSurveySection',
      fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('key', models.CharField(max_length=255)),
        ('sort', models.IntegerField(default=0)),
        ('created_at', models.DateTimeField(auto_now_add=True)),
        ('updated_at', models.DateTimeField(auto_now=True)),
      ],
      options={
        'db_table': 'baseline_survey_sections',
        'ordering': ['sort'],
      },
    ),
    migrations.CreateModel(
      name='UserBaselineSurveyDetail',
      fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        (
          'user',
          models.OneToOneField(
              on_delete=django.db.models.deletion.CASCADE,
              related_name='baseline_survey_detail',
              to=settings.AUTH_USER_MODEL,
          ),
        ),
        ('chronotype', models.CharField(blank=True, max_length=255, null=True)),
        ('completed_at', models.DateTimeField(blank=True, null=True)),
        ('created_at', models.DateTimeField(auto_now_add=True)),
        ('updated_at', models.DateTimeField(auto_now=True)),
      ],
      options={
        'db_table': 'users_baseline_survey_details',
      },
    ),
    migrations.CreateModel(
      name='UserBaselineSurveySectionResponse',
      fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        (
          'user',
          models.ForeignKey(
            on_delete=django.db.models.deletion.CASCADE,
            related_name='baseline_survey_section_responses',
            to=settings.AUTH_USER_MODEL,
          ),
        ),
        (
          'user_baseline_survey_detail',
          models.ForeignKey(
            on_delete=django.db.models.deletion.CASCADE,
            related_name='baseline_survey_responses',
            to='restore.userbaselinesurveydetail',
          ),
        ),
        (
          'baseline_survey_section',
          models.ForeignKey(
            on_delete=django.db.models.deletion.CASCADE,
            related_name='users_baseline_survey_section_responses',
            to='restore.baselinesurveysection',
          ),
        ),
        ('responses', models.JSONField(default=dict)),
        ('created_at', models.DateTimeField(auto_now_add=True)),
        ('updated_at', models.DateTimeField(auto_now=True)),
      ],
      options={
        'db_table': 'users_baseline_survey_section_responses',
      },
    ),
    migrations.AlterUniqueTogether(
      name='userbaselinesurveysectionresponse',
      unique_together={('user', 'user_baseline_survey_detail', 'baseline_survey_section')},
    ),
  ]