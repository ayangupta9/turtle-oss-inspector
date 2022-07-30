import json
import os
from github import Repository
from components.classes.Dependency import Dependency
from components.classes.MetricSignal import MetricSignal
from components.classes.Vulnerability import Vulnerability


def return_dependencies_from_report(report_path):
    dependencies = []
    packages = []

    with open(report_path) as f:
        json_result = json.load(f)
        for dependency in json_result["dependencies"]:
            new_dep = Dependency()
            if "filePath" in dependency:
                new_dep.file_path = dependency["filePath"]
            if "packages" in dependency:
                pkg_name = dependency["packages"][0].get("id", None).split(":")[1]
                new_dep.package_name = pkg_name
                if pkg_name != None:
                    packages.append(pkg_name)

                pkg_url = dependency["packages"][0].get("url", None)
                new_dep.package_url = pkg_url

            if "vulnerabilities" in dependency:
                new_vuln = Vulnerability()
                for vuln in dependency["vulnerabilities"]:
                    if "source" in vuln:
                        new_vuln.source = vuln["source"]

                    if "severity" in vuln:
                        new_vuln.severity = vuln["severity"]

                    if "name" in vuln:
                        new_vuln.name = vuln["name"]

                    if "description" in vuln:
                        new_vuln.description = vuln["description"]

                    if "cvssv3" in vuln:
                        new_vuln.cvss3 = {
                            "baseScore": vuln["cvssv3"]["baseScore"],
                            "userInteraction": vuln["cvssv3"]["userInteraction"],
                            "confidentialityImpact": vuln["cvssv3"][
                                "confidentialityImpact"
                            ],
                            "integrityImpact": vuln["cvssv3"]["integrityImpact"],
                            "availabilityImpact": vuln["cvssv3"]["availabilityImpact"],
                            "baseSeverity": vuln["cvssv3"]["baseSeverity"],
                            "exploitabilityScore": vuln["cvssv3"][
                                "exploitabilityScore"
                            ],
                            "impactScore": vuln["cvssv3"]["impactScore"],
                        }

                    if "references" in vuln:
                        new_vuln.references = vuln["references"][0:20]

                new_dep.vulnerabilities.append(new_vuln.__dict__)
            dependencies.append(new_dep.__dict__)
        f.close()
    return dependencies, packages


def execute_dependency_check(repo: Repository.Repository):
    ms = MetricSignal()

    DEPENDENCY_CHECK_BAT = "shell-process\\dependency-check\\bin\\dependency-check.bat"
    REPO_PATH = "cloned_repos\\" + repo.name.__str__()

    os.system(command=f"git clone {repo.clone_url} {REPO_PATH}")

    OUTPUT_REPORT_PATH = "dc-output-reports\\" + repo.name.__str__() + "-report.json"
    command = f"{DEPENDENCY_CHECK_BAT} --scan {REPO_PATH} --out {OUTPUT_REPORT_PATH} --format JSON --enableExperimental"
    result = os.system(command=command)
    if result != 0:
        ms.signal = False
        ms.message = "Could not run command properly"
    else:
        report_results = return_dependencies_from_report(OUTPUT_REPORT_PATH)

        ms.signal = True
        ms.payload = report_results
        ms.message = "Generated data from reports"

    return ms
