import requests
from github import Github, Repository
from pprint import pprint

# import xkcd2347
from tqdm import tqdm
from components.classes.MetricSignal import MetricSignal
from utils.packaging.main import check_if_repo_is_package


# GITHUB_ACCESS_TOKEN = "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"
# g = Github(GITHUB_ACCESS_TOKEN)


def get_vulnerabilites(coordinate: str):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "authorization": "Basic YXlhbmd1cHRhLmRldkBnbWFpbC5jb206MzAzZDZhMTVmMGJlOGIxNGE5MGViM2E4ZDE2YzZlNmI1NmY1NWZjZg==",
    }

    response = requests.post(
        "https://ossindex.sonatype.org/api/v3/authorized/component-report",
        headers=headers,
        json={"coordinates": [f"{coordinate}"]},
    )
    if response.status_code == 200:
        return response.json()
    else:
        return []


def get_vuln_dependencies_of_repo(repo: Repository.Repository):
    #  = g.get_repo("expressjs/express")
    vuln_deps_result = {}

    ms = MetricSignal()

    m = check_if_repo_is_package(repo=repo)
    if m.signal:
        self_repo = m.payload[0]
        self_coordinate = f"pkg:{self_repo['platform']}/{self_repo['name']}@{self_repo['latest_stable_release_number']}"
        self_vulns = get_vulnerabilites(self_coordinate)[0]
        vuln_deps_result[self_repo["name"]] = self_vulns["vulnerabilities"]

    libraries_io_endpoint = f"https://libraries.io/api/github/{repo.owner.login}/{repo.name.__str__()}/dependencies?api_key=15728e4185f58c5eb6feee336aec6682"
    data = requests.get(url=libraries_io_endpoint)
    deps = data.json()["dependencies"]

    if len(deps) == 0:
        ms.signal = False
        ms.message = "No dependencies in the repository"
        return ms

    for dep in tqdm(deps):
        version = (
            dep["requirements"].split("==")[-1]
            if len(dep["requirements"]) > 1
            else dep["latest_stable"]
        )

        coordinate = f'pkg:{dep["platform"]}/{dep["name"]}@{version}'
        vulns = get_vulnerabilites(coordinate=coordinate)[0]

        # dep_vln = None
        # if vulns != None and len(vulns) > 0:
        #     dep_vln = vulns[0]

        if (
            vulns
            and "vulnerabilities" in vulns
            and len(vulns["vulnerabilities"]) > 0
            and dep["name"] not in vuln_deps_result
        ):
            vuln_deps_result[dep["name"]] = vulns["vulnerabilities"]

    ms.signal = True
    ms.payload = vuln_deps_result

    print("Completed dependency vuln check")

    return ms


# get_vuln_dependencies_of_repo()

# pprint({"name": dep["name"], "platform": dep["platform"], "version": version})

# gh = xkcd2347.GitHub(key=GITHUB_ACCESS_TOKEN)
# deps = gh.get_dependencies(
#     repo_owner=repo.owner.login, repo_name=repo.name.__str__()
# )
# for dep in deps:
#     pprint(dep)


# endpoint = f"https://libraries.io/api/github/{repo.owner.login}/projects?api_key=15728e4185f58c5eb6feee336aec6682"
# data = requests.get(url=endpoint)
# owner_contributed_to: list = data.json()

# result = list(
#     filter(
#         lambda contribution: contribution["name"].lower()
#         == repo.name.__str__().lower()
#         and repo.owner.login + "/" + repo.name.__str__()
#         == contribution["repository_url"].split(".com/")[-1],
#         owner_contributed_to,
#     )
# )
