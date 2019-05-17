import pathlib
import re

from setuptools import setup

ROOT = pathlib.Path(__file__).parent

with open(str(ROOT / "README.md"), encoding="utf-8") as f:
    LONG_DESC = f.read()

with open(str(ROOT / "requirements.txt"), encoding="utf-8") as f:
    REQS = f.read().splitlines()

with open(str(ROOT / "async_pokepy" / "__init__.py"), encoding="utf-8") as f:
    VERSION = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", f.read(), re.MULTILINE).group(1)

if not VERSION:
    raise RuntimeError("Version is not set.")

EXTRA_REQS = {
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
      version=VERSION,
      description="A simple asynchronous wrapper for the PokeAPI.co API.",
      long_description=LONG_DESC,
      long_description_content_type="text/markdown",
      keywords="async pokemon asyncio rest api",
      url="https://github.com/PendragonLore/async_pokepy",
      download_url="https://github.com/PendragonLore/async_pokepy/archive/{0}.tar.gz".format(VERSION),
      project_urls={
          "Issue Tracker": "https://github.com/PendragonLore/async_pokepy/issues",
          "Documentation": "https://async-pokepy.rtfd.io",
      },
      python_requires=">=3.5.3",
      platforms=["macOS", "POSIX", "Windows"],
      install_requires=REQS,
      include_package_data=True,
      license="MIT",
      extras_require=EXTRA_REQS,
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
