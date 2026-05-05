from django.urls import path, include

from .import views
from .models import Customer

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
#     path('save_baseline_survey', views.save_baseline_survey, name='save_baseline_survey'),
#     path('energy_plan', views.energy_plan, name='energy_plan'),
#     path('energy_blueprint', views.energy_blueprint, name='energy_blueprint'),
#     path('save_energy_plan_suggestion_selection', views.save_energy_plan_suggestion_selection, name='save_energy_plan_suggestion_selection'),
#     path('settings', views.settings, name='settings'),
#     path('blueprint_settings', views.blueprint_settings, name='blueprint_settings'),
#     path('nudge', views.nudge, name='nudge'),
#    # path("service-worker.js", views.service_worker, name="service_worker"),
#     path('about/', views.about, name='about'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.add_customer, name='add_customer'),
    path('customers/customer_list/customer_search/', views.customer_search, name='customer_search'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('products/products/search/', views.product_search, name='product_search'),
    path('departments/', views.department_list, name='department_list'),
    path('orders/', views.order, name='orders'),
    path('placeorder/', views.placeorder, name='placeorder'),
    path('ordersitems/', views.orderitems, name='orderitems'),
]   
