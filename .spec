# streamlit_app.spec

from PyInstaller.utils.hooks import collect_all
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

# Analysis step
a = Analysis(
    ['Variation_Generator.py'],  # Your main Python script
    pathex=['.'],  # Path to your script
    binaries=[],  # No binaries initially
    datas=[],  # No datas initially
    hiddenimports=['itertools', 'streamlit.components.v1', 'numpy', 'pyarrow'],  # Hidden imports
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Pack Python modules into one package
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Create the final executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Variation_Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set this to False if you want a windowed app without a console
    onefile=True  # This ensures it packages everything as a single .exe file
)

# Collect only datas for now to avoid unpacking error
_, streamlit_datas, _ = collect_all('streamlit')

# Now COLLECT follows the EXE
coll = COLLECT(
    exe,
    a.binaries,  # Keep binaries empty for now to isolate the issue
    a.scripts,
    a.pure,
    a.zipfiles,
    a.datas + streamlit_datas,  # Only collect the data part
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Variation_Generator',
    excludes=['_internal/rpds']
)
