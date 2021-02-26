from setuptools import setup, find_packages
from djcelery_ses import __version__


setup(
    name='django-celery-ses',
    version=__version__,
    description="django-celery-ses",
    author='tzangms',
    author_email='tzangms@streetvoice.com',
    url='http://github.com/StreetVoice/django-celery-ses',
    license='MIT',
    test_suite='runtests.runtests',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "django >= 1.10, <= 1.11.29",
        "django-celery >= 3",
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
        'Environment :: Web Environment',
    ],
    keywords='django,celery,mail',
)
