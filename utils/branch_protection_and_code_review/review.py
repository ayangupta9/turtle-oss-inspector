from github import Repository
from components.classes.MetricSignal import MetricSignal

# from issues import get_issues_stats
from utils.branch_protection_and_code_review.issues import get_issues_stats


def get_code_review(repo: Repository.Repository):

    ms = MetricSignal()

    # * check 1
    is_archived = repo.archived
    review_result = {}
    review_result["archived"] = is_archived

    # * check 2
    is_protected = None
    approving_review_count = None
    branch = repo.get_branch(repo.default_branch)
    is_protected = branch.protected

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
    review_result["issues_stats"] = get_issues_stats(repo=repo)

    ms.signal = True
    ms.payload = review_result

    print("Completed code review")

    return ms
