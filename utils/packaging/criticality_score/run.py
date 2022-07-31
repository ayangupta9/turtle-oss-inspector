"""Main python script for calculating OSS Criticality Score."""

import datetime
import json
import logging
import math
import sys
import threading
import time
import urllib
from github import Repository as R
import requests

from components.classes.MetricSignal import MetricSignal

from .defaults import *  # pylint: disable=wildcard-import

logger = logging.getLogger()

_CACHED_GITHUB_TOKEN = None

PARAMS = [
    "description",
    "created_since",
    "updated_since",
    "contributor_count",
    "watchers_count",
    "org_count",
    "commit_frequency",
    "recent_releases_count",
    "updated_issues_count",
    "closed_issues_count",
    "comment_frequency",
    "dependents_count",
]


class Repository:
    """General source repository."""

    def __init__(self, repo):
        self._repo = repo
        self._last_commit = None
        self._created_since = None

    @property
    def name(self):
        raise NotImplementedError

    @property
    def url(self):
        raise NotImplementedError

    @property
    def language(self):
        raise NotImplementedError

    @property
    def description(self):
        raise NotImplementedError

    @property
    def last_commit(self):
        raise NotImplementedError

    @property
    def created_since(self):
        raise NotImplementedError

    @property
    def updated_since(self):
        raise NotImplementedError

    @property
    def contributor_count(self):
        raise NotImplementedError

    @property
    def watchers_count(self):
        raise NotImplementedError

    @property
    def org_count(self):
        raise NotImplementedError

    @property
    def commit_frequency(self):
        raise NotImplementedError

    @property
    def recent_releases_count(self):
        raise NotImplementedError

    @property
    def updated_issues_count(self):
        raise NotImplementedError

    @property
    def closed_issues_count(self):
        raise NotImplementedError

    @property
    def comment_frequency(self):
        raise NotImplementedError

    def _request_url_with_auth_headers(self, url):
        headers = {}
        if "github.com" in url and _CACHED_GITHUB_TOKEN:
            headers = {"Authorization": f"token {_CACHED_GITHUB_TOKEN}"}

        return requests.get(url, headers=headers)

    @property
    def dependents_count(self):
        # TODO: Take package manager dependency trees into account. If we decide
        # to replace this, then find a solution for C/C++ as well.
        match = None
        parsed_url = urllib.parse.urlparse(self.url)
        repo_name = parsed_url.path.strip("/")
        dependents_url = f'https://github.com/search?q="{repo_name}"&type=commits'
        for i in range(FAIL_RETRIES):
            result = self._request_url_with_auth_headers(dependents_url)
            if result.status_code == 200:
                match = DEPENDENTS_REGEX.match(result.content)
                break
            time.sleep(2**i)
        if not match:
            return 0
        return int(match.group(1).replace(b",", b""))


class GitHubRepository(Repository):
    """Source repository hosted on GitHub."""

    # General metadata attributes.
    @property
    def name(self):
        return self._repo.name

    @property
    def url(self):
        return self._repo.html_url

    @property
    def language(self):
        return self._repo.language

    @property
    def description(self):
        return self._repo.description

    @property
    def last_commit(self):
        if self._last_commit:
            return self._last_commit
        try:
            self._last_commit = self._repo.get_commits()[0]
        except Exception:
            pass
        return self._last_commit

    def get_first_commit_time(self):
        def _parse_links(response):
            link_string = response.headers.get("Link")
            if not link_string:
                return None

            links = {}
            for part in link_string.split(","):
                match = re.match(r'<(.*)>; rel="(.*)"', part.strip())
                if match:
                    links[match.group(2)] = match.group(1)
            return links

        for i in range(FAIL_RETRIES):
            result = self._request_url_with_auth_headers(f"{self._repo.url}/commits")
            links = _parse_links(result)
            if links and links.get("last"):
                result = self._request_url_with_auth_headers(links["last"])
            if result.status_code == 200:
                commits = json.loads(result.content)
                if commits:
                    last_commit_time_string = commits[-1]["commit"]["committer"]["date"]
                    return datetime.datetime.strptime(
                        last_commit_time_string, "%Y-%m-%dT%H:%M:%SZ"
                    )
            time.sleep(2**i)

        return None

    # Criteria important for ranking.
    @property
    def created_since(self):
        if self._created_since:
            return self._created_since

        creation_time = self._repo.created_at

        # See if there are exist any commits before this repository creation
        # time on GitHub. If yes, then the repository creation time is not
        # correct, and it was residing somewhere else before. So, use the first
        # commit date.
        if self._repo.get_commits(until=creation_time).totalCount:
            first_commit_time = self.get_first_commit_time()
            if first_commit_time:
                creation_time = min(creation_time, first_commit_time)

        difference = datetime.datetime.utcnow() - creation_time
        self._created_since = round(difference.days / 30)
        return self._created_since

    @property
    def updated_since(self):
        last_commit_time = self.last_commit.commit.author.date
        difference = datetime.datetime.utcnow() - last_commit_time
        return round(difference.days / 30)

    @property
    def contributor_count(self):
        try:
            return self._repo.get_contributors(anon="true").totalCount
        except Exception:
            # Very large number of contributors, i.e. 5000+. Cap at 5,000.
            return 5000

    @property
    def watchers_count(self):
        return self._repo.watchers_count

    @property
    def org_count(self):
        def _filter_name(org_name):
            return (
                org_name.lower()
                .replace("inc.", "")
                .replace("llc", "")
                .replace("@", "")
                .replace(" ", "")
                .rstrip(",")
            )

        orgs = set()
        contributors = self._repo.get_contributors()[:TOP_CONTRIBUTOR_COUNT]
        try:
            for contributor in contributors:
                if contributor.company:
                    orgs.add(_filter_name(contributor.company))
        except Exception:
            # Very large number of contributors, i.e. 5000+. Cap at 10.
            return 10
        return len(orgs)

    @property
    def commit_frequency(self):
        total = 0
        for week_stat in self._repo.get_stats_commit_activity():
            total += week_stat.total
        return round(total / 52, 1)

    @property
    def recent_releases_count(self):
        total = 0
        for release in self._repo.get_releases():
            if (
                datetime.datetime.utcnow() - release.created_at
            ).days > RELEASE_LOOKBACK_DAYS:
                continue
            total += 1
        if not total:
            # Make rough estimation of tags used in last year from overall
            # project history. This query is extremely expensive, so instead
            # do the rough calculation.
            days_since_creation = self.created_since * 30
            if not days_since_creation:
                return 0
            total_tags = 0
            try:
                total_tags = self._repo.get_tags().totalCount
            except Exception:
                # Very large number of tags, i.e. 5000+. Cap at 26.
                logger.error(f"get_tags is failed: {self._repo.url}")
                return RECENT_RELEASES_THRESHOLD
            total = round((total_tags / days_since_creation) * RELEASE_LOOKBACK_DAYS)
        return total

    @property
    def updated_issues_count(self):
        issues_since_time = datetime.datetime.utcnow() - datetime.timedelta(
            days=ISSUE_LOOKBACK_DAYS
        )
        return self._repo.get_issues(state="all", since=issues_since_time).totalCount

    @property
    def closed_issues_count(self):
        issues_since_time = datetime.datetime.utcnow() - datetime.timedelta(
            days=ISSUE_LOOKBACK_DAYS
        )
        return self._repo.get_issues(state="closed", since=issues_since_time).totalCount

    @property
    def comment_frequency(self):
        issues_since_time = datetime.datetime.utcnow() - datetime.timedelta(
            days=ISSUE_LOOKBACK_DAYS
        )
        issue_count = self._repo.get_issues(
            state="all", since=issues_since_time
        ).totalCount
        if not issue_count:
            return 0
        comment_count = self._repo.get_issues_comments(
            since=issues_since_time
        ).totalCount
        return round(comment_count / issue_count, 1)


def get_param_score(param, max_value, weight=1):
    """Return paramater score given its current value, max value and
    parameter weight."""
    return (math.log(1 + param) / math.log(1 + max(param, max_value))) * weight


def get_repository(repo: R.Repository):
    return GitHubRepository(repo)


def get_repository_stats(repo):
    """Return repository stats by grabing the raw signal data from the repo."""
    if not repo.last_commit:
        logger.error(f"Repo is empty: {repo.url}")
        return None

    def _worker(repo, param, return_dict):
        """worker function"""
        return_dict[param] = getattr(repo, param)

    threads = []
    return_dict = {}
    for param in PARAMS:
        thread = threading.Thread(target=_worker, args=(repo, param, return_dict))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    # Guarantee insertion order.
    result_dict = {
        "name": repo.name,
        "url": repo.url,
        "language": repo.language,
    }
    for param in PARAMS:
        result_dict[param] = return_dict[param]

    return result_dict


def get_repository_score(repo_stats, additional_params=None):
    """Return one repository's criticality score based on repo stats."""
    # Validate and compute additional params first.
    if additional_params is None:
        additional_params = []
    additional_params_total_weight = 0
    additional_params_score = 0
    for additional_param in additional_params:
        try:
            value, weight, max_threshold = [
                float(i) for i in additional_param.split(":")
            ]
        except ValueError:
            logger.error("Parameter value in bad format: " + additional_param)
            sys.exit(1)
        additional_params_total_weight += weight
        additional_params_score += get_param_score(value, max_threshold, weight)

    total_weight = (
        CREATED_SINCE_WEIGHT
        + UPDATED_SINCE_WEIGHT
        + CONTRIBUTOR_COUNT_WEIGHT
        + ORG_COUNT_WEIGHT
        + COMMIT_FREQUENCY_WEIGHT
        + RECENT_RELEASES_WEIGHT
        + CLOSED_ISSUES_WEIGHT
        + UPDATED_ISSUES_WEIGHT
        + COMMENT_FREQUENCY_WEIGHT
        + DEPENDENTS_COUNT_WEIGHT
        + additional_params_total_weight
    )

    criticality_score = round(
        (
            (
                get_param_score(
                    float(repo_stats["created_since"]),
                    CREATED_SINCE_THRESHOLD,
                    CREATED_SINCE_WEIGHT,
                )
            )
            + (
                get_param_score(
                    float(repo_stats["updated_since"]),
                    UPDATED_SINCE_THRESHOLD,
                    UPDATED_SINCE_WEIGHT,
                )
            )
            + (
                get_param_score(
                    float(repo_stats["contributor_count"]),
                    CONTRIBUTOR_COUNT_THRESHOLD,
                    CONTRIBUTOR_COUNT_WEIGHT,
                )
            )
            + (
                get_param_score(
                    float(repo_stats["org_count"]),
                    ORG_COUNT_THRESHOLD,
                    ORG_COUNT_WEIGHT,
                )
            )
            + (
                get_param_score(
                    float(repo_stats["commit_frequency"]),
                    COMMIT_FREQUENCY_THRESHOLD,
                    COMMIT_FREQUENCY_WEIGHT,
                )
            )
            + (
                get_param_score(
                    float(repo_stats["recent_releases_count"]),
                    RECENT_RELEASES_THRESHOLD,
                    RECENT_RELEASES_WEIGHT,
                )
            )
            + (
                get_param_score(
                    float(repo_stats["closed_issues_count"]),
                    CLOSED_ISSUES_THRESHOLD,
                    CLOSED_ISSUES_WEIGHT,
                )
            )
            + (
                get_param_score(
                    float(repo_stats["updated_issues_count"]),
                    UPDATED_ISSUES_THRESHOLD,
                    UPDATED_ISSUES_WEIGHT,
                )
            )
            + (
                get_param_score(
                    float(repo_stats["comment_frequency"]),
                    COMMENT_FREQUENCY_THRESHOLD,
                    COMMENT_FREQUENCY_WEIGHT,
                )
            )
            + (
                get_param_score(
                    float(repo_stats["dependents_count"]),
                    DEPENDENTS_COUNT_THRESHOLD,
                    DEPENDENTS_COUNT_WEIGHT,
                )
            )
            + additional_params_score
        )
        / total_weight,
        5,
    )

    # Make sure score between 0 (least-critical) and 1 (most-critical).
    criticality_score = max(min(criticality_score, 1), 0)

    return criticality_score


def get_repository_score_from_raw_stats(repo: R.Repository, params=None):
    """Get repository's criticality_score based on raw signal data."""
    repo = get_repository(repo)

    ms = MetricSignal()

    if repo is None:
        ms.signal = False
        return ms
    repo_stats = get_repository_stats(repo)
    repo_stats["criticality_score"] = get_repository_score(repo_stats, params)

    

    ms.signal = True
    ms.payload = repo_stats
    ms.message = "Calculated criticality score with other repository stats"

    print("Completed criticality score")

    return ms
