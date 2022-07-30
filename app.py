# import requests
# from flask_cors import CORS
# from flask import Flask, jsonify

from datetime import datetime
import json
from multiprocessing.pool import ThreadPool
import os
from utils.dependency_check.main import execute_dependency_check
from github import Github
from utils.packaging.criticality_score.run import get_repository_score_from_raw_stats
from utils.binary_artifacts.binary_artifacts import get_binaries
from utils.branch_protection_and_code_review.branch_protection import (
    get_branch_protection,
)
from utils.branch_protection_and_code_review.cii_badge import cii_badge
from utils.branch_protection_and_code_review.review import get_code_review
from utils.contributors.main import get_contributors_stats
from utils.dependency_check.dependency_update_check import has_dependency_update_tool
from utils.dependency_check.main import execute_dependency_check
from utils.license_and_security.license import license_stats
from utils.license_and_security.security import check_security_files
from utils.maintenance.main import project_maintained
from utils.packaging.main import check_if_repo_is_package


pool = ThreadPool(processes=11)

GITHUB_ACCESS_TOKEN = "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"
g = Github(GITHUB_ACCESS_TOKEN)


# app = Flask(__name__)
# CORS(app=app)

def create_html_report():
    pass


def main():

    # * DECLARE REPOSITORY WITH OWENER NAME AND REPO NAME IN THIS FORMAT ->
    #                  {owner_name/repo_name}
    repo = g.get_repo("ayangupta9/oss_test_repo")
    license_repo = g.get_repo("spdx/license-list-data")

    # * TESTS

    # ! html done
    binary_artifacts_result = pool.apply_async(
        get_binaries, args=(repo,)
    )  # * BINARY ARTIFACTS TEST 

    branch_protection_result = pool.apply_async(
        get_branch_protection, args=(repo,)
    )  # * BRANCH PROTECTION

    # ! html done
    badge_result = pool.apply_async(
        cii_badge, args=(repo,)
    )  # * CII BEST PRACTICES BADGES

    code_review_result = pool.apply_async(
        get_code_review, args=(repo,)
    )  # * BASIC CODE & REPO REVIEW

    contri_result = pool.apply_async(
        get_contributors_stats, args=(repo,)
    )  # * CONTRIBUTORS REVIEW

    dep_up_tool_result = pool.apply_async(
        has_dependency_update_tool, args=(repo,)
    )  # * DEPENDENCY UPDATE TOOL CHECK

    dep_check = pool.apply_async(
        execute_dependency_check, args=(repo,)
    )  # * OWASP DEPENDENCY CHECK

    license_result = pool.apply_async(
        license_stats,
        args=(
            repo7,
            license_repo,
        ),
    )  # * LICENSE CHECK

    security_result = pool.apply_async(
        check_security_files, args=(repo,)
    )  # * SECURITY CHECK

    maintenance_result = pool.apply_async(
        project_maintained, args=(repo,)
    )  # * MAINTENANCE CHECK

    repo_is_pack_result = pool.apply_async(
        check_if_repo_is_package, args=(repo,)
    )  # * PACKAGE CHECK

    criticality_score_result = pool.apply_async(
        get_repository_score_from_raw_stats, args=(repo,)
    )  # * CRITICALITY SCORE

    # ! ALL CHECK RESULTS
    binary_artifacts_result = binary_artifacts_result.get()
    branch_protection_result = branch_protection_result.get()
    badge_result = badge_result.get()
    code_review_result = code_review_result.get()
    contri_result = contri_result.get()
    dep_up_tool_result = dep_up_tool_result.get()
    dep_check = dep_check.get()
    license_result = license_result.get()
    security_result = security_result.get()
    maintenance_result = maintenance_result.get()
    repo_is_pack_result = repo_is_pack_result.get()
    criticality_score_result = criticality_score_result.get()

    # * CUMULATION OF RESULTS
    final_result = {
        "binary_artifacts_result": binary_artifacts_result.__dict__,
        "branch_protection_result": branch_protection_result.__dict__,
        "badge_result": badge_result.__dict__,
        "code_review_result": code_review_result.__dict__,
        "contri_result": contri_result.__dict__,
        "dep_up_tool_result": dep_up_tool_result.__dict__,
        "dep_check": dep_check.__dict__,
        "license_result": license_result.__dict__,
        "security_result": security_result.__dict__,
        "maintenance_result": maintenance_result.__dict__,
        "repo_is_pack_result": repo_is_pack_result.__dict__,
        "criticality_score_result": criticality_score_result.__dict__,
    }

    # * RESULTS DUMPED INTO JSON AND SAVED
    with open(
        f"{repo.owner.login}_{repo.name.__str__()}_result_{datetime.now().__str__().split('.')[0]}.json",
        "w",
    ) as open_file:
        print("Writing data in json file")
        json.dump(final_result, open_file)
        print("Data completely written.\n")


def init():
    cloned_repos_path = "cloned_repos\\"
    cloned_repos_dir_exists = os.path.exists(cloned_repos_path)

    if not cloned_repos_dir_exists:
        os.mkdir(cloned_repos_path)

    dependency_check_reports_path = "dc_output_reports\\"
    dc_reports_dir_exists = os.path.exists(dependency_check_reports_path)

    if not dc_reports_dir_exists:
        os.mkdir(dependency_check_reports_path)


init()
