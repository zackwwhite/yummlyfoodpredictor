from setuptools import setup, find_packages

setup(
	name = 'project2',
	version = '1.0',
	author = 'Zack White',
	author_email = 'zaq@ou.edu',
	packages = find_packages(exclude=('docs'))
)
