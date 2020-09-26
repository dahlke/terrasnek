import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="terrasnek",
    version="0.0.8",
    author="Neil Dahlke",
    author_email="neil.dahlke+terrasnek@gmail.com",
    description="A Python client for the Terraform Cloud API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dahlke/terrasnek",
    packages=setuptools.find_packages(),
    # packages=[
        # "requests==2.21.0",
        # "pylint==2.3.1",
        # "coverage==4.5.4",
        # "coverage-badge==1.0.1",
        # "twine==1.13.0",
        # "wheel==0.33.4",
        # "setuptools==41.1.0",
        # "sphinx==3.0.3",
        # "recommonmark==0.6.0",
        # "beautifulsoup4==4.9.1",
        # "tabulate==0.8.7",
        # "timeout-decorator==0.4.1",
        # "anybadge==1.7.0"
    # ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
)