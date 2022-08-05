from github import Repository
from components.classes.MetricSignal import MetricSignal
from dotenv import load_dotenv
import os

# from issues import get_issues_stats
from utils.branch_protection_and_code_review.issues import get_issues_stats

load_dotenv()


def get_code_review(repo: Repository.Repository):

    ms = MetricSignal()
    score = 0
    # * check 1
    is_archived = repo.archived
    if not is_archived:
        score += 1
    review_result = {}
    review_result["archived"] = is_archived

    # * check 2
    is_protected = None
    approving_review_count = None
    branch = repo.get_branch(repo.default_branch)
    is_protected = branch.protected
    if is_protected:
        score += 1

    if is_protected == True:
        try:
            approving_review_count = (
                is_protected
                & branch.get_required_pull_request_reviews().required_approving_review_count
                >= 1
            )
        except:
            pass
        finally:
            review_result["approving_review_count"] = approving_review_count

    review_result["protected"] = is_protected
    review_result["issues_stats"] = get_issues_stats(
        repo=repo, GITHUB_ACCESS_TOKEN=os.getenv("GITHUB_ACCESS_TOKEN")
    )

    if approving_review_count != None:
        score += 1

    ms.signal = True
    ms.payload = review_result
    ms.score = score / 3
    print("Completed code review")

    return ms
