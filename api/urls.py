from django.urls import path

from extract.views import *
from extraxt_subscription.views import *

urlpatterns = [
    path('get-sources/',get_source_list.as_view()),
    path('get-functions/',get_function_list.as_view()),
    path('get-etl/',get_etl_list.as_view()),
    path('get-functionsource/<int:function_id>/',get_function_source_mapping.as_view()),
    path('get-globalparameters/<int:etl_id>/',get_etlglobalparameters.as_view()),
    path('get-functionsourceetl/<int:function_id>/<int:source_id>/',get_functionsource_etl.as_view()),
    path('get-subscriptiondetails/<int:etl_id>/',get_subscription_details.as_view()),
    path('get-localparametermapping/<int:etl_id>/',get_localparametermapping.as_view()),
    path('get-singlesubscriptiondetail/<int:etl_id>/<int:subscription_id>/',get_singlesubscriptiondetail.as_view()),
    path('get-parameteroptions/<str:parameter_name>/',get_parametersoptions.as_view()),
    path('post-globalparametermapping/<int:etl_id>/',updateGloabalParamters.as_view()),
    path('post-addsubscription/<int:etl_id>/',addsubscription.as_view()),
    path('post-editlocalparameter/<int:etl_id>/<int:subscription_id>/',editlocalparamters.as_view()),
    path('del-singlesubscription/<int:etl_id>/<int:subscription_id>/',delete_singlesubscription.as_view()),
    path('del-singlelocalparametervalue/<int:subscription_id>/<int:parameter_id>/',DeleteSingleLocalParameterValue.as_view()),
    path('del-singleglobalparametervalue/<int:etl_id>/<int:parameter_id>/',DeleteSingleGlobalParameterValue.as_view()),
]
