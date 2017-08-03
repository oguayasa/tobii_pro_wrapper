from distutils.core import setup


setup(
    name='tobii_pro_wrapper',
    version='0.1',
    author='Olivia Guayasamin',
    author_email='oguayasa@gmail.com',
    packages=['tobii_pro_wrapper'],
    url='https://github.com/oguayasa/tobii_pro_wrapper',
    license='LICENSE.txt',
    description='Wrapper for the new Tobii Pro SDK',
    long_description='README.md',
    install_requires=[
        'numpy',
        'scipy',
        'psychopy',
        'datetime',
        'random',
        'collections',
        'win32api',
        'tobii_research',
    ],
)
