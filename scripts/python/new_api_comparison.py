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

# Base URLs for scraping from GitHub
GITHUB_DOCS_BASE_URL = "https://github.com/hashicorp/terraform-website/tree/master/content/cloud-docs/api-docs"
GITHUB_DOCS_ADMIN_BASE_URL = "https://github.com/hashicorp/terraform-website/tree/master/content/cloud-docs/api-docs/admin"
RAW_GITHUB_DOCS_BASE_URL = "https://raw.githubusercontent.com/hashicorp/terraform-website/master/content/cloud-docs/api-docs"
RAW_GITHUB_DOCS_ADMIN_BASE_URL = "https://raw.githubusercontent.com/hashicorp/terraform-website/master/content/cloud-docs/api-docs/admin"

# Helpful constants for the parsing of the GitHub markdown docs
TFC_API_BASE_URL = "https://www.terraform.io/cloud-docs/api-docs"
HTTP_VERBS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
SKIPPABLE_GITHUB_TITLES = ["admin", "_template", "Go to parent directory", "changelog", "index", "stability-policy"]
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

def get_admin_docs():
    pass

def get_non_admin_docs():
    pass

def main():
    pass

# TODO: add comments to everything below.

if __name__ == "__main__":

    # Get the API index page, and pass it into Beautiful Soup
    # req = requests.get(f"{TFC_API_BASE_URL}/{TFC_API_PREFIX}/index.html")
    req = requests.get(f"{GITHUB_DOCS_BASE_URL}")
    soup = BeautifulSoup(req.text, features="html.parser")
    endpoints = {}

    row_headers = soup.find_all(role="rowheader")

    for row_header in row_headers:
        link = row_header.find("a")
        filename = link.get("title")
        title = filename.replace(".mdx", "")
        github_url = f"{RAW_GITHUB_DOCS_BASE_URL}/{filename}"
        docs_url = f"{TFC_API_BASE_URL}/{title}"

        if title not in SKIPPABLE_GITHUB_TITLES:
            endpoints[title] = {
                "filename": filename,
                "docs-url": docs_url,
                "github-url": github_url,
                "methods": {}
            }

    for ep_name in endpoints:
        ep = endpoints[ep_name]
        req = requests.get(ep["github-url"])
        method_names = []
        method_descriptions = []
        permalinks = []

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
                    "http-path": "",
                    "descriptions": [],
                    "permalink": ""
                }
            else:
                # TODO: this print statement will show some inconsistencies
                # print(ep_name, header)
                pass

        for codeblock in codeblocks:
            # TODO: this has to handle deprecated codeblocks, like registry modules
            if codeblock is not None:
                split_block = codeblock.text.split(" ")
                potential_http_verb = split_block[0]

                # Check that the first word in the code block is an HTTP verb and isn't _just_
                # an HTTP verb (like `PUT`).
                if potential_http_verb in HTTP_VERBS and len(split_block) > 1:
                    prev_method_header = codeblock.parent.find_previous_sibling('h2')

                    # NOTE: this is specifically for the delete modules endpoint, which has some weird formatting
                    # https://www.terraform.io/cloud-docs/api-docs/modules
                    # If we can't find a previous header in this level of the HTML, try going up one more level
                    if prev_method_header is None:
                        prev_method_header = codeblock.parent.parent.find_previous_sibling('h2')

                    ep["methods"][prev_method_header.text]["descriptions"].append(codeblock.text)

                    permalink_arg = prev_method_header.text.lower().replace(" ", "-")
                    permalink = f"{ep['docs-url']}#{permalink_arg}"
                    ep["methods"][prev_method_header.text]["permalink"] = permalink

        # print(ep)

    print(endpoints)


    main()
