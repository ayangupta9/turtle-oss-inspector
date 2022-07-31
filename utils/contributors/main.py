from github import Repository
from datetime import datetime, timedelta

from components.classes.MetricSignal import MetricSignal


def process_company(company: str):
    company = company.lower()
    company = (
        company.replace("inc", "")
        .replace("llc", "")
        .replace(",", "")
        .replace(".", "")
        .lstrip("@")
        .strip(" ")
    )

    return company


def get_contributors_stats(repo: Repository.Repository):
    companies = set()
    commit_authors = {}

    ms = MetricSignal()
    commits_since_time = datetime.now() + timedelta(weeks=-1)

    commits = list(repo.get_commits(since=commits_since_time))
    total_commits = len(commits)

    for commit in commits:
        if (
            commit.author
            and commit.author.company
            and len(list(commit.author.get_orgs())) >= 1
        ):
            pc = process_company(commit.author.company)
            companies.add(pc)
            if not commit.author.login in commit_authors:
                commit_authors[commit.author.login] = {}
                commit_authors[commit.author.login]["company"] = pc
                commit_authors[commit.author.login]["commits_count"] = 1
                commit_authors[commit.author.login]["orgs"] = [
                    x.name.__str__() for x in commit.author.get_orgs()
                ]

            else:
                commit_authors[commit.author.login]["commits_count"] += 1

    ms.signal = True

    if len(list(companies)) > 3:
        ms.score += 0.5
    if len(commit_authors.keys()) / 3 >= total_commits:
        ms.score += 0.5

    ms.payload = {
        "commits_since": str(commits_since_time),
        "distinct_companies": list(companies),
        "legit_contributors": commit_authors,
        "total_commits": total_commits,
    }

    print("Completed contributors")

    return ms
