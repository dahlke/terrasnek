#!/bin/python3
"""
This script is _extremely_ custom, and really meant to be used as a sanity
check. The get_endpints_from_api_docs is particularly brittle, so this will
likely need to be updated often and should not be relied upon for any testing,
just quick lookups. It is meant to be self contained.
"""

import os
import json
import requests
import anybadge

from tabulate import tabulate
from bs4 import BeautifulSoup

TFC_API_BASE_URL = "https://www.terraform.io"
TFC_API_PREFIX = "docs/cloud/api"
IMPLEMENTATION_PATH = "./terrasnek"
TEST_PATH = "./test"
DOCS_PATH = "./docs"
HTTP_VERBS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def get_valid_filenames_in_dir(dir_name, prefix_ignore=[".", "_"], filename_ignore=[]):
    """
    List a directory, and return all filenames that don't start with a "." or "_",
    and also don't match the explict filenames to ignore.
    """
    valid_filenames = []

    # List all the files in the directory
    filenames = os.listdir(dir_name)
    remove_from_filenames = [".py", ".md", "_test"]

    for filename in filenames:
        # Remove all the relevant file extensions, as well as the test postfix.
        for suffix in remove_from_filenames:
            filename = filename.replace(suffix, "")

        valid_prefix = filename[0] not in prefix_ignore
        valid_filename = filename not in filename_ignore

        # If it's a valid filename, add it to our valid filenames array.
        if valid_prefix and valid_filename:
            valid_filenames.append(filename)

    return valid_filenames

def scrape_endpoint_info():
    """
    Scrape the Terraform Cloud API docs to get all of the published and documented
    endpoints. Clean the URL slugs to match the file naming convention for this project.
    Return a dict of the endpoint names and their URLs, as well as all of the methods for
    the endpoint.

    This method is the most brittle of everything here. If anything changes on the API
    Docs website, this will stop working.
    """

    # Get the API index page, and pass it into Beautiful Soup
    req = requests.get(f"{TFC_API_BASE_URL}/{TFC_API_PREFIX}/index.html")
    soup = BeautifulSoup(req.text, features="html.parser")

    # Get the sidebar from the page, it has all the API endpoint names in it.
    sidebar = soup.find(id="docs-sidebar")

    # Declare the endpoint map which we will add to below.
    endpoints = {}

    # Start looping through all the links in the sidebar.
    for links in sidebar.find_all('a'):
        # Get the URL that the link points to.
        api_path = links.get('href')

        # Check to see if it's an admin link, this is used later.
        is_admin = "admin" in api_path

        if TFC_API_PREFIX in api_path:
            # If it's a valid API path, get the endpoint name from the end of the URL.
            endpoint_name = api_path.split("/")[-1].replace(".html", "").replace("-", "_")

            # Replace the URL strings with the ones I used in the library for conciseness.
            endpoint_name = endpoint_name.replace("organization", "org")
            endpoint_name = endpoint_name.replace("configuration", "config")
            endpoint_name = endpoint_name.replace("workspace_variables", "workspace_vars")
            endpoint_name = endpoint_name.replace("variables", "vars")
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

    # Now with each endpoint named and mapped to a URL with the description
    # of methods on the endpoint, we need to pull in the methods.
    for ep_name in endpoints:
        endpoint = endpoints[ep_name]
        url = endpoint["url"]

        # Retrieve the API docs page for a specific endpoint, pass it into
        # Beautiful Soup.
        req = requests.get(url)
        soup = BeautifulSoup(req.text, features="html.parser")

        # Comments
        inner = soup.find(id="inner")
        codeblocks = inner.find_all("code")

        endpoint["methods"] = []
        for codeblock in codeblocks:
            contents = codeblock.contents[0]
            if not callable(contents):
                split_contents = contents.split(" ")

                if split_contents is not None:
                    potential_verb = split_contents[0]
                    if potential_verb in HTTP_VERBS:
                        method_desc = None
                        method_permalink = None

                        method_header = codeblock.parent.find_previous_sibling('h2')
                        if method_header is not None:
                            method_desc = method_header.find('a')

                        if method_desc is not None:
                            method_permalink = method_desc.get('href')
                            method_desc = method_header.contents[-1].replace("\n", "").strip()

                        endpoint["methods"].append({
                            "http-path": contents,
                            "description": method_desc,
                            "permalink": method_permalink
                        })

    return endpoints


def check_contributor_requirements(endpoints):
    """
    With the endpoint info we scraped from the API docs, check that each endpoint
    has an implementation, a test, and docs.
    """
    # Check for an implementation file for each endpoint
    implementation_filenames = \
        get_valid_filenames_in_dir(IMPLEMENTATION_PATH, \
            filename_ignore=["endpoint", "api", "exceptions"])
    for filename in implementation_filenames:
        if filename in endpoints:
            endpoints[filename]["implementation"] = True

    # Check for an test file for each endpoint
    tests_filenames = \
        get_valid_filenames_in_dir(TEST_PATH, filename_ignore=["secrets", "base", "index"])
    for filename in tests_filenames:
        if filename in endpoints:
            endpoints[filename]["test"] = True

    # Check for an docs file for each endpoint
    docs_filenames = \
        get_valid_filenames_in_dir(DOCS_PATH, filename_ignore=[])
    for filename in docs_filenames:
        if filename in endpoints:
            endpoints[filename]["docs"] = True

    return endpoints

def check_methods_implementation(endpoints):
    """
    With the endpoint info we scraped from the API docs, check that each method
    in the docs has an implementation.
    """

    for ep_name in endpoints:
        endpoint = endpoints[ep_name]
        endpoint_methods = endpoint["methods"]
        path = f"{IMPLEMENTATION_PATH}/{ep_name}.py"
        file_contents = ""
        split_by_func_def = []

        if os.path.exists(path):
            with open(path, "r") as infile:
                file_contents = infile.read()
                split_by_func_def = file_contents.split("\n")

        for method in endpoint_methods:
            path = method["http-path"]
            method["implemented"] = False
            method["implementation-method-name"] = None
            most_recent_method_name = None


            for line in split_by_func_def:
                if "def" in line:
                    most_recent_method_name = line.split("(")[0].replace("def", "").strip()

                if path in line:
                    method["implemented"] = True
                    method["implementation-method-name"] = most_recent_method_name
                    break

    return endpoints

def write_table_to_file(path, rows, headers, tablefmt):
    """
    Helper function to write table data to a file.
    """
    with open(path, "w") as outfile:
        table_data = tabulate(rows, headers=headers, tablefmt=tablefmt)
        outfile.write("# `terrasnek` API Coverage Completeness\n\n")
        outfile.write(table_data)
        outfile.write("\n")

def write_pretty_json_to_file(path, data):
    """
    Helper function to write pretty JSON to a file.
    """
    with open(path, "w") as outfile:
        pretty_json = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        outfile.write(pretty_json)

def main():
    """
    Main function to check the implemementation files herein this repo
    and what is specced out in the TFC API docs.
    """
    endpoints = scrape_endpoint_info()
    endpoints = check_contributor_requirements(endpoints)
    endpoints = check_methods_implementation(endpoints)

    write_pretty_json_to_file("./ref/data/endpoint_data.raw.json", endpoints)

    # High level comparison which shows if the endpoint is implemented at all.
    # Build a markdown table for GitHub display
    endpoint_headers = [
        "Endpoint",
        "Module",
        "Has Implementation",
        "Has Test",
        "Has Docs"
    ]
    endpoint_rows = []
    for ep_name in endpoints:
        endpoint = endpoints[ep_name]
        endpoint_rows.append([
            f'[{ep_name.replace("_", " ").title()}]({endpoint["url"]})',
            f'`{ep_name}`',
            "implementation" in endpoint,
            "test" in endpoint,
            "docs" in endpoint
        ])

    endpoint_rows.sort(key=lambda x: x[0])
    write_table_to_file("./CONTRIBUTING_REQS_TABLE.md", endpoint_rows, endpoint_headers, "github")

    md_method_headers = [
        "API Endpoint",
        "Method Description",
        "HTTP Method",
        "Terrasnek Method",
        "Implemented"
    ]
    md_method_rows = []
    for ep_name in endpoints:
        endpoint = endpoints[ep_name]
        for method in endpoint["methods"]:
            method_name = None

            if method["implementation-method-name"] is not None:
                method_name = f'`{ep_name}.{method["implementation-method-name"]}`'

            md_method_row = [
                ep_name.replace("_", " ").title(),
                f'[{method["description"]}]({endpoint["url"]}{method["permalink"]})',
                f'`{method["http-path"]}`',
                method_name,
                method["implemented"]
            ]
            md_method_rows.append(md_method_row)

    md_method_rows.sort(key=lambda x: x[0])
    write_table_to_file("./TERRASNEK_API_COVERAGE_COMPLETENESS.md", \
        md_method_rows, md_method_headers, "github")

    # Build an RST table for the Sphinx Python Docs
    rst_method_headers = [
        "API Endpoint",
        "Method Description",
        "HTTP Method",
        "Terrasnek Method",
        "Implemented",
        "Permalink"
    ]
    rst_method_rows = []
    for ep_name in endpoints:
        endpoint = endpoints[ep_name]
        for method in endpoint["methods"]:
            method_name = None
            if method["implementation-method-name"] is not None:
                method_name = f'`{ep_name}.{method["implementation-method-name"]}`'

            rst_method_row = [
                ep_name.replace("_", " ").title(),
                f'`{method["description"]}`',
                f'`{method["http-path"]}`',
                method_name,
                method["implemented"],
                f'{endpoint["url"]}{method["permalink"]}'
            ]
            rst_method_rows.append(rst_method_row)

    rst_method_rows.sort(key=lambda x: x[0])
    write_table_to_file("./docs/TERRASNEK_API_COVERAGE_COMPLETENESS.rst", \
        rst_method_rows, rst_method_headers, "rst")

    # Write a badge for the # of implemented methods vs the total # of method endpoints
    num_methods_implemented = 0
    num_total_methods = 0
    for ep_name in endpoints:
        endpoint = endpoints[ep_name]
        for method in endpoint["methods"]:
            num_total_methods += 1
            if method["implemented"]:
                num_methods_implemented += 1

    badge_text = f"{num_methods_implemented}/{num_total_methods} API endpoints implemented"
    print(badge_text)
    implemented_pct = round(((num_methods_implemented / num_total_methods) * 100), 2)
    badge = anybadge.Badge(badge_text, f"{implemented_pct}%", default_color="lightgrey")
    badge.write_badge("api_endpoints_implemented.svg", overwrite=True)

if __name__ == "__main__":
    main()
