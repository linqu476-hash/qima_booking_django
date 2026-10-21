# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = (
    collect_submodules("apps")
    + collect_submodules("config")
    + ["waitress", "whitenoise", "whitenoise.middleware"]
)

a = Analysis(
    ["launcher.py"],
    pathex=["."],
    binaries=[],
    datas=[
        ("templates", "templates"),
        ("staticfiles", "staticfiles"),
        # Django migrations are loaded from files, so keep them as data too
        ("apps", "apps"),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter"],
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="QimaBooking",
    debug=False,
    strip=False,
    upx=False,
    console=True,  # set False once everything works to hide the console window
    onefile=True,
)
