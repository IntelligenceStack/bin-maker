from setuptools import setup, find_packages

setup(
    name='bin-maker',
    version='2.0.0',
    description='protect and speed up python source code',
    py_modules=["bin_maker"],
    long_description="protect and speed up python source code",
    url='https://github.com/IntelligenceStack/bin-maker.git',
    author='umaru',
    author_email='15875339926@139.com',
    classifiers=[],
    keywords='',
    install_requires=['cython', 'PyInstaller', 'logzero'],
    extras_require={},
    packages=find_packages(),
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': [
            'bin-maker-build=bin_maker.build:build',
            'bin-maker-release=bin_maker.action:release',
            'bin-maker-package=bin_maker.action:package',
        ],
    },
    project_urls={},
)
