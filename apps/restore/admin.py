from django.contrib import admin
from .models import User, Department, Customer, Product, Category

admin.site.site_header = 'RESTORE Admin Portal'
admin.site.site_title = 'RESTORE Admin'
admin.site.register(User)

admin.site.register(Department)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
