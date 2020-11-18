import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="terrasnek",
    version="0.0.10",
    author="Neil Dahlke",
    author_email="neil.dahlke+terrasnek@gmail.com",
    description="A Python client for the Terraform Cloud API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dahlke/terrasnek",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests==2.21.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
)