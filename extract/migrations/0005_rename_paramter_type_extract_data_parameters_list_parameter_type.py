# Generated by Django 5.0.9 on 2024-11-18 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extract', '0004_rename_parameter_valu_etl_global_parameters_mapping_parameter_value'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extract_data_parameters_list',
            old_name='paramter_type',
            new_name='parameter_type',
        ),
    ]
