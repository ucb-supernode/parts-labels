import os
env = Environment(ENV=os.environ)
Export('env')

# for some reason SCons always invokes Python27 on Command(python)...
env['PYTHON'] = "C:\Python34\python"

# Just a wrapper so generated files get dropped in the right directory.
SConscript('SConscript', variant_dir='generated')
