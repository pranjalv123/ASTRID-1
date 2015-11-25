from setuptools import setup
from setuptools.command.install import install
from setuptools.extension import Extension
from Cython.Distutils import build_ext

import numpy

class install_with_distmethods(install):
    def run(self):
        install.run(self)
        import subprocess
        import sys
        import ASTRID
        import os
        dir = os.path.dirname(ASTRID.DistanceMethods.__file__)
        print "Installing distance methods to " + dir 
        subprocess.call('bash ' + dir + '/distmethods/install.sh', shell=True) 

setup(name="astrid-phylo",
      version="1.1",
      author="Pranjal Vachaspati",
      author_email="pr@nj.al",
      url="https://github.com/pranjalv123/ASTRID",
      description='Accurate Species TRee Reconstruction with Internode Distances',
      package_dir={'ASTRID':'src'},
      package_data={'':['distmethods/install.py', 'distmethods/install.sh']},
      packages=['ASTRID'],
      scripts=['ASTRID'],
      license='GPLv3',
      cmdclass={'install':install_with_distmethods,
                'build_ext': build_ext
            },
      ext_modules = [Extension("fastdm",
                            sources=["src/fdm.pyx"],
                            include_dirs=[numpy.get_include()],
                               language = "c++")],
      )
