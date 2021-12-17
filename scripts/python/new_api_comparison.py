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

# Base URLs for scraping from GitHub
GITHUB_DOCS_BASE_URL = "https://github.com/hashicorp/terraform-website/tree/master/content/cloud-docs/api-docs"
GITHUB_DOCS_ADMIN_BASE_URL = "https://github.com/hashicorp/terraform-website/tree/master/content/cloud-docs/api-docs/admin"
RAW_GITHUB_DOCS_BASE_URL = "https://raw.githubusercontent.com/hashicorp/terraform-website/master/content/cloud-docs/api-docs"
RAW_GITHUB_DOCS_ADMIN_BASE_URL = "https://raw.githubusercontent.com/hashicorp/terraform-website/master/content/cloud-docs/api-docs/admin"

# Helpful constants for the parsing of the GitHub markdown docs
TFC_API_BASE_URL = "https://www.terraform.io/cloud-docs/api-docs"
HTTP_VERBS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
SKIPPABLE_GITHUB_TITLES = ["admin", "_template", "Go to parent directory", "changelog", "index", "stability-policy", "admin-index"]
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

        # TODO: modify the title names for admin and
        endpoint_name = filename

        if endpoint_name not in SKIPPABLE_GITHUB_TITLES:
            endpoint_name = endpoint_name.replace("organization", "org")
            endpoint_name = endpoint_name.replace("configuration", "config")
            endpoint_name = endpoint_name.replace("workspace-variables", "workspace-vars")
            endpoint_name = endpoint_name.replace("variables", "vars")
            endpoint_name = endpoint_name.replace("variable-sets", "var-sets")
            endpoint_name = endpoint_name.replace("team-members", "team-memberships")
            endpoint_name = endpoint_name.replace("modules", "registry-modules")
            endpoint_name = endpoint_name.replace("providers", "registry-providers")

            # if endpoint_name = "run":
                # endpoint_name = "runs"

            if is_admin:
                github_url = f"{RAW_GITHUB_DOCS_BASE_URL}/admin/{raw_filename}"
                docs_url = f"{TFC_API_BASE_URL}/admin/{endpoint_name}"
                endpoint_name = "admin-" + endpoint_name
            else:
                github_url = f"{RAW_GITHUB_DOCS_BASE_URL}/{raw_filename}"
                docs_url = f"{TFC_API_BASE_URL}/{endpoint_name}"

            endpoints[endpoint_name] = {
                "filename": raw_filename,
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
                    permalink = f"{ep['docs-url']}#{permalink_arg}"
                    ep["methods"][prev_method_header.text]["permalink"] = permalink

    return endpoints

def main():
    non_admin_endpoints = get_docs_from_github()
    admin_endpoints = get_docs_from_github(is_admin=True)

    # Merge the endpoint types
    all_endpoints = non_admin_endpoints.copy()
    all_endpoints.update(admin_endpoints)
    print(all_endpoints)


# TODO: add comments to everything below.

if __name__ == "__main__":
    main()
