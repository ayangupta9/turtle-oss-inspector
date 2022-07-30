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

    commits = list(repo.get_commits(since=datetime.now() + timedelta(weeks=-1)))
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
            else:
                commit_authors[commit.author.login]["commits_count"] += 1

    legit_contributors = total_commits - len(list(commit_authors.keys()))

    ms.signal = True
    ms.payload = {
        "distinct_companies": companies,
        "legit_contributors": {
            "count": legit_contributors,
            "contributors": commit_authors,
        },
        "total_commits": total_commits,
    }

    return ms
