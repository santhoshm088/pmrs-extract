from django.db import models

#Function-List Model
class function_list(models.Model):
    function_id=models.AutoField(primary_key=True)
    function_name=models.CharField(max_length=45)
    def __str__(self):
        return self.function_name
    
    
#Source-List Model
class source_list(models.Model):
    source_id=models.AutoField(primary_key=True)
    source_name=models.CharField(max_length=45)
    def __str__(self):
        return self.source_name
    
    
#Function-Source-Mapping Model
class function_source_mapping(models.Model):
    function_source_id=models.AutoField(primary_key=True)
    function=models.ForeignKey(function_list,on_delete=models.SET_NULL,null=True)
    source=models.ForeignKey(source_list,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return f"{self.function} - {self.source}"  
    
        
#Extract-ETL-List Model
class extract_etl_list(models.Model):
    etl_id=models.AutoField(primary_key=True)
    etl_name=models.CharField(max_length=45)
    subscription_id=models.CharField(max_length=45)
    etl_description=models.CharField(max_length=45)
    resource_group_name=models.CharField(max_length=45)
    factory_name=models.CharField(max_length=45)
    pipeline_id=models.CharField(max_length=45)
    def __str__(self):
        return str(self.etl_id)

#Extract-Data-Parameters-List Model
class extract_data_parameters_list(models.Model):
    parameter_id=models.AutoField(primary_key=True)
    parameter_type=models.CharField(max_length=45)
    parameter_name=models.CharField(max_length=45)
    parameter_options=models.CharField(max_length=45)
    def __str__(self):
        return str(self.parameter_id)
    


#Function-Source-ETL-Mapping Model
class function_source_etl_mapping(models.Model):
    function_source_etl_id=models.AutoField(primary_key=True)
    function=models.ForeignKey(function_list,on_delete=models.SET_NULL,null=True)
    source=models.ForeignKey(source_list,on_delete=models.SET_NULL,null=True)
    etl=models.ForeignKey(extract_etl_list,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return str(self.function)

    
#Extract-Subscription-List Model
class extract_subscription_list(models.Model):
    subscription_id=models.AutoField(primary_key=True)
    subscription_name=models.CharField(max_length=45)
    etl=models.ForeignKey(extract_etl_list,on_delete=models.SET_NULL,null=True)
    last_execution_time=models.DateTimeField(auto_created=True)
    created_by=models.CharField(max_length=45)
    def __str__(self):
        return self.subscription_name

    

    
#ETL-Global-Parameters-Mapping Model
class etl_global_parameters_mapping(models.Model):
    etl_global_parameter_id=models.AutoField(primary_key=True)
    etl=models.ForeignKey(extract_etl_list,on_delete=models.SET_NULL,null=True)
    parameter=models.ForeignKey(extract_data_parameters_list,on_delete=models.SET_NULL,null=True)
    parameter_value=models.CharField(max_length=45)
    def __str__(self):
        return self.parameter_value


#Extract-Subscription-Parameters-Mapping Model
class extract_subscription_parameters_mapping(models.Model):
    subscription_parameter_id=models.AutoField(primary_key=True)
    subscription=models.ForeignKey(extract_subscription_list,on_delete=models.SET_NULL,null=True)
    parameter=models.ForeignKey(extract_data_parameters_list,on_delete=models.SET_NULL,null=True)
    parameter_value=models.CharField(max_length=45)
    def __str__(self):
        return self.parameter_value
    

    
#ETL-Local-Parameters-Mapping Model
class etl_local_parameters_mapping(models.Model):
    etl_local_parameter_id=models.AutoField(primary_key=True)
    etl=models.ForeignKey(extract_etl_list,on_delete=models.SET_NULL,null=True)
    parameter=models.ForeignKey(extract_data_parameters_list,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return f"{self.etl} - {self.parameter}"  
    