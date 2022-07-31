from github import Commit, Repository

from components.classes.MetricSignal import MetricSignal

# https://github.com/ossf/scorecard/blob/1e0e44a0e8433b01ae749993e00da53579784d3d/checks/raw/binary_artifact.go

binaries_formats = [
    "crx",
    "deb",
    "dex",
    "dey",
    "elf",
    "o",
    "so",
    "macho",
    "iso",
    "class",
    "jar",
    "bundle",
    "dylib",
    "lib",
    "msi",
    "dll",
    "drv",
    "efi",
    "exe",
    "ocx",
    "pyc",
    "pyo",
    "par",
    "rpm",
    "whl",
]


def get_binaries(repo: Repository.Repository):
    last_commit: Commit.Commit = repo.get_commits()[0]
    tree = repo.get_git_tree(sha=last_commit.sha, recursive=True).tree
    executables = []
    # binary_artifacts_score = 0

    for elements in tree:
        if elements.path.split(".")[-1].lower() in binaries_formats:
            executables.append(elements.path.split("/")[-1])

    ms = MetricSignal()

    if len(executables) > 0:
        ms.signal = True
        ms.payload = {"executables": executables}
        ms.message = "Repository has binary artifacts. Be careful"

    else:
        ms.signal = False
        ms.message = "Repository has no binary artifacts"
    print('Completed binary artifact')
    return ms
