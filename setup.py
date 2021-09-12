from setuptools import setup

setup(name='managor',
      version='0.0.1',
      description='Reusable code to build a Pulumi stack with an S3 backend',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration'
      ],
      url='http://www.kenjenney.com',
      author='Ken Jenney',
      author_email='me@kenjenney.com',
      license='MIT',
      packages=['managor'],
      install_requires=[
        'argparse',
        'pulumi',
        'pulumi-aws',
        'encrytor @ git+https://github.com/kjenney/encryptor.git'
      ],
      zip_safe=False)
