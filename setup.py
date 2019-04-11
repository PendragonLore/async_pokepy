import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="async_pokepy",
    version="0.0.4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PendragonLore/async_pokepy",
    python_requires=">=3.5.0",
    install_requires="aiohttp>=3.3.0,<=3.6.0",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
)
