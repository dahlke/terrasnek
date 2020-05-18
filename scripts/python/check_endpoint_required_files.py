#!/bin/python3

import os
import requests

from bs4 import BeautifulSoup

TFC_API_BASE_URL = "https://www.terraform.io"
TFC_API_PREFIX = "docs/cloud/api"

def get_endpoints_from_api_docs():
    req = requests.get(f"{TFC_API_BASE_URL}/{TFC_API_PREFIX}/index.html")
    soup = BeautifulSoup(req.text, features="html.parser")
    sidebar = soup.find(id="docs-sidebar")
    endpoints = {}

    for links in sidebar.find_all('a'):
        api_path = links.get('href')
        if TFC_API_PREFIX in api_path:
            endpoint_name = api_path.split("/")[-1].replace(".html", "").replace("-", "_")
            endpoints[endpoint_name] = {}
            endpoints[endpoint_name]["url"] = f"{TFC_API_BASE_URL}/{api_path}"

    return endpoints

def main():
    endpoints = get_endpoints_from_api_docs()

    endpoint_map = {}
    endpoints_filenames = os.listdir("./terrasnek/")

    for filename in endpoints_filenames:
        filename = filename.replace(".py", "")

        if filename[0] != "_"  and filename[0] != "." \
            and filename != "api" and filename != "endpoint" \
            and filename != "exceptions":
            endpoint_map[filename] = {}
            endpoint_map[filename]["endpoint"] = True

    tests_filenames = os.listdir("./test/")
    for filename in tests_filenames:
        filename = filename.replace("_test.py", "")

        if filename in endpoint_map:
            if filename[0] != "_"  and filename[0] != ".":
                endpoint_map[filename]["test"] = True

    docs_filenames = os.listdir("./docs/")
    for filename in docs_filenames:
        filename = filename.replace(".md", "")

        if filename in endpoint_map:
            if filename[0] != "_"  and filename[0] != ".":
                endpoint_map[filename]["docs"] = True

    for ep_name in endpoint_map:
        ep = endpoint_map[ep_name]

        if "docs" not in ep:
            print(ep_name, "needs docs.")

        if "test" not in ep:
            print(ep_name, "needs a test.")

if __name__ == "__main__":
    main()
