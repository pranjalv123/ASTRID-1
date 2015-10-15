from distutils.core import setup
from distutils.command.install import install

class install_with_distmethods(install):
    def run(self):
        install.run(self)
        import subprocess
        import sys
        subprocess.call('bash ' + sys.path[0] + '/src/distmethods/install.sh', shell=True) 

setup(name="ASTRID",
      version="1.0",
      author="Pranjal Vachaspati",
      author_email="pr@nj.al",
      url="https://github.com/pranjalv123/ASTRID",
      package_dir={'ASTRID':'src'},
      package_data={'':['distmethods/install.py', 'distmethods/install.sh']},
      packages=['ASTRID'],
      scripts=['ASTRID'],
      license='GPLv3',
      cmdclass={'install':install_with_distmethods}
      )
