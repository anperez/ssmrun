import setuptools

requirements = [
    'Click>=6.0',
    'boto3>=1.3.1'
]

setuptools.setup(
    name="ssmrun",
    version="0.1.1",
    url="https://github.com/Fullscreen/ssmrun",

    author="Fullscreen Devops",
    author_email="devops@fullscreen.com",

    description="Utilities for AWS EC2 SSM",
    long_description=open('README.rst').read(),

    packages=[
        'ssmrun',
    ],
    package_dir={'ssmrun':
                 'ssmrun'},
    entry_points={
        'console_scripts': [
            'ssm=ssmrun.cli:main'
        ]
    },

    install_requires=requirements,
    license="MIT license",

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
