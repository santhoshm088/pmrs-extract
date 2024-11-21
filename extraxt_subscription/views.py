from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time
from django.db import connection
from extract.models import *
from django.db.models import F, Value
from django.db.models.functions import Concat
#get subscription-details with parameter-values
class get_subscription_details(APIView):    
    def get(self,request,etl_id):  
        if etl_id is None:
            return Response({"error":"Missing Validation params"},status=status.HTTP_400_BAD_REQUEST)
         
        try:
            start_time=time.time()
            query="""
                SELECT edpl.parameter_id,edpl.parameter_name,spm.parameter_value,sl.*
                FROM extract_extract_subscription_parameters_mapping as spm
                join extract_extract_data_parameters_list as edpl  on spm.parameter_id=edpl.parameter_id
                join extract_extract_subscription_list as sl on spm.subscription_id=sl.subscription_id
                where etl_id=%s;
            """
            with connection.cursor() as cursor:
                cursor.execute(query,[etl_id]) 
                results=cursor.fetchall()
                subscriptions = {}

                for row in results:
                    subscription_id = row[4]
    
                    if subscription_id not in subscriptions:
                        subscriptions[subscription_id] = {
                            "subscription_id": subscription_id,
                            "subscription_name": row[5],
                            "last_execution_time": row[3],
                            "created_by": row[6],
                            "etl_id": row[7],
                            "parameters": []
                        }
                    
                    subscriptions[subscription_id]["parameters"].append({
                        "parameter_id":row[0],
                        "parameter_name": row[1],
                        "parameter_value": row[2].split(","),
                    })
                            
            execution_time = time.time() - start_time
            response_data={
                "data":list(subscriptions.values()),
                "query":{
                    "sql":query,
                    "execution_time":execution_time
                }
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except:
            return Response({"error:Server Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
# get_paramter-options(specific one)
class get_parametersoptions(APIView):
    def get(self,request,parameter_name):
        if parameter_name is None or parameter_name == " ":
            return Response({"error":"Missing Validation params"},status=status.HTTP_400_BAD_REQUEST)
        try:
                start_time=time.time()
                query="""
                   SELECT parameter_name,parameter_options FROM extract_extract_data_parameters_list
                    where parameter_name=%s;
                """
                with connection.cursor() as cursor:
                    cursor.execute(query,[parameter_name]) 
                    results=cursor.fetchall()
                    parameters=[{
                        "parameter_name":row[0],
                        "parameter_options":row[1].split(",")
                        }
                        for row in results]       
                execution_time = time.time() - start_time
                response_data={
                    "data":parameters,
                    "query":{
                        "sql":query,
                        "execution_time":execution_time
                    }
                }
                return Response(response_data,status=status.HTTP_200_OK)
        except:
            return Response({"error:Server Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#get_local-parameters-mapping    
class get_localparametermapping(APIView):
    def get(self,request,etl_id):
        if etl_id is None:
              return Response({"error":"Missing Validation params"},status=status.HTTP_400_BAD_REQUEST)
       
        try:
            start_time=time.time()
            query="""
             SELECT  parameter.parameter_type, parameter.parameter_name, parameter.parameter_options
             FROM extract_extract_data_parameters_list as parameter
             JOIN extract_etl_local_parameters_mapping as lpm on parameter.parameter_id=lpm.parameter_id
             where etl_id=%s;
            """
            with connection.cursor() as cursor:
                cursor.execute(query,[etl_id])
                results=cursor.fetchall()
                mappedvalues=[
                    {
                        "parameter_type":row[0],
                        "parameter_name":row[1],
                        "parameter_options":row[2].split(","),
                    }
                    for row in results]
                           
            execution_time = time.time() - start_time
            response_data={
                "data":mappedvalues,
                "query":{
                    "sql":query,
                    "execution_time":execution_time
                }
            }
            return Response(response_data,status=status.HTTP_200_OK)
           
        except:
            return Response({"error:Server Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class get_singlesubscriptiondetail(APIView):
    def get(self,request,etl_id,subscription_id):
        if etl_id is None:
              return Response({"error":"Missing Validation params"},status=status.HTTP_400_BAD_REQUEST)
       
        try:
            start_time=time.time()
            query="""
              SELECT  subscription.subscription_name, dpl.parameter_name, spm.parameter_value
FROM extract_extract_subscription_list  as subscription
JOIN extract_extract_subscription_parameters_mapping as spm on subscription.subscription_id=spm.subscription_id
JOIN extract_extract_data_parameters_list as dpl on spm.parameter_id = dpl.parameter_id


where subscription.subscription_id=%s and subscription.etl_id=%s
                """
            with connection.cursor() as cursor:
                cursor.execute(query, [etl_id, subscription_id])
                results = cursor.fetchall()

        # Group data by subscription name and prepare a list of parameters
                subscription_name = results[0][0] if results else None  # Get the subscription name (assuming all rows have the same subscription name)
                parameters = [
                    {
                        "parameter_name": row[1],
                        "parameter_values": row[2].split(","),
                    }
                    for row in results
                ]

            execution_time = time.time() - start_time

            # Prepare the response
            response_data = {
                "subscription_name": subscription_name,
                "parameters": parameters,
                "query": {
                    "sql": query,
                    "execution_time": execution_time
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)
           
        except:
            return Response({"error:Server Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
               



               
class updateGloabalParamters(APIView):
    def put(self,request,etl_id):
        try:
            parameter_id= request.data['parameter_id']

            parameter_name = request.data["parameter_name"]
    
            value=request.data["value"]

            result = ",".join(value)
            
            start_time=time.time()

            
            edit= etl_global_parameters_mapping.objects.filter(etl_id=etl_id ,parameter_id=parameter_id)
            
            edit.update(parameter_value=result)
            

          
            
#             query="""
# UPDATE e
# SET e.parameter_value = CONCAT(e.parameter_value, ',', %s)
# FROM extract_etl_global_parameters_mapping e
# JOIN extract_extract_data_parameters_list p
#   ON e.parameter_id = p.parameter_id
# WHERE e.etl_id = %s
#   AND p.parameter_name = %s;

#             """
#             with connection.cursor() as cursor:
#                 cursor.execute(query,[result,etl_id,parameter_name])
#                 # results=cursor.fetchall()
#                 # mappedvalues=[
#                 #     {
#                 #         "etl":row[0],
#                 #         "parameter_name":row[1],
#                 #         "parameter_values":row[2].split(","),
#                 #     }
#                 #     for row in results]
                           
            execution_time = time.time() - start_time
            response_data={
                "data":"mappedvalues",
                "query":{
                    "result":"sucessfully updated",
                    "execution_time":execution_time
                }
            }
            return Response(response_data,status=status.HTTP_200_OK)  
        except Exception as e:
            return Response(
                {"error": "Server Error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


class addsubscription(APIView):
    def post(self,request,etl_id):
        

        try:
            subscription_name = request.data.get("subscription_name")
            created_by = request.data.get("created_by")
            last_execution_time = request.data.get("last_execution_time")
            parameters = request.data.get("parameter")

            

        

            etl_instance = extract_etl_list.objects.get(etl_id=etl_id)

            # Create subscription instance
            model_subscription_instance = extract_subscription_list.objects.create(
                subscription_name=subscription_name, 
                etl=etl_instance,
                last_execution_time=last_execution_time,
                created_by=created_by
            )

            model_subscription_id = model_subscription_instance.subscription_id

            # Loop through the parameters
            for param in parameters:
                parameter_id = param.get("parameter_id")
                parameter_values = param.get("parameter_value")

                # Join the parameter values into a comma-separated string
                result = ",".join(parameter_values)


                # Create the mapping entry
                extract_subscription_parameters_mapping.objects.create(
                    subscription=model_subscription_instance,  # Pass the actual model instance here
                    parameter_id=parameter_id,  # Pass the actual parameter instance here, not just the ID
                    parameter_value=result
                )

            # Record the time taken for execution (just for debugging)
            start_time = time.time()
            execution_time = time.time() - start_time

            # Prepare the response data (you can customize this further)
            response_data = {
                "message": "Subscription and parameters stored successfully",
                "execution_time": execution_time,
                "subscription_id": model_subscription_id
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Server Error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


@method_decorator(csrf_exempt, name='dispatch')

class editlocalparamters(APIView):
    # def put(self,request,etl_id,subscription_id):
    #     try :
    #         subscription = request.data.get("subscription")
    #         parameters = request.data.get("parameter")


    #         model_subscription_id = extract_subscription_list.objects.get(subscription_id=subscription_id)
    #         for key, value in parameters.items():
                    
    #                 result = ",".join(value)

    #                 try:
    #                     parameter_instance = extract_data_parameters_list.objects.get(parameter_name=key)
    #                 except extract_data_parameters_list.DoesNotExist:
    #                     return Response(
    #                     {"error": f"Parameter '{key}' does not exist in extract_data_parameters_list."},
    #                     status=status.HTTP_400_BAD_REQUEST
    #                 )


    #                 # Create the mapping entry
    #                 edit = extract_subscription_parameters_mapping.objects.filter(subscription=model_subscription_id,parameter=parameter_instance)


                    
    #                 edit.update(
                
    #              parameter_value=Concat(F('parameter_value'), Value(','+result))
            
    #         )
             

    #         etl_instance = extract_etl_list.objects.get(etl_id=etl_id)

    #         pro =  extract_subscription_list.objects.filter(etl_id=etl_instance, subscription_id=subscription_id)


    #         pro.update(
    #             subscription_name=subscription, 
            
    #         )

    #             # Prepare the response data (you can customize this further)
    #         response_data = {
    #                 "message": "Subscription and parameters stored successfully",
    #                 "execution_time": "kk",
    #                 "subscription_id": "kk"
    #             }

    #         return Response(response_data, status=status.HTTP_200_OK)

    #     except Exception as e:
    #         return Response(
    #             {"error": "Server Error", "details": str(e)},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )   

   def put(self, request, etl_id, subscription_id):
        try:
            
            data = json.loads(request.body)
            subscription_name = data.get("subscription_name")
            parameter_data = data.get("parameter", []) 

            # Update the subscription name
            subscription = extract_subscription_list.objects.filter(
                subscription_id=subscription_id, etl_id=etl_id
            ).first()
            if not subscription:
                return JsonResponse({"error": "Subscription not found"}, status=404)
            
            subscription.subscription_name = subscription_name
            subscription.save()

            
            relevant_parameters = etl_local_parameters_mapping.objects.filter(
                etl_id=etl_id
            ).values_list("parameter_id", flat=True)

            
            for param in parameter_data:
                parameter_id = int(param.get("parameter_id"))
                parameter_values = param.get("parameter_value", []) 
                
                if parameter_id not in relevant_parameters:
                    continue  
                
                
                result = ",".join(parameter_values)

                # Update or append the parameter_value using database-level concatenation
                parameter_mapping = extract_subscription_parameters_mapping.objects.filter(
                    subscription_id=subscription_id,
                    parameter_id=parameter_id
                )

                parameter_mapping.update(
                
                 parameter_value=result
            
            )

            return JsonResponse({"success": "Subscription and parameters updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
            
       

class delete_singlesubscription(APIView):
    def delete(self,request,etl_id,subscription_id):

        try:

            result = extract_subscription_list.objects.filter(
                    subscription_id=subscription_id, etl_id=etl_id
                )
            if result.exists():  # Check if the record exists before deletion
                result.delete()  # Deletes all matching records
                return Response(
                    {"message": "Subscription deleted successfully."},
                    status=status.HTTP_200_OK
            )
            else:
                return Response(
                    {"error": "Subscription not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        


class DeleteSingleLocalParameterValue(APIView):
    def delete(self, request, subscription_id, parameter_id):
        value_to_delete = request.data.get("value")  # Value to remove

        if not value_to_delete:
            return Response(
                {"error": "Value to delete is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch the record
            result = extract_subscription_parameters_mapping.objects.filter(
                subscription_id=subscription_id, parameter_id=parameter_id
            ).first()

            if not result:  # Check if the record exists
                return Response(
                    {"error": "Subscription or parameter not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Parse the parameter_value column
            current_values = result.parameter_value.split(",")  # Assuming comma-separated values
            if value_to_delete not in current_values:
                return Response(
                    {"error": f"Value '{value_to_delete}' not found in parameter values."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Remove the specific value
            updated_values = [v for v in current_values if v != value_to_delete]

            # Update the parameter_value column
            result.parameter_value = ",".join(updated_values)
            result.save()

            return Response(
                {
                    "message": f"Value '{value_to_delete}' deleted successfully.",
                    "updated_values": updated_values,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteSingleGlobalParameterValue(APIView):
    def delete(self, request, etl_id, parameter_id):
        value_to_delete = request.data.get("value")  # Value to remove

        if not value_to_delete:
            return Response(
                {"error": "Value to delete is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch the record
            result = etl_global_parameters_mapping.objects.filter(
                etl_id=etl_id, parameter_id=parameter_id
            ).first()

            if not result:  # Check if the record exists
                return Response(
                    {"error": "Subscription or parameter not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Parse the parameter_value column
            current_values = result.parameter_value.split(",")  # Assuming comma-separated values
            if value_to_delete not in current_values:
                return Response(
                    {"error": f"Value '{value_to_delete}' not found in parameter values."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Remove the specific value
            updated_values = [v for v in current_values if v != value_to_delete]

            # Update the parameter_value column
            result.parameter_value = ",".join(updated_values)
            result.save()

            return Response(
                {
                    "message": f"Value '{value_to_delete}' deleted successfully.",
                    "updated_values": updated_values,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


