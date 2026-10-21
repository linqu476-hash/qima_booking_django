"""Shared booking service: validates uploads and queues work for the single worker."""
from pathlib import Path
from django.core.exceptions import ValidationError
from .models import BookingRun
MAX_UPLOAD_BYTES=25*1024*1024

def validate_upload(upload, allowed_exts, required=False):
 if not upload:
  if required: raise ValidationError('This file is required.')
  return
 if Path(upload.name).suffix.lower() not in allowed_exts:
  raise ValidationError(f'Unsupported file type for {upload.name}.')
 if upload.size > MAX_UPLOAD_BYTES:
  raise ValidationError(f'{upload.name} exceeds the 25 MB upload limit.')

def create_run(*, user, booking_file, booking_list_file, technical_info_file=None, po_pdfs=None):
 validate_upload(booking_file,{'.xlsx'},True)
 validate_upload(booking_list_file,{'.xlsx'},True)
 validate_upload(technical_info_file,{'.xlsx'})
 if not po_pdfs: raise ValidationError('Upload at least one PO PDF.')
 for pdf in po_pdfs: validate_upload(pdf,{'.pdf'},True)
 run=BookingRun.objects.create(user=user,booking_file=booking_file,booking_list_file=booking_list_file,technical_info_file=technical_info_file)
 # PDFs are saved under the run's private workspace by the view before worker execution.
 return run, po_pdfs
