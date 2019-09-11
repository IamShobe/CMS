from setuptools import setup, find_packages

setup(
    name='CMS',
    version='0.1.0',
    url='https://github.com/IamShobe/car.git',
    author='Elran Shefer',
    author_email='elran777@gmail.com',
    description='Car Multimedia Software',
    packages=find_packages("src"),
    install_requires=[],
    package_dir={"": "src"},
    package_data={"web_template": ["static/*",
                          "static/img/*",
                          "static/font/*",
                          "templates/*"]},
)
