"""This check determines whether the project is actively maintained. 
If the project is archived, it receives the lowest score. 
If there is at least one commit per week during the previous 90 days, 
the project receives the highest score. If there is activity on issues 
from users who are collaborators, members, or owners of the project, 
the project receives a partial score."""


from github import Repository
from datetime import datetime, timedelta

from components.classes.MetricSignal import MetricSignal


def get_commits(repo: Repository.Repository):
    commits_stats_result = {}
    for stat in list(repo.get_stats_commit_activity()):
        commits_stats_result[str(stat.week)] = stat.total
    return commits_stats_result


def project_maintained(repo: Repository.Repository):
    is_archived = repo.archived

    ms = MetricSignal()

    if not is_archived:
        git_stats = get_commits(repo=repo)

        ms.signal = True
        ms.payload = git_stats
        ms.message = "Fetched commit data. Track frequency of code commits to measure maintenance metric"
    else:
        ms.message = "Repository is archived"
        ms.signal = False

    print("Completed maintenance")

    return ms
