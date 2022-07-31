from github import Repository, Commit

from components.classes.MetricSignal import MetricSignal


def has_dependency_update_tool(repo: Repository.Repository):
    dependency_update_tool_result = {}

    ms = MetricSignal()

    dependabot_files = ["dependabot.yml", "dependabot.yaml"]
    renovabot_files = [
        ".github/renovate.json",
        ".github/renovate.json5",
        ".renovaterc.json",
        "renovate.json",
        "renovate.json5",
        ".renovaterc",
    ]

    last_commit: Commit.Commit = repo.get_commits()[0]
    tree = repo.get_git_tree(sha=last_commit.sha, recursive=True).tree

    for element in tree:
        file_name = element.path.split("/")[-1]
        if "." in file_name:
            if file_name in renovabot_files or file_name in dependabot_files:
                tool_url = (
                    "https://github.com/"
                    + repo.owner.login
                    + "/"
                    + repo.name.__str__()
                    + "/tree/"
                    + repo.default_branch
                    + "/"
                    + element.path
                )

                dependency_update_tool_result[file_name.split(".")[0]] = tool_url

    if len(dependency_update_tool_result.keys()) > 0:
        ms.signal = True
        ms.message = "Repository has dependency update tool"
        ms.payload = dependency_update_tool_result

    else:
        ms.message = "Repository lacks dependency update tool"
        ms.signal = False

    print('Completed dependency update check')

    return ms
