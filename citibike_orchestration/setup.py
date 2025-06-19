from setuptools import find_packages, setup

setup(
    name="citibike_orchestration",
    packages=find_packages(exclude=["citibike_orchestration_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
