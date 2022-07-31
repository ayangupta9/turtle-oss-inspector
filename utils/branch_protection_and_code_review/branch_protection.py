from github import Repository

from components.classes.MetricSignal import MetricSignal


def get_branch_protection(repo: Repository.Repository):
    branch = repo.get_branch(repo.default_branch)

    branch_protection_score = 0

    branch_protection_output = {
        "branch_protected": False,
        "not_allow_force_pushes": False,
        "not_allow_force_pushes": False,
        "enforce_admins": False,
        "requires_pull_request_reviews": False,
        "required_approving_review_count": False,
        "requires_status_checks": False,
        "strict_status_checks": False,
        "requires_commit_signatures": False,
    }

    ms = MetricSignal()

    if branch.protected:
        branch_protection_score += 1
        branch_protection_output["branch_protected"] = True
        try:
            branch_protection_data = branch.get_protection().raw_data
            if (
                "allow_force_pushes" in branch_protection_data
                and branch_protection_data["allow_force_pushes"]["enabled"] == False
            ):
                # check if force pushes are allowed on default branch
                branch_protection_output["not_allow_force_pushes"] = True
                branch_protection_score += 1
            if (
                "allow_deletions" in branch_protection_data
                and branch_protection_data["allow_deletions"]["enabled"] == False
            ):  # check if deletions are allowed on default branch
                branch_protection_output["not_allow_force_pushes"] = True
                branch_protection_score += 1

            if (
                "enforce_admins" in branch_protection_data
                and branch_protection_data["enforce_admins"]["enabled"] == True
            ):
                branch_protection_output["enforce_admins"] = True
                branch_protection_score += 1

            if "required_pull_request_reviews" in branch_protection_data:
                branch_protection_score += 1
                branch_protection_output["requires_pull_request_reviews"] = True
                if (
                    branch_protection_data["required_pull_request_reviews"][
                        "required_approving_review_count"
                    ]
                    >= 1
                ):
                    branch_protection_output["required_approving_review_count"] = True
                    branch_protection_score += min(
                        2,
                        branch_protection_data["required_pull_request_reviews"][
                            "required_approving_review_count"
                        ],
                    )
            if (
                "required_status_checks" in branch_protection_data
                and len(branch_protection_data["required_status_checks"]["contexts"])
                > 0
                and len(branch_protection_data["required_status_checks"]["checks"]) > 0
            ):
                branch_protection_output["requires_status_checks"] = True
                branch_protection_score += 1

                if branch_protection_data["required_status_checks"]["strict"] == True:
                    branch_protection_output["strict_status_checks"] = True
                    branch_protection_score += 1

            if (
                "required_signatures" in branch_protection_data
                and branch_protection_data["required_signatures"]["enabled"]
            ):
                branch_protection_output["requires_commit_signatures"] = True
                branch_protection_score += 1

                ms.message = (
                    "Branch is protected and branch protection stats is accessible."
                )
        except Exception:
            ms.message = "Branch is protected but branch protection stats not accessible. Needs admin/curator rights of the repository"
        ms.signal = True
    else:
        ms.signal = False
        ms.message = "Branch is not protected"
    ms.payload = {
        "branch_protection_score": branch_protection_score,
        "branch_protection_output": branch_protection_output,
    }
    print('Completed branch protection')
    return ms
