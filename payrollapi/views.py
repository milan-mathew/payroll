from django.shortcuts import render
from django.http import HttpResponse
from payrollapi.serializers import ReportSerializer, CSVDataSerializer
from payrollapi.models import TimeReport
import csv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CSVData
from datetime import datetime
from decimal import Decimal
import re
import calendar
class CSVUploadAPIView(APIView):
    def updateReport(self, date, hours_worked, employee_id, job_group):
        day = date.day
        month = date.month
        year = date.year
        amount = 0

        if (job_group == "A"):
          amount = Decimal(20) * Decimal(hours_worked)
        elif (job_group == "B"):
          amount = Decimal(30) * Decimal(hours_worked)

        start_day = 1
        end_day = 15
        if (day > 15):
            start_day = 16
            _, end_day = calendar.monthrange(year, month)

        start_date = f"{year}-{month}-{start_day}"
        end_date = f"{year}-{month}-{end_day}"
        
        time_report = TimeReport.objects.filter(employee_id = employee_id, start_date = start_date, end_date = end_date)

        if(time_report.exists()):
          data_found = time_report.values()
          time_report.update(amount_paid = data_found[0]['amount_paid'] + amount)
        else:
          time_report = TimeReport(employee_id = employee_id, start_date = start_date, end_date = end_date, amount_paid = amount)
          time_report.save()


    def post(self, request, format=None):
        csv_file = request.FILES['file']
        file_name = csv_file.name
        file_id = re.search('time-report-(\d+)\.csv', file_name).group(1)
        isFileExists = CSVData.objects.filter(file_id = file_id).exists()
        
        if (not isFileExists):
          decoded_file = csv_file.read().decode('utf-8').splitlines()
          csv_reader = csv.reader(decoded_file)
          next(csv_reader, None)

          product_list = []
          for row in csv_reader:
            date = datetime.strptime(row[0], "%d/%m/%Y").date()
            hours_worked = row[1]
            employee_id = row[2]
            job_group = row[3]
            product_list.append(
                CSVData(
                    file_id = file_id,
                    date = date,
                    hours_worked = hours_worked,
                    employee_id = employee_id,
                    job_group = job_group
                )
            )
            self.updateReport(
              date = date,
              hours_worked = hours_worked,
              employee_id = employee_id,  
              job_group = job_group
            )
          CSVData.objects.bulk_create(product_list)
          return Response({'message': 'CSV file uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
          return Response({'message': 'File already uploaded'}, status=status.HTTP_400_BAD_REQUEST)

class ReportAPIView(APIView):
    def get(self, request, format=None):
        data = TimeReport.objects.order_by('employee_id', 'start_date').values()
        result = [
            {
                "employeeId": d["employee_id"],
                "payPeriod": {
                    "startDate": d["start_date"],
                    "endDate": d["end_date"]
                },
                "amountPaid": d["amount_paid"]
            }
            for d in data
        ]

        output = {
            "payrollReport": {
                "employeeReports": result
            }
        }

        return Response(output, status=status.HTTP_200_OK)
        
