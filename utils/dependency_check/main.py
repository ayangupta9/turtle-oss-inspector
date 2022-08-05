import requests
from github import Github, Repository
from pprint import pprint
from dotenv import load_dotenv
import os

# import xkcd2347
from tqdm import tqdm
from components.classes.MetricSignal import MetricSignal
from utils.packaging.main import check_if_repo_is_package


load_dotenv()


def get_vulnerabilites(coordinate: str):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "authorization": f"Basic {os.getenv('OSS_INDEX_API_KEY')}",
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
        vulns = get_vulnerabilites(coordinate=coordinate)
        if vulns != None and len(vulns) > 0:
            vulns = vulns[0]
        else:
            continue

        if (
            vulns
            and "vulnerabilities" in vulns
            and len(vulns["vulnerabilities"]) > 0
            and dep["name"] not in vuln_deps_result
        ):
            vuln_deps_result[dep["name"]] = vulns["vulnerabilities"]
            ms.score += 1.0

    ms.signal = True
    ms.payload = vuln_deps_result
    ms.score /= len(deps)
    ms.score = 1 - ms.score
    print("Completed dependency vuln check")

    return ms
