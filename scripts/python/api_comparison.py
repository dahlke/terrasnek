#!/bin/python3
"""
This script is _extremely_ custom, and really meant to be used as a sanity
check. The get_endpints_from_api_docs is particularly brittle, so this will
likely need to be updated often and should not be relied upon for any testing,
just quick lookups. It is meant to be self contained.
"""

import os
import sys
import json
import requests
import anybadge
import markdown

from tabulate import tabulate
from bs4 import BeautifulSoup

# TODO: clean up the variable names in this script
# TODO: expecting 240+ endpoints, nowhere near that right now - admin endpoints?
# TODO: break this out into more files so it's moer consumable, and just generally clean it up
# TODO: handling multiple http-paths need to be sorted out
# TODO: add all sorts of comments here.

# NOTE: This api_comparison tool was updated in v0.1.8.

# Base URLs for scraping from GitHub
GITHUB_DOCS_BASE_URL = "https://github.com/hashicorp/terraform-docs-common/tree/main/website/docs/cloud-docs/api-docs"

GITHUB_DOCS_ADMIN_BASE_URL = "https://github.com/hashicorp/terraform-docs-common/tree/main/website/docs/cloud-docs/api-docs/admin"
RAW_GITHUB_DOCS_BASE_URL = "https://raw.githubusercontent.com/hashicorp/terraform-docs-common/main/website/docs/cloud-docs/api-docs"
RAW_GITHUB_DOCS_ADMIN_BASE_URL = "https://raw.githubusercontent.com/hashicorp/terraform-docs-common/main/website/docs/cloud-docs/api-docs/admin"

# Helpful constants for the parsing of the GitHub markdown docs
TFC_API_BASE_URL = "https://www.terraform.io/cloud-docs/api-docs"
HTTP_VERBS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
SKIPPABLE_GITHUB_TITLES = [
    "admin",
    "_template",
    "Go to parent directory",
    "changelog",
    "index",
    "stability_policy",
    "admin_index"
]
SKIPPABLE_MD_HEADERS = [
    "Attributes",
    "IP Ranges Payload", # ip-ranges
    "Terraform Cloud Registry Implementation", # modules
    "Sample Response",
    "Available Related Resources",
    "Notification Triggers", # notification-configurations
    "Notification Payload", # notification-configurations
    "Notification Authenticity", # notification-configurations
    "Notification Verification and Delivery Responses", # notification-configurations
    "Relationships",
    "Organization Membership", # team-members
    "Required Permissions", # run-tasks
]

# Paths for checking against implementations, tests and docs
IMPLEMENTATION_PATH = "./terrasnek"
TEST_PATH = "./test"
DOCS_PATH = "./docs"


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

def get_docs_from_github(is_admin=False):
    # Get the API index page, and pass it into Beautiful Soup
    # req = requests.get(f"{TFC_API_BASE_URL}/{TFC_API_PREFIX}/index.html")
    url = GITHUB_DOCS_ADMIN_BASE_URL if is_admin else GITHUB_DOCS_BASE_URL
    req = requests.get(f"{url}")
    soup = BeautifulSoup(req.text, features="html.parser")
    endpoints = {}

    row_headers = soup.find_all(role="rowheader")

    for row_header in row_headers:
        link = row_header.find("a")
        raw_filename = link.get("title")
        filename = raw_filename.replace(".mdx", "")

        endpoint_name = filename.replace("-", "_")

        if endpoint_name not in SKIPPABLE_GITHUB_TITLES:
            endpoint_name = endpoint_name.replace("organization", "org")
            endpoint_name = endpoint_name.replace("configuration", "config")
            endpoint_name = endpoint_name.replace("workspace_variables", "workspace_vars")
            endpoint_name = endpoint_name.replace("variables", "vars")
            endpoint_name = endpoint_name.replace("variable_sets", "var_sets")
            endpoint_name = endpoint_name.replace("team_members", "team_memberships")
            endpoint_name = endpoint_name.replace("modules", "registry_modules")
            endpoint_name = endpoint_name.replace("providers", "registry_providers")

            # NOTE: The implementation uses "runs" and the documentation uses "run"
            if endpoint_name == "run":
                endpoint_name = "runs"

            if is_admin:
                github_url = f"{RAW_GITHUB_DOCS_BASE_URL}/admin/{raw_filename}"
                docs_url = f"{TFC_API_BASE_URL}/admin/{filename}"
                endpoint_name = "admin_" + endpoint_name
            else:
                github_url = f"{RAW_GITHUB_DOCS_BASE_URL}/{raw_filename}"
                docs_url = f"{TFC_API_BASE_URL}/{filename}"

            endpoints[endpoint_name] = {
                "docs-url": docs_url,
                "github-url": github_url,
                "methods": {}
            }

    for ep_name in endpoints:
        ep = endpoints[ep_name]
        req = requests.get(ep["github-url"])

        md_html = markdown.markdown(req.text)
        soup = BeautifulSoup(md_html, features="html.parser")
        method_headers = soup.find_all("h2")
        codeblocks = soup.find_all("code")

        for header in method_headers:
            method_header = header.text

            if "page_title" not in method_header and \
                method_header not in SKIPPABLE_MD_HEADERS and \
                    method_header not in ep["methods"]:
                ep["methods"][header.text] = {
                    "http-paths": [],
                    "permalink": ""
                }
            else:
                # NOTE: This print statement will show some inconsistencies, like the skippable MD headers
                # print(ep_name, header)
                pass

        for codeblock in codeblocks:
            if codeblock is not None:
                split_block = codeblock.text.split(" ")
                potential_http_verb = split_block[0]

                # Check that the first word in the code block is an HTTP verb and isn't _just_
                # an HTTP verb (like `PUT`).
                if potential_http_verb in HTTP_VERBS and len(split_block) > 1:
                    prev_method_header = codeblock.parent.find_previous_sibling('h2')

                    # If we can't find a previous header in this level of the HTML, try going up one more level
                    # This is specifically for the delete modules endpoint, which has some weird formatting
                    # https://www.terraform.io/cloud-docs/api-docs/modules
                    if prev_method_header is None:
                        prev_method_header = codeblock.parent.parent.find_previous_sibling('h2')

                    ep["methods"][prev_method_header.text]["http-paths"].append(codeblock.text)
                    permalink_arg = prev_method_header.text.lower().replace(" ", "-")
                    docs_url = ep["docs-url"] if ep_name != "registry-modules" else "modules"
                    permalink = f"{docs_url}#{permalink_arg}"
                    ep["methods"][prev_method_header.text]["permalink"] = permalink

        for method_header in list(ep["methods"]):
            method = ep["methods"][method_header]

            # TODO: this may need to get re-worked later since it's just to get rid of false positives.
            # If there is no matching HTTP path, then remove this method.
            if len(method["http-paths"]) == 0:
                del ep["methods"][method_header]

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
        stripped_filename = filename.replace(".rst", "")
        if stripped_filename in endpoints:
            endpoints[stripped_filename]["docs"] = True

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

        for method_header in endpoint_methods:
            method = endpoint_methods[method_header]

            if method["http-paths"]:
                # TODO: manage where there are multiple http-paths
                path = method["http-paths"][0]
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
            else:
                print(method_header, method, "\n\n")

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
    non_admin_endpoints = get_docs_from_github()
    admin_endpoints = get_docs_from_github(is_admin=True)

    # Merge the endpoint types
    endpoints = non_admin_endpoints.copy()
    endpoints.update(admin_endpoints)
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

    # TODO: make sure implementation and test and docs work
    for ep_name in endpoints:
        endpoint = endpoints[ep_name]
        endpoint_rows.append([
            f'[{ep_name.replace("_", " ").title()}]({endpoint["docs-url"]})',
            f'`{ep_name}`',
            "implementation" in endpoint,
            "test" in endpoint,
            "docs" in endpoint
        ])

    endpoint_rows.sort(key=lambda x: x[0])
    write_table_to_file("./CONTRIBUTING_REQS_TABLE.md", endpoint_rows, endpoint_headers, "github")

    md_method_headers = [
        "API Endpoint",
        "Endpoint Description",
        "HTTP Method",
        "Terrasnek Method",
        "Implemented"
    ]
    md_method_rows = []
    for ep_name in endpoints:
        endpoint = endpoints[ep_name]
        for method_header in endpoint["methods"]:
            method = endpoint["methods"][method_header]
            method_name = None

            if method["implementation-method-name"] is not None:
                method_name = f'`{ep_name}.{method["implementation-method-name"]}`'

            md_method_row = [
                ep_name.replace("_", " ").replace("-", " ").title(),
                f"[{method_header}]({method['permalink']})",
                method["http-paths"][0],
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
        "Endpoint Description",
        "HTTP Method",
        "Terrasnek Method",
        "Implemented",
        "Permalink"
    ]
    rst_method_rows = []
    for ep_name in endpoints:
        endpoint = endpoints[ep_name]
        for method_header in endpoint["methods"]:
            method = endpoint["methods"][method_header]
            method_name = None

            if method["implementation-method-name"] is not None:
                method_name = f'`{ep_name}.{method["implementation-method-name"]}`'

            rst_method_row = [
                ep_name.replace("_", " ").title(),
                f'`{method_header}`',
                f'`{method["http-paths"][0]}`',
                method_name,
                method["implemented"],
                method["permalink"]
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
        for method_header in endpoint["methods"]:
            method = endpoint["methods"][method_header]
            num_total_methods += 1
            if method["implemented"]:
                num_methods_implemented += 1

    badge_text = f"{num_methods_implemented}/{num_total_methods} API endpoints implemented"
    print(badge_text)
    implemented_pct = round(((num_methods_implemented / num_total_methods) * 100), 2)
    badge = anybadge.Badge(badge_text, f"{implemented_pct}%", default_color="lightgrey")
    badge.write_badge("api_endpoints_implemented.svg", overwrite=True)

    # We want this to error if we fall below 99% coverage so we know we have to do work
    if implemented_pct <= 97:
        sys.exit(1)

if __name__ == "__main__":
    main()
