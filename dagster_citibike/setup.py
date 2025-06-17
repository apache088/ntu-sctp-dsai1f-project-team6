from setuptools import find_packages, setup

setup(
    name="dagster_citibike",
    packages=find_packages(exclude=["dagster_citibike_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
