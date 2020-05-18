#!/bin/python3

import os


def main():
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
