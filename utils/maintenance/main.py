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
    commits_score = 0

    commits_stats_result = {}
    for stat in list(repo.get_stats_commit_activity()):
        if stat.total != 0:
            commits_score += 1
        commits_stats_result[str(stat.week)] = stat.total
    return (commits_stats_result, commits_score)


def project_maintained(repo: Repository.Repository):
    is_archived = repo.archived

    score = 0

    ms = MetricSignal()

    if not is_archived:
        score += 1
        git_stats, commits_score = get_commits(repo=repo)
        score += commits_score

        ms.signal = True
        ms.payload = git_stats
        ms.message = "Fetched commit data. Track frequency of code commits to measure maintenance metric"
    else:
        ms.message = "Repository is archived"
        ms.signal = False

    ms.score = score / (len(git_stats.keys()) + 1)

    print("Completed maintenance")

    return ms
