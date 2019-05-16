import re

from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("async_pokepy/__init__.py") as f:
    version = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError("Version is not set.")

extra = {
    "docs": [
        "sphinx",
        "sphinxcontrib.napoleon",
        "sphinxcontrib-asyncio",
    ],
    "tests": [
        "flake8",
        "pylint",
        "pytest",
        "pytest-cov",
        "isort"
    ]
}

setup(author="Lorenzo",
      name="async_pokepy",
      version=version,
      description="A simple asynchronous wrapper for the PokeAPI.co API.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      keywords="async pokemon asyncio rest api",
      url="https://github.com/PendragonLore/async_pokepy",
      project_urls={
          "Issue Tracker": "https://github.com/PendragonLore/async_pokepy/issues",
          "Documentation": "https://async-pokepy.rtfd.io",
      },
      python_requires=">=3.5.3",
      install_requires=requirements,
      include_package_data=True,
      license="MIT",
      extras_require=extra,
      packages=["async_pokepy", "async_pokepy.types"],
      classifiers=[
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Intended Audience :: Developers",
          "Topic :: Internet",
          "Topic :: Software Development :: Libraries",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Utilities",
          "Framework :: AsyncIO",
          "Operating System :: OS Independent",
          "Development Status :: 3 - Alpha",
      ],
      )
