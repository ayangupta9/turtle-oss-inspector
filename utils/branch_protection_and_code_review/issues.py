from string import Template
from github import Repository
import requests


def get_issues_count(owner: str, repo_name: str):
    GITHUB_ACCESS_TOKEN = "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"
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}"}

    template = Template(
        """
    {
        repository(owner: "$owner", name: "$repo_name") {
		    issues {
                totalCount
            }
        }
    }   
    """
    )
    query = template.substitute(owner=owner, repo_name=repo_name)
    data = requests.post(url=url, headers=headers, json={"query": query})
    if data.status_code == 200:
        return data.json()["data"]["repository"]["issues"]["totalCount"]
    else:
        return False


def get_bug_issues(repo: Repository.Repository):
    bug_labels = []
    bug_results = {}

    for label in list(repo.get_labels()):
        if (
            "bug" in label.name
            and "fix" not in label.name
            and "debug" not in label.name
            or "critical" in label.name
            or "high" in label.name
        ):
            bug_labels.append(label.name)
            bug_results[label.name] = {"url": label.url}

    for bug_label in bug_labels:
        bug_issues = list(repo.get_issues(labels=[bug_label]))
        bug_results[bug_label]["count"] = len(bug_issues)

    return bug_results


def get_issues_stats(repo: Repository.Repository):
    issues_stats = {}
    if repo.has_issues:
        total_issues_count = get_issues_count(
            owner=repo.owner.login, repo_name=repo.name.__str__()
        )
        issues_stats["open_issues"] = repo.open_issues_count
        issues_stats["closed_issues"] = total_issues_count - repo.open_issues_count

        issues_stats["bug_issues"] = get_bug_issues(repo)
        return issues_stats
    else:
        return False
