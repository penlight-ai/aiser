from setuptools import setup, find_packages

setup(
    name='aiser',
    version='0.2.0',
    url='https://github.com/penlight-ai/aiapi',
    author='Penlight AI Inc.',
    author_email='support@penlight.ai',
    description='Python package to serve AI agents and knowledge bases for Penlight AI.',
    long_description='Python package to serve AI agents and knowledge bases for Penlight AI.',
    packages=find_packages(),
    install_requires=[
        'uvicorn',
        'fastapi',
        'pyjwt[crypto]'
        'httpx',
    ],
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.11',
    ],
)
