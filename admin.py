from django.contrib import admin
from .import models
# Register your models here.
admin .site.register(models.userregister)
admin .site.register(models.Feedback)
admin .site.register(models.Contact)
admin .site.register(models.Category)
admin .site.register(models.Product)
admin .site.register(models.addcart)
admin .site.register(models.Pre_Build)
admin .site.register(models.Cart)

