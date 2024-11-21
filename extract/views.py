from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time
from django.db import connection
from .models import *


#get source-list
class get_source_list(APIView):    
    def get(self,request):   
       
        try:
            start_time=time.time()
            
            query="SELECT * FROM extract_source_list;"
            print("hhyy")
            with connection.cursor() as cursor:
                cursor.execute(query) 
                results=cursor.fetchall()
                sources = [{"source_id": row[0], "source_name": row[1]} for row in results]
                            
            execution_time = time.time() - start_time
            response_data={
                "data":sources,
                "query":{
                    "sql":query,
                    "execution_time":execution_time
                }
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except:
            return Response({"error:Server Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#get function-list 
class get_function_list(APIView):    
    def get(self,request):   
        try:
            start_time=time.time()
            query="SELECT * from extract_function_list;"
            with connection.cursor() as cursor:
                cursor.execute(query) 
                results=cursor.fetchall()
                functions=[{"function_id": row[0], "function_name": row[1]} for row in results]
                            
            execution_time = time.time() - start_time
            response_data={
                "data":functions,
                "query":{
                    "sql":query,
                    "execution_time":execution_time
                }
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except:
            return Response({"error:Server Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#get function-list 
class get_etl_list(APIView):    
    def get(self,request):   
        try:
            start_time=time.time()
            query="SELECT * from extract_extract_etl_list;"
            with connection.cursor() as cursor:
                cursor.execute(query) 
                results=cursor.fetchall()
                functions=[{"etl_id":row[0],"etl_name":row[1]} for row in results]
                            
            execution_time = time.time() - start_time
            response_data={
                "data":functions,
                "query":{
                    "sql":query,
                    "execution_time":execution_time
                }
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except:
            return Response({"error:Server Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#get function-source mapping 
class get_function_source_mapping(APIView):    
    def get(self,request,function_id):   
        if function_id is None:
            return Response({"error":"Missing Validation params"},status=status.HTTP_400_BAD_REQUEST)
        try:
            start_time=time.time()
            query="""SELECT esl.*
                   FROM extract_source_list AS esl 
                   JOIN extract_function_source_mapping AS efsm 
                   ON esl.source_id = efsm.source_id 
                   WHERE efsm.function_id = %s"""
            with connection.cursor() as cursor:
                cursor.execute(query,[function_id]) 
                results=cursor.fetchall()
                mapped_values=[{"source_id":row[0],"source_name":row[1]} for row in results]
                            
            execution_time = time.time() - start_time
            response_data={
                "data":mapped_values,
                "query":{
                    "sql":query,
                    "execution_time":execution_time
                }
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except:
            return Response({"error:Server Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class get_extractsubscription_list(APIView):
    def get(self,request):
        try:
            start_time=time.time()
            query="SELECT * from extract_extract_etl_list;"
            with connection.cursor() as cursor:
                cursor.execute(query) 
                results=cursor.fetchall()
                functions=[{"etl_id":row[0],"etl_name":row[1]} for row in results]
                            
            execution_time = time.time() - start_time
            response_data={
                "data":functions,
                "query":{
                    "sql":query,
                    "execution_time":execution_time
                }
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except:
            return Response({"error:Server Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class get_etlglobalparameters(APIView):
    def get(self,request,etl_id):
        if etl_id is None:
            return Response({"error":"Missing Validation params"},status=status.HTTP_400_BAD_REQUEST)
        try:
            start_time=time.time()
            query="""
            SELECT gpm.parameter_id,edpl.parameter_name,gpm.parameter_value
            FROM extract_etl_global_parameters_mapping as gpm
            join extract_extract_data_parameters_list as edpl on gpm.parameter_id=edpl.parameter_id
            where gpm.etl_id=%s;
            """
            with connection.cursor() as cursor:
                cursor.execute(query,[etl_id]) 
                results=cursor.fetchall()
                mappedvalues=[
                    {
                        "parameter_id":row[0],
                        "parameter_name":row[1],
                        "parameter_value":row[2].split(",")
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
        
class get_functionsource_etl(APIView):
    def get(self,request,function_id,source_id):
        if function_id is None or source_id is None:
              return Response({"error":"Missing Validation params"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start_time=time.time()
            query="""
            SELECT etl.etl_id,etl.etl_name FROM extract_extract_etl_list as etl 
            join extract_function_source_etl_mapping as fsem
            on etl.etl_id =fsem.etl_id
            where fsem.function_id=%s and fsem.source_id=%s;
            """
            with connection.cursor() as cursor:
                cursor.execute(query,[function_id,source_id]) 
                results=cursor.fetchall()
                mappedvalues=[
                    {
                        "etl_id":row[0],
                        "etl_name":row[1],
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