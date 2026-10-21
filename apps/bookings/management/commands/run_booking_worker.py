import os, shutil, subprocess, time
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.bookings.models import BookingRun

class Command(BaseCommand):
 help='Run the single QIMA booking automation worker. Keep one worker instance.'
 def add_arguments(self,parser): parser.add_argument('--poll-seconds',type=float,default=2.0)
 def handle(self,*args,**opts):
  while True:
   run=BookingRun.objects.filter(status='queued').order_by('created_at').first()
   if not run:
    time.sleep(opts['poll_seconds']); continue
   # Conditional update prevents two workers from claiming the same queued job.
   changed=BookingRun.objects.filter(pk=run.pk,status='queued').update(status='running',started_at=timezone.now())
   if not changed: continue
   run.refresh_from_db()
   try: self.execute_run(run)
   except Exception as exc:
    run.status='failed'; run.error_message=str(exc)[:2000]; run.finished_at=timezone.now(); run.save(update_fields=['status','error_message','finished_at'])
 def execute_run(self,run):
  root=Path(settings.BASE_DIR)/'data'/'workspaces'/str(run.pk)
  auto=root/'automation'; inputs=auto/'input'; pdf_dir=inputs/'po_pdf'; logs=auto/'logs'
  if root.exists(): shutil.rmtree(root)
  shutil.copytree(Path(settings.BASE_DIR)/'automation',auto,ignore=shutil.ignore_patterns('__pycache__','*.pyc','logs'))
  inputs.mkdir(parents=True,exist_ok=True); pdf_dir.mkdir(parents=True,exist_ok=True); logs.mkdir(parents=True,exist_ok=True)
  for field,dest in [(run.booking_file,inputs/'booking.xlsx'),(run.booking_list_file,inputs/'booking_list.xlsx'),(run.technical_info_file,inputs/'technical_info.xlsx')]:
   if field and field.name:
    with field.open('rb') as source, dest.open('wb') as target: shutil.copyfileobj(source,target)
  if run.workspace:
   for f in Path(run.workspace).glob('*.pdf'): shutil.copy2(f,pdf_dir/f.name)
  env=os.environ.copy(); env.update({'HEADLESS':os.getenv('QIMA_HEADLESS','true'),'DRY_RUN':os.getenv('QIMA_DRY_RUN','true'),'QIMA_USER':os.getenv('QIMA_USER',''),'QIMA_PASS':os.getenv('QIMA_PASS',''),'PYTHONUNBUFFERED':'1'})
  # Explicit env vars from deployment config are passed to the existing automation unchanged.
  proc=subprocess.Popen([os.getenv('PYTHON_EXECUTABLE','python'),'main.py'],cwd=auto,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
  lines=[]
  try:
   for line in proc.stdout:
    lines.append(line)
    run.log_text=''.join(lines)[-100000:]
    run.save(update_fields=['log_text'])
   rc=proc.wait(timeout=int(os.getenv('QIMA_TIMEOUT_SECONDS','3600')))
  except Exception:
   proc.kill(); proc.wait(); raise
  run.log_text=''.join(lines)[-100000:]
  run.status='done' if rc==0 else 'failed'
  if rc: run.error_message=f'Automation exited with code {rc}. Review logs.'
  run.finished_at=timezone.now(); run.save(update_fields=['log_text','status','error_message','finished_at'])
  # Copy results into the run's private file directory for later download.
  dest=Path(settings.MEDIA_ROOT)/'run_results'/str(run.pk); dest.mkdir(parents=True,exist_ok=True)
  for folder in [inputs,logs]:
   if folder.exists(): shutil.copytree(folder,dest/folder.name,dirs_exist_ok=True)
