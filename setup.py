from setuptools import setup, find_packages
from svcelery_email import __version__


setup(
    name='streetvoice-celery-email',
    version=__version__,
    description="streetvoice-celery-email",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='django,celery,mail',
    author='tzangms',
    author_email='tzangms@gmail.com',
    url='http://github.com/tzangms/streetvoice-celery-email',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
