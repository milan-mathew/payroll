from django.contrib.auth.models import User, Group
from rest_framework import serializers
from payrollapi.models import TimeReport,CSVData


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TimeReport
        fields = ['employee_id', 'start_date', 'end_date', 'amount_paid']


class CSVDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVData
        fields = ['date','hours_worked','employee_id','file_id','job_group']