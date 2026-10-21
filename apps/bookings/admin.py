from django.contrib import admin
from .models import BookingRun
@admin.register(BookingRun)
class BookingRunAdmin(admin.ModelAdmin):
 list_display=('id','status','user','created_at','started_at','finished_at')
 list_filter=('status','created_at')
 readonly_fields=('created_at','started_at','finished_at','log_text','workspace')
