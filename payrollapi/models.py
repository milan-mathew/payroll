from django.db import models

# Create your models here.

# class FileUpload(models.Model):
#     """Represents file upload model class."""

#     # owner = models.CharField(max_length=250)
#     file = models.FileField(upload_to='csv_uploads/%y/%m')
#     created = models.DateTimeField(auto_now_add=True)
#     file_id = models.IntegerField(max_length=50)

#     def __str__(self):
#         return self.file.name

class CSVData(models.Model):
    date = models.DateField()
    hours_worked = models.DecimalField(max_digits=10, decimal_places=0)
    employee_id = models.IntegerField()
    job_group = models.CharField(max_length=10)
    file_id = models.IntegerField()

    def __str__(self):
        return f"date: {self.date}, hours_worked: {self.hours_worked}, employee_id: {self.employee_id}, file_id: {self.file_id}"

class TimeReport(models.Model):
    employee_id = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Employee ID: {self.employee_id}, Start Date: {self.start_date}, End Date: {self.end_date}, Amount Paid: {self.amount_paid}"
