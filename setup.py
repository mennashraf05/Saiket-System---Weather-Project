from setuptools import setup, find_packages

setup(
    name="weather-open-meteo",
    version="0.1.0",
    description="Command-line weather application using Open-Meteo API",
    author="Your Name",
    author_email="youremail@example.com",
    py_modules=["weather_open_meteo"],
    install_requires=[
        "requests>=2.0",
        "aiohttp>=3.0",
        "matplotlib>=3.0",
    ],
    entry_points={
        "console_scripts": [
        "weather_open_meteo=weather_open_meteo:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
