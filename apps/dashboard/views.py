import os, shutil
from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import get_valid_filename
from apps.bookings.models import BookingRun
from apps.bookings.services import create_run

@login_required
def dashboard(request):
 runs=BookingRun.objects.filter(user=request.user) if not request.user.is_staff else BookingRun.objects.all()
 return render(request,'dashboard/index.html',{'runs':runs[:50]})

@login_required
def new_run(request):
 if request.method=='POST':
  try:
   pdfs=request.FILES.getlist('po_pdfs')
   run,pdfs=create_run(user=request.user,booking_file=request.FILES.get('booking_file'),booking_list_file=request.FILES.get('booking_list_file'),technical_info_file=request.FILES.get('technical_info_file'),po_pdfs=pdfs)
   # Store PDF inputs in a private run-specific directory; worker copies all files into its workspace.
   pdf_dir=Path(settings.MEDIA_ROOT)/'run_pdfs'/str(run.pk)
   pdf_dir.mkdir(parents=True,exist_ok=True)
   names=[]
   for f in pdfs:
    name=get_valid_filename(Path(f.name).name)
    dest=pdf_dir/name
    with dest.open('wb') as target:
     for chunk in f.chunks(): target.write(chunk)
    names.append(name)
   run.workspace=str(pdf_dir)
   run.save(update_fields=['workspace'])
   messages.success(request,f'Run #{run.pk} queued. The automation worker will pick it up.')
   return redirect('run_detail',pk=run.pk)
  except (ValidationError,ValueError) as exc:
   messages.error(request,' '.join(getattr(exc,'messages',[str(exc)])))
 return render(request,'dashboard/new_run.html')

@login_required
def run_detail(request,pk):
 run=get_object_or_404(BookingRun,pk=pk)
 if not request.user.is_staff and run.user_id != request.user.id: raise Http404
 files=[]
 if run.workspace:
  p=Path(run.workspace)
  if p.is_dir(): files=[x.name for x in p.iterdir() if x.is_file()]
 return render(request,'dashboard/run_detail.html',{'run':run,'files':files})

@login_required
def run_file(request,pk,relative_path):
 run=get_object_or_404(BookingRun,pk=pk)
 if not request.user.is_staff and run.user_id != request.user.id: raise Http404
 root=Path(run.workspace).resolve() if run.workspace else None
 if not root: raise Http404
 target=(root/relative_path).resolve()
 if root not in target.parents or not target.is_file(): raise Http404
 return FileResponse(target.open('rb'),as_attachment=True,filename=target.name)
