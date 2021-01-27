#!/bin/python3
"""
This script is used in pre-commit hooks as well as the CircleCI tests to make
sure that we fail out if we don't meet the minimum percentage threshold we
define for coverage or linting. It is meant to be self contained.
"""

import sys
import xml.etree.ElementTree as ET

MIN_COVERAGE_SCORE = 0.9
MIN_LINT_SCORE = 0.9


def get_coverage_score():
    """
    Get the coverage score from the coverage output, return it.
    """
    tree = ET.parse("./coverage.xml")
    root = tree.getroot()
    line_rate = float(root.attrib["line-rate"])
    return line_rate


def get_lint_score():
    """
    Get the lint score from the pylint output, return it.
    """
    lint_results = ""

    with open("./lint_output.txt", "r") as infile:
        lint_results = infile.read()

    lint_results_list = [i for i in lint_results.split("\n") if i]
    score_line = lint_results_list[-1]
    score = float(score_line.replace("Your code has been rated at ", "")\
        .split(" ")[0].split("/")[0]) / 10

    return score


def check_versions():
    """
    Make sure all of the files that need to have the right version number in them
    have the right version number.
    """
    # TODO: check the git branch
    changelog_lines = []
    changelog_version = None

    setup_lines = []
    pypi_version = None

    conf_lines = []
    docs_version = None

    with open("./CHANGELOG.md", "r") as infile:
        changelog_lines = infile.readlines()

    for line in changelog_lines:
        if "##" in line:
            changelog_version = \
                line[line.find("[")+1:line.find("]")].strip()
            break

    with open("./setup.py", "r") as infile:
        setup_lines = infile.readlines()
        for line in setup_lines:
            if "version" in line:
                pypi_version = line.split('"')[1].strip()
                break

    with open("./docs/conf.py", "r") as infile:
        conf_lines = infile.readlines()
        for line in conf_lines:
            if "release" in line:
                docs_version = line.split("'")[1].strip()
                break

    return changelog_version, pypi_version, docs_version


def main():
    """
    Retrieve the coverage and lint scores, and compare them to the tolerable
    thresholds. Make sure all of the relevant files in this project reflect the
    same project version.
    """
    coverage_score = get_coverage_score()
    lint_score = get_lint_score()
    changelog_version, pypi_version, docs_version = check_versions()

    meets_coverage = coverage_score >= MIN_COVERAGE_SCORE
    meets_lint = lint_score >= MIN_LINT_SCORE
    version_match = changelog_version == pypi_version == docs_version

    err_msg_list = []
    if not meets_coverage:
        err_msg_list.append(\
            f"The coverage score {coverage_score} \
                does not meet the coverage threshold {MIN_COVERAGE_SCORE}.")

    if not meets_lint:
        err_msg_list.append(\
            f"The lint score {lint_score} does not meet the lint threshold {MIN_LINT_SCORE}.")

    if not version_match:
        err_msg_list.append(\
            f"The versions do not match across the important files (CHANGELOG.md, setup.py, docs/conf.py).")

    if err_msg_list:
        print("\n".join(err_msg_list), "Exiting.")
        sys.exit(1)
    else:
        print("Coverage score and lint score both meet their thresholds.")
        print("All of the versions match in the important files (CHANGELOG.md, setup.py, docs/conf.py).")

if __name__ == "__main__":
    main()
