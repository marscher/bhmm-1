"""
BHMM: A toolkit for Bayesian hidden Markov model analysis of single-molecule trajectories.

"""
from __future__ import print_function
import os
import sys
from distutils.version import StrictVersion
from setuptools import setup, Extension, find_packages
import numpy
import glob
from os.path import relpath, join
import subprocess
from Cython.Build import cythonize

DOCLINES = __doc__.split("\n")

########################
VERSION = "0.1.0"
ISRELEASED = False
__version__ = VERSION
########################
CLASSIFIERS = """\
Development Status :: 3 - Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: Lesser GNU Public License (LGPL)
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Scientific/Engineering :: Bio-Informatics
Topic :: Scientific/Engineering :: Chemistry
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""

################################################################################
# Writing version control information to the module
################################################################################

def git_version():
    # Return the git revision as a string
    # copied from numpy setup.py
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = 'Unknown'

    return GIT_REVISION


def write_version_py(filename='bhmm/version.py'):
    cnt = """
# This file is automatically generated by setup.py
short_version = '%(version)s'
version = '%(version)s'
full_version = '%(full_version)s'
git_revision = '%(git_revision)s'
release = %(isrelease)s

if not release:
    version = full_version
"""
    # Adding the git rev number needs to be done inside write_version_py(),
    # otherwise the import of numpy.version messes up the build under Python 3.
    FULLVERSION = VERSION
    if os.path.exists('.git'):
        GIT_REVISION = git_version()
    else:
        GIT_REVISION = 'Unknown'

    if not ISRELEASED:
        FULLVERSION += '.dev-' + GIT_REVISION[:7]

    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION,
                       'full_version': FULLVERSION,
                       'git_revision': GIT_REVISION,
                       'isrelease': str(ISRELEASED)})
    finally:
        a.close()

################################################################################
# USEFUL SUBROUTINES
################################################################################

def find_package_data(data_root, package_root):
    files = []
    for root, dirnames, filenames in os.walk(data_root):
        for fn in filenames:
            files.append(relpath(join(root, fn), package_root))
    return files


################################################################################
# SETUP
################################################################################


#try:
#    import pyemma
#    print(pyemma.__version__)
#    if not StrictVersion(pyemma.__version__) >= '1.1.2':
#        raise ImportError
#except:
#    print('Bulding and running bhmm requires pyemma >= 1.1.2. Install first.')
#    sys.exit(1) 


#cython_ext = cythonize(Extension('bhmm.msm.tmatrix_sampling',
#                       		 sources = ['./bhmm/msm/tmatrix_sampling.pyx'],
#                       		 include_dirs = [numpy.get_include()]))
extensions = [Extension('bhmm.hidden.impl_c.hidden',
                        sources = ['./bhmm/hidden/impl_c/hidden.pyx',
                                   './bhmm/hidden/impl_c/_hidden.c'],
                        include_dirs = ['/bhmm/hidden/impl_c/',numpy.get_include()]),
	      Extension('bhmm.output_models.impl_c.gaussian',
                        sources = ['./bhmm/output_models/impl_c/gaussian.pyx',
                                   './bhmm/output_models/impl_c/_gaussian.c'],
                        include_dirs = ['/bhmm/output_models/impl_c/',numpy.get_include()]),
	      Extension('bhmm.msm.tmatrix_sampling',
			sources = ['./bhmm/msm/tmatrix_sampling.pyx'],
			include_dirs = [numpy.get_include()])]


write_version_py()
setup(
    name='bhmm',
    author='John Chodera and Frank Noe',
    author_email='john.chodera@choderalab.org',
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
    version=__version__,
    license='LGPL',
    url='https://github.com/choderalab/bhmm',
    platforms=['Linux', 'Mac OS-X', 'Unix', 'Windows'],
    classifiers=CLASSIFIERS.splitlines(),
    package_dir={'bhmm': 'bhmm'},
    #packages=['bhmm', "bhmm.tests"] + ['bhmm.%s' % package for package in find_packages('bhmm')],
    packages=['bhmm', 'bhmm.tests', 'bhmm.msm', 'bhmm.hidden', 'bhmm.init', 'bhmm.msm', 'bhmm.output_models', 'bhmm.output_models.impl_c', 'bhmm.util', 'bhmm.hidden.impl_python', 'bhmm.hidden.impl_c'],
    # + ['bhmm.%s' % package for package in find_packages('bhmm')],
    package_data={'bhmm': find_package_data('examples', 'bhmm')},  # NOTE: examples installs to bhmm.egg/examples/, NOT bhmm.egg/bhmm/examples/.  You need to do utils.get_data_filename("../examples/*/setup/").
    zip_safe=False,
    install_requires=[
        'cython',
        'numpy',
        'scipy',
        'pyemma>=1.2',
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'nose',
        'docopt>=0.6.1',
        ],
    ext_modules = cythonize(extensions),
    #ext_modules=[cext2]#cext1,
#		 Extension('bhmm.ml.lib.c',
#			   sources=['./bhmm/ml/lib/c/extension.c', './bhmm/ml/lib/c/hmm.c'],
#			   include_dirs = [numpy.get_include()]),
#		] + cext
    )

