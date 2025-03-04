# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['cfUpdater.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
<<<<<<< HEAD
    optimize=0,
=======
>>>>>>> 9ddd53d3262b2947f845068ea0d1273a4ec59dd4
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='cfUpdater',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
<<<<<<< HEAD
    console=False,
=======
    console=True,
>>>>>>> 9ddd53d3262b2947f845068ea0d1273a4ec59dd4
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
