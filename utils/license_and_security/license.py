import json
from github import Repository

from components.classes.MetricSignal import MetricSignal


def get_spdx_license_list(licenses_repo: Repository.Repository):
    #  = g.get_repo("spdx/license-list-data")

    licenses_content_file = licenses_repo.get_contents("json/licenses.json")
    licenses_list = json.loads(licenses_content_file.decoded_content)["licenses"]

    processed_license_list = {}
    keys = ["isDeprecatedLicenseId", "licenseId", "isOsiApproved", "name", "reference"]
    for license in licenses_list:
        processed_license_list[license["licenseId"]] = {
            key: license[key] for key in keys
        }

    return processed_license_list


def license_stats(repo: Repository.Repository, license_repo: Repository.Repository):
    license_list = get_spdx_license_list(licenses_repo=license_repo)
    license_stats_results = {}
    ms = MetricSignal()
    license_score = 0

    try:
        license = repo.get_license()
        license_stats_results["exists"] = True
        license_stats_results["repo_license"] = license.license.raw_data
        license_score += 1
        spdx_license = license_list.get(license.license.spdx_id, None)
        if spdx_license:
            license_stats_results["license_data"] = spdx_license
            if spdx_license["isDeprecatedLicenseId"] == False:
                license_score += 1
            if spdx_license["isOsiApproved"] == True:
                license_score += 1
            ms.signal = True
            ms.message = "License data fetched"

        else:
            ms.signal = False
            license_stats_results["license_data"] = None
    except:
        ms.signal = False
        license_stats_results["exists"] = False

    ms.payload = {
        "license_stats_results": license_stats_results,
        "license_score": license_score,
    }

    print("Completed license")

    return ms
