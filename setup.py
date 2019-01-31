from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext
from Cython.Build import cythonize
from os import name as os_name

if os_name == 'nt':
    #windows requires static links for exported symbols
    ext_list = ['src/*.pyx', 'src/rvo2.cpp', 'src/RVOSimulator.cpp',  'src/KdTree.cpp', 'src/Obstacle.cpp', 'src/Agent.cpp']
else:
    #unix is smarter
    ext_list = ['src/*.pyx']

class BuildRvo2Ext(_build_ext):
    """Builds RVO2 before our module."""

    def run(self):
        # Build RVO2
        import os
        import os.path
        import subprocess

        build_dir = os.path.abspath('build/RVO2')
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
            subprocess.check_call(['cmake', '../..'],
                                  cwd=build_dir)
        subprocess.check_call(['cmake', '--build', '.', '--config', 'Release'], cwd=build_dir)

        _build_ext.run(self)



extensions = [
    Extension('rvo2', ext_list,
              include_dirs=['src'],
              libraries=['RVO'],
              library_dirs=['build/RVO2/src', 'build/RVO2/src/Release'],
              extra_compile_args=[]),
]

setup(
    name="pyrvo2",
    ext_modules=cythonize(extensions),
    cmdclass={'build_ext': BuildRvo2Ext},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Cython',
        'Topic :: Games/Entertainment :: Simulation',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
