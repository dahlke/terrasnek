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
    with open("./lint_output.txt", "r") as f:
        lint_results = f.read()
    lint_results_list = [i for i in lint_results.split("\n") if i]
    score_line = lint_results_list[-1]
    score = float(score_line.replace("Your code has been rated at ", "")\
        .split(" ")[0].split("/")[0]) / 10
    return score

# TODO: make sure all the version numbers are the same and match the branch?
def check_versions():
    pass

def main():
    """
    Retrieve the coverage and lint scores, and compare them to the tolerable
    thresholds.
    """
    coverage_score = get_coverage_score()
    lint_score = get_lint_score()

    meets_coverage = coverage_score >= MIN_COVERAGE_SCORE
    meets_lint = lint_score >= MIN_LINT_SCORE

    err_msg_list = []
    if not meets_coverage:
        err_msg_list.append(\
            f"The coverage score {coverage_score} \
                does not meet the coverage threshold {MIN_COVERAGE_SCORE}.")

    if not meets_lint:
        err_msg_list.append(\
            f"The lint score {lint_score} does not meet the lint threshold {MIN_LINT_SCORE}.")

    if err_msg_list:
        print("\n".joins(err_msg_list), "Exiting.")
        sys.exit(1)
    else:
        print("Coverage score and lint score both meet their thresholds.")

if __name__ == "__main__":
    main()
