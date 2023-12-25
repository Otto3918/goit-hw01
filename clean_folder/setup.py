from setuptools import setup, find_namespace_packages

setup(name='clean_folder',
      version='0.0.1',
      description='Organizing your folder',
      url='https://github.com/Otto3918/clean_folder',
      author='Jury Skorynin',
      author_email='OttoUkr@ukr.net',
      license='MIT',
      packages=find_namespace_packages(),
      include_package_data=True,
      install_requires=['markdown'],
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']},
      zip_safe=False)