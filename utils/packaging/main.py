from github import Repository
import requests

from components.classes.MetricSignal import MetricSignal

LIBRARIESIO_API_KEY = "15728e4185f58c5eb6feee336aec6682"


def check_if_repo_is_package(repo: Repository.Repository):

    ms = MetricSignal()

    endpoint = f"https://libraries.io/api/github/{repo.owner.login}/projects?api_key=15728e4185f58c5eb6feee336aec6682"
    data = requests.get(url=endpoint)
    owner_contributed_to: list = data.json()

    result = list(
        filter(
            lambda contribution: contribution["name"].lower()
            == repo.name.__str__().lower()
            and repo.owner.login + "/" + repo.name.__str__()
            == contribution["repository_url"].split(".com/")[-1],
            owner_contributed_to,
        )
    )

    if len(result) > 0:
        ms.signal = True
        ms.payload = result
        ms.message = "Repository has package(s) associated with it"
    else:
        ms.signal = False
        ms.message = "Repository has no package(s) associated with it"

    return ms


# Get a list of packages referencing the given repository.
# ! https://libraries.io/api/github/:owner/:name/projects?api_key=YOUR_API_KEY

# Get packages in which user has contributed
# ! https://libraries.io/api/github/:login/project-contributions?api_key=YOUR_API_KEY

# Get repositories in which user has contributed
# ! https://libraries.io/api/github/:login/repository-contributions?api_key=YOUR_API_KEY

# Get a list of dependencies for a repositories. Currently only works for open source repositories.
# ! https://libraries.io/api/github/:owner/:name/dependencies?api_key=YOUR_API_KEY

# Get repositories that depend on a given project.
# ! https://libraries.io/api/:platform/:name/dependent_repositories?api_key=YOUR_API_KEY

# Get breakdown of SourceRank score for a given project.
# ! https://libraries.io/api/:platform/:name/sourcerank?api_key=YOUR_API_KEY
