# find_packages
# https://setuptools.pypa.io/en/latest/setuptools.html#using-find-packages
# https://stackoverflow.com/questions/43253701/python-packaging-subdirectories-not-installed
from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name    = 'krxpy',
    version = '0.0.1',
    license = 'MIT',
    description = "KRX Data Scraping ...",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/YongBeomKim',
    author = 'momukji lab',
    author_email = 'ybkim@momukji.com',
    keywords = ['krxpy'],
    python_requires = '>=3',
    include_package_data = True,
    package_data = {'': ['json/*.json']}, # 파일추가
    packages = find_packages(
        exclude = ['jupyter', 'backup', '.vscode', '.ipynb_checkpoints']
    ),
    install_requires=[
        'pytip',
        'pandas==2.0.2',
        'tqdm',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
