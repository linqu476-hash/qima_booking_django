"""Entry point for the one-file Windows build of qima_booking."""
import os
import sys
import threading
import webbrowser
from pathlib import Path

PORT = 8765


def base_dir() -> Path:
    # PyInstaller unpacks bundled files to sys._MEIPASS
    return Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))


def data_dir() -> Path:
    root = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "QimaBooking"
    (root / "storage").mkdir(parents=True, exist_ok=True)
    return root


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    os.environ["QIMA_BASE_DIR"] = str(base_dir())
    os.environ["QIMA_DATA_DIR"] = str(data_dir())
    os.environ.setdefault("CELERY_TASK_ALWAYS_EAGER", "1")

    import django

    django.setup()
    from django.core.management import call_command

    call_command("migrate", interactive=False, verbosity=0)

    from config.wsgi import application
    from waitress import serve

    threading.Timer(1.5, lambda: webbrowser.open(f"http://127.0.0.1:{PORT}")).start()
    print(f"QIMA Booking running at http://127.0.0.1:{PORT}  (close this window to stop)")
    serve(application, host="127.0.0.1", port=PORT)


if __name__ == "__main__":
    main()
