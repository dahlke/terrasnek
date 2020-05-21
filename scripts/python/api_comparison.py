#!/bin/python3
"""
This script is _extremely_ custom, and really meant to be used as a sanity
check. The get_endpints_from_api_docs is particularly brittle, so this will
likely need to be updated often and should not be relied upon for any testing,
just quick lookups.
"""

import os
import requests

from tabulate import tabulate
from bs4 import BeautifulSoup

TFC_API_BASE_URL = "https://www.terraform.io"
TFC_API_PREFIX = "docs/cloud/api"
HTTP_VERBS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def get_relevant_clean_filenames(dir_name, filename_ignore=[]):
    """
    List a directory, and return all filenames that don't start with a "." or "_",
    and also don't match the explict filenames to ignore.
    """
    prefix_ignore = [".", "_"]
    valid_filenames = []

    # List all the files in the directory
    filenames = os.listdir(dir_name)
    for filename in filenames:
        # Remove all the relevant file extensions, as well as the test postfix.
        filename = filename.replace(".py", "")
        filename = filename.replace(".md", "")
        filename = filename.replace("_test", "")
        valid_prefix = True
        valid_filename = True

        # Check that the filename doesn't have an invalid prefix
        for prefix in prefix_ignore:
            if filename[0] == prefix:
                valid_prefix = False
                break

        # Check that the filename isn't explicitly ignorable.
        for ignorable in filename_ignore:
            if filename == ignorable:
                valid_filename = False
                break

        # If it's a valid filename, add it to our valid filenames array.
        if valid_prefix and valid_filename:
            valid_filenames.append(filename)

    return valid_filenames


def get_endpoints_from_api_docs():
    """
    Scrape the Terraform Cloud API docs to get all of the published and documented
    endpoints. Clean the URL slugs to match the file naming convention for this project.
    Return a dict of the endpoint names and their URLs, as well as all of the methods for
    the endpoint.

    This method is the most brittle of everything here. If anything changes on the API
    Docs website, this will stop working.
    """
    req = requests.get(f"{TFC_API_BASE_URL}/{TFC_API_PREFIX}/index.html")
    soup = BeautifulSoup(req.text, features="html.parser")
    sidebar = soup.find(id="docs-sidebar")
    endpoints = {}

    for links in sidebar.find_all('a'):
        api_path = links.get('href')
        is_admin = "admin" in api_path
        if TFC_API_PREFIX in api_path:
            endpoint_name = api_path.split("/")[-1].replace(".html", "").replace("-", "_")

            # Replace the URL strings with the ones I used in the library for conciseness.
            endpoint_name = endpoint_name.replace("organization", "org")
            endpoint_name = endpoint_name.replace("configuration", "config")
            endpoint_name = endpoint_name.replace("variables", "vars")
            endpoint_name = endpoint_name.replace("workspace_vars", "vars")
            endpoint_name = endpoint_name.replace("team_members", "team_memberships")
            endpoint_name = endpoint_name.replace("modules", "registry_modules")

            if endpoint_name == "run":
                endpoint_name = "runs"

            if is_admin:
                endpoint_name = "admin_" + endpoint_name

            # Ignore some of the links from the API that don't represent endpoints
            if endpoint_name not in ["index", "stability_policy", "admin_index"]:
                endpoints[endpoint_name] = {}
                endpoints[endpoint_name]["url"] = f"{TFC_API_BASE_URL}{api_path}"

    for ep_name in endpoints:
        endpoint = endpoints[ep_name]
        url = endpoint["url"]

        req = requests.get(url)
        soup = BeautifulSoup(req.text, features="html.parser")
        inner = soup.find(id="inner")
        codeblocks = inner.find_all("code")

        endpoint["method_descriptions"] = []
        for codeblock in codeblocks:
            contents = codeblock.contents[0]
            if not callable(contents):
                split_contents = contents.split(" ")
                if split_contents is not None:
                    potential_verb = split_contents[0]
                    if potential_verb in HTTP_VERBS:
                        endpoint["method_descriptions"].append(contents)

    return endpoints

def main():
    endpoints = get_endpoints_from_api_docs()

    # Check for an implementation file for each endpoint
    implementation_filenames = \
        get_relevant_clean_filenames("./terrasnek/", filename_ignore=["endpoint", "api", "exceptions"])
    for filename in implementation_filenames:
        if filename in endpoints:
            endpoints[filename]["implementation"] = True

    # Check for an test file for each endpoint
    tests_filenames = \
        get_relevant_clean_filenames("./test/", filename_ignore=["secrets", "base", "index"])
    for filename in tests_filenames:
        if filename in endpoints:
            endpoints[filename]["test"] = True

    # Check for an docs file for each endpoint
    docs_filenames = \
        get_relevant_clean_filenames("./docs/", filename_ignore=[])
    for filename in docs_filenames:
        if filename in endpoints:
            endpoints[filename]["docs"] = True

    # Loop through all the data we compiled on our files compared to the API
    # docs and tell us what is missing.
    for ep_name in endpoints:
        endpoint = endpoints[ep_name]
        needs = []

        if "implementation" not in endpoint:
            needs.append("implementation")

        if "test" not in endpoint:
            needs.append("test")

        if "docs" not in endpoint:
            needs.append("docs")

        if needs:
            print(ep_name, "needs", ", ".join(needs), endpoint["url"])


    headers = ["Endpoint Name", "Module Name", "Implemented", "Test", "Docs", "Spec"]
    rows = []

    for ep_name in endpoints:
        endpoint = endpoints[ep_name]
        rows.append([
            ep_name.replace("_", " ").title(),
            ep_name,
            "implementation" in endpoint,
            "test" in endpoint,
            "docs" in endpoint,
            endpoint["url"]
        ])

    with open("./API_COMPARISON.md", "w") as f:
        table_data = tabulate(rows, headers=headers, tablefmt="github")
        print(table_data)
        f.write(table_data)

if __name__ == "__main__":
    main()
