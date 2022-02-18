import cx_Freeze
import sys


base = None
if (sys.platform == "win32"):
    base = "Win32GUI" 
exe = [cx_Freeze.Executable(script="geopip/manage.py",base=base)]

cx_Freeze.setup( name = "django", version = "1.0", options = {"build_exe": {"packages": ['asyncio'], "include_files": []}
    }, executables = exe )