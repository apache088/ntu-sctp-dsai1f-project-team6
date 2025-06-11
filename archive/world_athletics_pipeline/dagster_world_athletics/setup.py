from setuptools import find_packages, setup

setup(
    name="dagster_world_athletics",
    packages=find_packages(exclude=["dagster_world_athletics_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        'meltano',
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
