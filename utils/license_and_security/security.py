from github import Repository, Commit

from components.classes.MetricSignal import MetricSignal


def check_security_files(repo: Repository.Repository):

    last_commit: Commit.Commit = repo.get_commits()[0]
    tree = repo.get_git_tree(sha=last_commit.sha, recursive=True).tree

    ms = MetricSignal()

    for element in tree:
        file_name = element.path.split("/")[-1]
        if "." in file_name:
            if "security" in file_name.lower() and file_name.split(".")[-1] in [
                "md",
                "adoc",
                "rst",
                "txt",
                "html",
            ]:
                content_file = repo.get_contents(element.path)
                ms.signal = True
                ms.score = 1.0
                ms.payload = (
                    repo.clone_url.split(".git")[0]
                    + "/tree/"
                    + repo.default_branch
                    + "/"
                    + content_file.path
                )
                ms.message = "Security file found"
                break

    if ms.payload == None:
        ms.signal = False
        ms.message = "No security file"

    print("Completed security")

    return ms
