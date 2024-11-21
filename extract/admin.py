from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(function_list)
admin.site.register(source_list)
admin.site.register(function_source_mapping)
admin.site.register(extract_etl_list)
admin.site.register(extract_data_parameters_list)
admin.site.register(function_source_etl_mapping)
admin.site.register(extract_subscription_list)
admin.site.register(etl_global_parameters_mapping)
admin.site.register(extract_subscription_parameters_mapping)
admin.site.register(etl_local_parameters_mapping)
