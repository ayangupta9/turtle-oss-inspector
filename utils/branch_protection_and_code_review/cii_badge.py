# ! https://bestpractices.coreinfrastructure.org/projects.json
# ! https://bestpractices.coreinfrastructure.org/projects.json?url=https%3A%2F%2Fgithub.com%2Fnodejs%2Fnode

from github import Repository
import requests

from components.classes.MetricSignal import MetricSignal


def cii_badge(repo: Repository.Repository):
    cii_best_practices_url = (
        "https://bestpractices.coreinfrastructure.org/projects.json?url="
    )
    cii_badge_results = {}

    ms = MetricSignal()

    cii_project_url = cii_best_practices_url + repo.clone_url.split(".git")[0]
    data = requests.get(cii_project_url)
    if data.status_code == 200:
        if len(data.json()) > 0:
            cii_data = data.json()[0]
            if "implementation_languages" in cii_data:
                cii_badge_results["implementation_languages"] = cii_data[
                    "implementation_languages"
                ].split(", ")
            if "tiered_percentage" in cii_data:
                cii_badge_results["tiered_percentage"] = cii_data["tiered_percentage"]
            if "badge_level" in cii_data:
                cii_badge_results["badge_level"] = cii_data["badge_level"]

    else:
        ms.message = "Could not get data"

    if len(cii_badge_results.keys()) > 0:
        ms.signal = True
        ms.payload = cii_badge_results
        ms.message = "Found CII Best practice badges"
    else:
        ms.signal = False
        ms.message = "Found no badges"
