import json, string
from datetime import datetime, UTC
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.staticfiles import finders
from django.contrib import messages
from django.utils.timezone import now
from .models import Product,Order,OrderItem,Category, User, UserNudge, Timezone, BaselineSurveySection, UserBaselineSurveyDetail, UserBaselineSurveySectionResponse, UserEnergyPlanSuggestion, EnergySchedule, Customer, Department
from .services import Chronotype, Apex, Horizon, Aurora
from .utils import get_section_responses, get_user_nudge, assign_user_suggestions
from django.http import FileResponse
import json
from django.http import JsonResponse

######## EXTERNAL #########

def register(request):
  if request.user.is_authenticated:
    return redirect('/dashboard')
  else:
    if request.method == 'POST':
      email = request.POST['email']
      password = request.POST['password']
      first_name = request.POST['first_name']
      last_name = request.POST['last_name']
      user_name = email # request.POST['user_name']

      if User.objects.filter(email=email).exists():
        messages.error(request, '''+email +'''+'Email already exists! please try with another email.')
        return redirect('register')

      user = User.objects.create_user(
        username = user_name,
        email = email,
        password = password,
        first_name = first_name,
        last_name = last_name
      )

      messages.success(request, 'Registration successful, Please login now!')
      return redirect('/login')
    else:
      return render(request, 'register.html')

def user_login(request):
  if request.user.is_authenticated:
    return redirect('/dashboard')
  else:
    if request.method == 'POST':
      email = request.POST['email']
      password = request.POST['password']
      timezone_offset = request.POST['timezone']

      user = authenticate(request, email=email, password=password)

      if user:
        show_banner = 0
        if not user.timezone:
          show_banner = 1

        if not user.timezone and timezone_offset:
          offset, dst = timezone_offset.split(',')
          timezone = Timezone.objects.get(offset=offset, observe_dst=dst)
          User.objects.filter(id=user.id).update(timezone=timezone)

        login(request, user)
        return redirect(f'/dashboard?show_banner={show_banner}')
      else:
        messages.error(request, 'Invalid credentials please try again!')
        return redirect('/login')
    else:
      return render(request, 'login.html')

######## INTERNAL #########

@login_required
def user_logout(request):
  logout(request)
  return redirect('/login')

@login_required
def dashboard(request):
  finish = request.GET.get('finish', 0)
  show_banner = request.GET.get('show_banner', 0)

  my_chronotype = {}
  timezones = Timezone.objects.all()
  responses = UserBaselineSurveySectionResponse.objects.filter(user=request.user)
  max_section_id = responses.order_by("-baseline_survey_section_id").values_list("baseline_survey_section_id", flat=True).first()
  survey_detail = UserBaselineSurveyDetail.objects.filter(user=request.user).first()
  chronotype = survey_detail and survey_detail.chronotype
  survey_completed_at = survey_detail and survey_detail.completed_at
  if chronotype:
    my_chronotype = Chronotype.instance_of(chronotype).to_dict()
  else:
    assign_user_suggestions(request.user)
  apex = Apex()
  horizon = Horizon()
  aurora = Aurora()
  user_nudge = get_user_nudge(request.user.id)

  if finish == '1':
    messages.success(request, 'Baseline survey responses have been successfully saved')

  response_body = {
    'timezones': timezones,
    'general_info': get_section_responses(responses, 'general_info'),
    'workday_sleep': get_section_responses(responses, 'workday_sleep'),
    'nonworkday_sleep': get_section_responses(responses, 'nonworkday_sleep'),
    'rhythms_and_habits': get_section_responses(responses, 'rhythms_and_habits'),
    'work_and_energy': get_section_responses(responses, 'work_and_energy'),
    'caffeine_and_food': get_section_responses(responses, 'caffeine_and_food'),
    'nudges': get_section_responses(responses, 'nudges'),
    'survey_completed_at': survey_completed_at or '',
    'max_section_id': max_section_id or '',
    'chronotype': string.capwords(chronotype or ''),
    'my_chronotype': my_chronotype,
    'apex': apex.to_dict(),
    'horizon': horizon.to_dict(),
    'aurora': aurora.to_dict(),
    'show_banner': show_banner,
  }
  if user_nudge:
    user_nudge.is_read = True
    user_nudge.save()
    response_body['user_nudge_desktop'] = 'desktop' in user_nudge.sent_to
    response_body['user_nudge_id'] = user_nudge.id
    response_body['user_nudge_text'] = user_nudge.nudge_text
    response_body['user_nudge_options'] = json.loads(user_nudge.nudge_options)

  return render(request, 'dashboard.html', response_body)

@login_required
@require_POST
def save_baseline_survey(request):
  try:
    value_keys_to_remove = ['csrfmiddlewaretoken']
    baseline_survey_section = json.loads(request.body)
    for key, value in baseline_survey_section.items():
      for value_key in value_keys_to_remove:
        value.pop(value_key, None)

      user_baseline_survey_detail, created = UserBaselineSurveyDetail.objects.update_or_create(
        user=request.user
      )
      user_baseline_survey_detail.updated_at = now()
      if key == 'nudges':
        user_baseline_survey_detail.completed_at = now()
      user_baseline_survey_detail.save()
      baseline_survey_section = BaselineSurveySection.objects.get(key=key)
      UserBaselineSurveySectionResponse.objects.update_or_create(
        user=request.user,
        user_baseline_survey_detail=user_baseline_survey_detail,
        baseline_survey_section=baseline_survey_section,
        defaults={'responses': value,'updated_at': now()}
      )

      if key == 'nonworkday_sleep':
        # get the chronotype
        chronotype = Chronotype(user_baseline_survey_detail).determine_chronotype()
        # update users chronotype
        user_baseline_survey_detail.chronotype = chronotype
        user_baseline_survey_detail.save(update_fields=["chronotype", "updated_at"])
        user = request.user
        user.energy_schedule_start = Chronotype.ENERGY_SCHEDULE_DEFAULT_START[chronotype]
        user.save(update_fields=["energy_schedule_start", "updated_at"])
        response = {'status': 'ok', 'chronotype': string.capwords(chronotype)}
      else:
        response = {'status': 'ok'}

    return JsonResponse(response)
  except json.JSONDecodeError:
    return JsonResponse({'error': 'Invalid JSON'}, status=400)

@login_required
def energy_plan(request):
  user_tier_a_suggestions = UserEnergyPlanSuggestion.objects.filter(user=request.user, energy_plan_suggestion__tier='A', is_done=False)
  user_tier_b_suggestions = UserEnergyPlanSuggestion.objects.filter(user=request.user, energy_plan_suggestion__tier='B', is_done=False)
  user_tier_c_suggestions = UserEnergyPlanSuggestion.objects.filter(user=request.user, energy_plan_suggestion__tier='C', is_done=False)

  return render(request, 'energy_plan.html', {
    'user_tier_a_suggestions': user_tier_a_suggestions,
    'user_tier_b_suggestions': user_tier_b_suggestions,
    'user_tier_c_suggestions': user_tier_c_suggestions,
  })

@login_required
@require_POST
def save_energy_plan_suggestion_selection(request):
  try:
    value_keys_to_remove = ['csrfmiddlewaretoken']
    user_energy_plan_suggestion_selection = json.loads(request.body)

    suggestion = UserEnergyPlanSuggestion.objects.get(id=user_energy_plan_suggestion_selection['user_energy_plan_suggestion_id'])
    if suggestion:
      suggestion.is_selected = user_energy_plan_suggestion_selection['is_checked']
      suggestion.save()
    response = {'status': 'ok'}
    return JsonResponse(response)
  except json.JSONDecodeError:
    return JsonResponse({'error': 'Invalid JSON'}, status=400)

@login_required
def energy_blueprint(request):
  finish = request.GET.get('finish', 0)

  my_chronotype = {}
  timezones = Timezone.objects.all()
  responses = UserBaselineSurveySectionResponse.objects.filter(user=request.user)
  max_section_id = responses.order_by("-baseline_survey_section_id").values_list("baseline_survey_section_id", flat=True).first()
  survey_detail = UserBaselineSurveyDetail.objects.filter(user=request.user).first()
  chronotype = survey_detail and survey_detail.chronotype
  survey_completed_at = survey_detail and survey_detail.completed_at
  if chronotype:
    my_chronotype = Chronotype.instance_of(chronotype).to_dict()
  apex = Apex()
  horizon = Horizon()
  aurora = Aurora()
  energy_schedules = EnergySchedule.objects.filter(chronotype=chronotype,time_num__gte=request.user.energy_schedule_start).order_by('id')

  if finish == '1':
    messages.success(request, 'Baseline survey responses have been successfully saved')

  energy_schedule_message_shown = request.user.energy_schedule_message_shown_at
  if not energy_schedule_message_shown:
    user = request.user
    user.energy_schedule_message_shown_at = now()
    user.save(update_fields=["energy_schedule_message_shown_at", "updated_at"])

  response_body = {
    'timezones': timezones,
    'general_info': get_section_responses(responses, 'general_info'),
    'workday_sleep': get_section_responses(responses, 'workday_sleep'),
    'nonworkday_sleep': get_section_responses(responses, 'nonworkday_sleep'),
    'rhythms_and_habits': get_section_responses(responses, 'rhythms_and_habits'),
    'work_and_energy': get_section_responses(responses, 'work_and_energy'),
    'caffeine_and_food': get_section_responses(responses, 'caffeine_and_food'),
    'nudges': get_section_responses(responses, 'nudges'),
    'survey_completed_at': survey_completed_at or '',
    'max_section_id': max_section_id or '',
    'chronotype': string.capwords(chronotype or ''),
    'my_chronotype': my_chronotype,
    'apex': apex.to_dict(),
    'horizon': horizon.to_dict(),
    'aurora': aurora.to_dict(),
    'energy_schedules': energy_schedules,
    'energy_schedule_message_shown': energy_schedule_message_shown
  }

  return render(request, 'energy_blueprint.html', response_body)

@login_required
def settings(request):
  if request.method == 'POST':
    channels = request.POST.getlist('channels')
    frequency = request.POST['frequency']
    time_of_day = request.POST['time_of_day']

    responses = {
      'channels': channels,
      'frequency': frequency,
      'time_of_day': time_of_day
    }

    user_baseline_survey_detail = UserBaselineSurveyDetail.objects.get(user=request.user)
    user_baseline_survey_detail.updated_at = now()
    user_baseline_survey_detail.completed_at = now()
    user_baseline_survey_detail.save()
    
    baseline_survey_section = BaselineSurveySection.objects.get(key='nudges')
    baseline_survey_section_response = UserBaselineSurveySectionResponse.objects.get(user=request.user, baseline_survey_section=baseline_survey_section, user_baseline_survey_detail=user_baseline_survey_detail)
    baseline_survey_section_response.responses = responses
    baseline_survey_section_response.updated_at = now()
    baseline_survey_section_response.save()

    messages.success(request, 'Energy pulse settings have been successfully updated')

  responses = UserBaselineSurveySectionResponse.objects.filter(user=request.user)

  return render(request, 'settings.html', {
    'nudges': get_section_responses(responses, 'nudges'),
  })

@login_required
def blueprint_settings(request):
  if request.method == 'POST':
    energy_schedule_start = request.POST['energy_schedule_start']

    user = request.user
    user.energy_schedule_start = int(energy_schedule_start)
    user.save(update_fields=["energy_schedule_start", "updated_at"])

    messages.success(request, 'Energy blueprint settings have been successfully updated')

  return redirect('/settings')

def nudge(request):
  response_recorded = False
  short_id = request.GET.get('id', None)
  value = request.GET.get('val', None) or request.POST.get('nudge_option', None)

  if short_id:
    user_nudge = get_user_nudge(short_id, value)
  elif request.user:
    user_nudge = get_user_nudge(request.user.id, value)
  else:
    user_nudge = None
    
  if user_nudge:
    if user_nudge.responded_at:
      messages.success(request, 'Your response to this energy pulse has already been recorded')
      return redirect('/login')
    else:
      if value != None and value in user_nudge.nudge.nudge_options['values']:
        user_nudge.nudge_response = value
        user_nudge.responded_at = datetime.now(UTC)
        user_nudge.is_read = True # just in case they came from the email click
        response_recorded = True
      else:
        user_nudge.is_read = True
      user_nudge.save()
  else:
    return redirect('/login')

  return render(request, 'nudge.html', {'response_recorded': response_recorded, 'user_nudge_id': user_nudge.id, 'user_nudge_text': user_nudge.nudge_text, 'user_nudge_options': json.loads(user_nudge.nudge_options)})

def service_worker(request):
  return FileResponse(
    open(finders.find('assets/js/helpers/service-worker.js'), "rb"),
    content_type="application/javascript"
  )
from django.shortcuts import render

def about(request):
    return render(request, 'about.html')

@login_required
def customer_list(request):
    customers = Customer.objects.select_related('department').all()
    return render(request, 'customer_list.html', {'customers': customers})

@login_required
def add_customer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number') 
        department_name = request.POST.get('department', '').strip() or 'General'
        department, _ = Department.objects.get_or_create(name=department_name)
        Customer.objects.create(
            name=name,
            email=email,
            department=department,
            mobile_number=mobile_number,
        )
        messages.success(request, 'Customer added successfully!')
    return redirect('customer_list')
def customer_search(request):
    query = request.GET.get('q', '')
    print('......search-----')
    print(query)
    customer_list = Customer.objects.filter(name__icontains=query)
    return render(request, 'customer_list.html', {'customers': customer_list, 'search_query': query})

def product_list(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(
            category_id=category_id
        )
    else:
        products = Product.objects.all()

    return render(
        request,
        'products.html',
        {
            'products': products,
            'categories': categories
        }
    )


def product_search(request):
    print('searching.....')
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    print(f"Search query: {query}, Found products: {products}")
    return render(request, 'products.html', {'products': products, 'search_query': query})


@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        sku = request.POST.get('sku')
        is_active = request.POST.get('is_active') == 'on'

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            sku=sku,
            is_active=is_active
        )
        messages.success(request, 'Product added successfully!')
        return redirect('product_list')

    return redirect('product_list')

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.sku = request.POST.get('sku')
        product.is_active = request.POST.get('is_active') == 'on'
        product.save()

        messages.success(request, 'Product updated successfully!')
        return redirect('product_list')

    return render(request, 'products.html', {'products': Product.objects.all(), 'edit_product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('product_list')

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})

def placeorder(request):
    if request.method == "GET":
      products = Product.objects.all()
      return render(request, 'placeorder.html', {'products': products})
    if request.method == "POST":
      payload = json.loads(request.body.decode("utf-8"))
      print('..........')
      print( payload)
      selected_products = payload.get('products', [])
      customer = Customer.objects.first()
      order = Order.objects.create(
        customer=customer,
        status="Pending"
      )
      for prod in selected_products:
        product = Product.objects.get(id=prod['productId'])
        OrderItem.objects.create(
          order=order,
          product=product,
          quantity=prod['quantity'],
          price=product.price
          )
      return JsonResponse({
    'status': 'success',
    'message': 'Order placed successfully'
    })
def order(request):
    orders = Order.objects.select_related('customer').all()
    return render(request, 'order.html', {'orders': orders})
def orderitems(request):
    order_items = OrderItem.objects.select_related('order', 'product').all()
    print(order_items)
    return render(request, 'orderitems.html', {'order_items': order_items})
def category(request):
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories': categories})
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_code = request.POST.get('category_code')

        Category.objects.create(
            name=name,
            description=description,
            category_code=category_code
        )
        messages.success(request, 'Category added successfully!')
        return redirect('category')
    return render(request, 'category.html', {'categories': Category.objects.all()})
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        category.category_code = request.POST.get('category_code')
        category.save()

        messages.success(request, 'Category updated successfully!')
        return redirect('category')

    return render(request, 'category.html', {'categories': Category.objects.all(), 'edit_category': category})

   