from setuptools import setup

setup(name='spongebob',
      version='0.1.3',
      description='DeSCriPTiOn (OpTiONaL)',
      url='https://github.com/ltskinner/spongebob',
      author='ltskinner',
      license='MIT',
      install_requires=['docx2txt', 'python-docx'],
      packages=['spongebob'],
      package_data={'': ['spongebob.jpg', 'banner.txt']},
      zip_safe=False)

