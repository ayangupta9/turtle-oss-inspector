from flask_cors import CORS
from flask import Flask, jsonify

from datetime import datetime
import json
from multiprocessing.pool import ThreadPool
import os
from flask import appcontext_popped

# from utils.dependency_check.main import execute_dependency_check
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

# from utils.dependency_check.main import execute_dependency_check
from utils.license_and_security.license import license_stats
from utils.license_and_security.security import check_security_files
from utils.maintenance.main import project_maintained
from utils.packaging.main import check_if_repo_is_package
from utils.dependency_check.main import get_vuln_dependencies_of_repo


pool = ThreadPool(processes=11)

GITHUB_ACCESS_TOKEN = "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"
g = Github(GITHUB_ACCESS_TOKEN)


# github.enable_console_debug_logging()


app = Flask(__name__)
CORS(app=app)


def main():

    # * DECLARE REPOSITORY WITH OWENER NAME AND REPO NAME IN THIS FORMAT ->
    #                  {owner_name/repo_name}
    # repo = g.get_repo("ayangupta9/oss_test_repo")
    # repo2 = g.get_repo("ayangupta9/ieee_gcet_backend")
    # repo3 = g.get_repo("nodejs/node")
    repo4 = g.get_repo("expressjs/express")
    license_repo = g.get_repo("spdx/license-list-data")

    # for org in list(g.get_user('ayangupta9').get_orgs()):

    # * TESTS

    # ! html done
    binary_artifacts_result = pool.apply_async(
        get_binaries, args=(repo4,)
    )  # * BINARY ARTIFACTS TEST

    branch_protection_result = pool.apply_async(
        get_branch_protection, args=(repo4,)
    )  # * BRANCH PROTECTION

    # ! html done
    badge_result = pool.apply_async(
        cii_badge, args=(repo4,)
    )  # * CII BEST PRACTICES BADGES

    code_review_result = pool.apply_async(
        get_code_review, args=(repo4,)
    )  # * BASIC CODE & REPO REVIEW

    contri_result = pool.apply_async(
        get_contributors_stats, args=(repo4,)
    )  # * CONTRIBUTORS REVIEW

    dep_up_tool_result = pool.apply_async(
        has_dependency_update_tool, args=(repo4,)
    )  # * DEPENDENCY UPDATE TOOL CHECK

    dep_check = pool.apply_async(
        get_vuln_dependencies_of_repo, args=(repo4,)
    )  # * OWASP DEPENDENCY CHECK

    license_result = pool.apply_async(
        license_stats,
        args=(
            repo4,
            license_repo,
        ),
    )  # * LICENSE CHECK

    security_result = pool.apply_async(
        check_security_files, args=(repo4,)
    )  # * SECURITY CHECK

    maintenance_result = pool.apply_async(
        project_maintained, args=(repo4,)
    )  # * MAINTENANCE CHECK

    repo_is_pack_result = pool.apply_async(
        check_if_repo_is_package, args=(repo4,)
    )  # * PACKAGE CHECK

    criticality_score_result = pool.apply_async(
        get_repository_score_from_raw_stats, args=(repo4,)
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

    RESULTS_WEIGHTS = {
        "BINARY_ARTIFACTS_RESULT": 1,
        "BRANCH_PROTECTION_RESULT": 1
        if branch_protection_result["payload"]["signal"] == True
        else 0,
        "BADGE_RESULT": 2,
        "CODE_REVIEW_RESULT": 1,
        "CONTRI_RESULT": 1,
        "DEP_UP_TOOL_RESULT": 1,
        "DEP_CHECK": 3,
        "LICENSE_RESULT": 0,
        "SECURITY_RESULT": 0,
        "MAINTENANCE_RESULT": 1,
        "REPO_IS_PACK_RESULT": 1,
        "CRITICALITY_SCORE_RESULT": 2,
    }

    print("All completed")

    # * CUMULATION OF RESULTS
    final_result = {
        "BINARY_ARTIFACTS_RESULT": binary_artifacts_result.__dict__,
        "BRANCH_PROTECTION_RESULT": branch_protection_result.__dict__,
        "BADGE_RESULT": badge_result.__dict__,
        "CODE_REVIEW_RESULT": code_review_result.__dict__,
        "CONTRI_RESULT": contri_result.__dict__,
        "DEP_UP_TOOL_RESULT": dep_up_tool_result.__dict__,
        "DEP_CHECK": dep_check.__dict__,
        "LICENSE_RESULT": license_result.__dict__,
        "SECURITY_RESULT": security_result.__dict__,
        "MAINTENANCE_RESULT": maintenance_result.__dict__,
        "REPO_IS_PACK_RESULT": repo_is_pack_result.__dict__,
        "CRITICALITY_SCORE_RESULT": criticality_score_result.__dict__,
    }

    result = 0
    for key, stats in RESULTS_WEIGHTS.items():
        result += RESULTS_WEIGHTS[key]
    # print(final_result)
    final_score = 0
    for key, stats in final_result.items():
        print(stats)
        final_score += stats["score"] * RESULTS_WEIGHTS[key]
    # _{datetime.now().__str__().split('.')[0]

    # update final_result with final score
    final_result["FINAL_SCORE"] = final_score
    final_result["TOTAL_SCORE"] = result
    final_result["RESULT_SCORE"] = final_score / result

    # * RESULTS DUMPED INTO JSON AND SAVED
    with open(
        # f"{repo.owner.login}_{repo.name.__str__()}_result.json",
        f"public\\assets\\reports\\{repo4.owner.login}_{repo4.name.__str__()}.json",
        "w",
    ) as open_file:
        print("Writing data in json file")
        json.dump(final_result, open_file)
        print("Data completely written.\n")


def start():
    # init()
    main()


start()
# ms = get_vuln_dependencies_of_repo()

# if __name__ == "__main__":


# init()
