from django.conf import settings
from django.db import models
class BookingRun(models.Model):
 STATUS_CHOICES=[('queued','Queued'),('running','Running'),('done','Completed'),('failed','Failed')]
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
 status=models.CharField(max_length=16,choices=STATUS_CHOICES,default='queued',db_index=True)
 created_at=models.DateTimeField(auto_now_add=True)
 started_at=models.DateTimeField(null=True,blank=True)
 finished_at=models.DateTimeField(null=True,blank=True)
 booking_file=models.FileField(upload_to='runs/%Y/%m/%d/booking/',blank=True)
 booking_list_file=models.FileField(upload_to='runs/%Y/%m/%d/list/',blank=True)
 technical_info_file=models.FileField(upload_to='runs/%Y/%m/%d/technical/',blank=True)
 error_message=models.TextField(blank=True)
 log_text=models.TextField(blank=True)
 workspace=models.CharField(max_length=500,blank=True)
 class Meta:
  ordering=['-created_at']
 def __str__(self): return f'Run {self.pk} ({self.status})'
