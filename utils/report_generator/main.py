import json
from pprint import pprint
from string import Template

from components.classes.MetricSignal import MetricSignal


def binary_artifacts_component(data: dict):

    html_code = ""

    template = Template(
        """
        <div class="d-flex binary-artifacts-content">
            <h1 class="flex-grow-1 center-element w-100">$executables_count</h1>
                <ul class="list-unstyled flex-grow-1 center-element w-100 flex-column align-items-start">
                    $executable_items
                </ul>
        </div>
    """
    )

    if data.signal == True:
        executables: list = data["payload"]["executables"]

        list_items = ""
        for executable in executables:
            list_items += f"<li><code>{executable}</code></li>\n"

        html_code = template.substitute(
            executables_count=len(executables), executable_items=list_items
        )
    else:
        html_code = template.substitute(
            executables_count=0,
            executable_items="<li><code>No executables ✔</code></li>",
        )

    return html_code


def badges_component(data: dict):
    html_code = ""

    template = Template(
        """
        <div class="d-flex flex-column badges-content align-items-center">
            <div class="d-flex justify-content-evenly py-3 w-100">
                <h1 class="flex-grow-1 center-element w-100">$percentage %</h1>
                <h1 class="flex-grow-1 center-element w-100">$badge_level</h1>
            </div>
            <ul class="impl-langs d-flex m-0 px-0 py-1 w-100 list-group-horizontal">
                $impl_langs
            </ul>
        </div>
    """
    )

    if data.signal == True:
        list_items = ""
        for lang in data["payload"]["implementation_languages"]:
            list_items += f"<li class='list-group-item'>{lang}</li>"
        html_code = template.substitute(
            percentage=data["payload"]["tiered_percentage"],
            badge_level=data["payload"]["badge_level"],
            impl_langs=list_items,
        )

    else:
        html_code = template.substitute(
            percentage="-", badge_level="No badge", impl_langs=""
        )

    return html_code


def code_review_component(data):

    if data["payload"]["archived"] == True:
        return "<p>Github repo is archived</p>"

    html_code = ""

    template = Template(
        """
          <div class="code-review-content">
                <h2 class="text-center py-2">$is_protected</h2>
                <h4 class="text-center py-2">REVIEWER COUNT: $reviewer_count</h4>
                <div class="issues-content">
                    <div class="d-flex justify-content-evenly align-items-center py-2 w-100">
                        <h6 class="w-50 text-center">OPEN ISSUES : $open_issues</h6>
                        <h6 class="w-50 text-center">CLOSED ISSUES : $closed_issues</h6>
                    </div>
                    <ul class="issues-list d-flex m-0 px-0 py-1 w-100 list-group-horizontal">
                        $issues_stats
                    </ul>
                </div>
            </div>
        """
    )

    list_items = ""
    issue_stats = data["payload"]["issues_stats"]["bug_issues"]

    # if data.signal == True:

    for issue_label, issue_stat in issue_stats.items():
        list_items += f"""<li class="list-group-item">
                                <div>
                                    <h4 class="mb-0">{issue_label}</h4>
                                    <small>{issue_stat['count']}</small>
                                    <br>
                                    <a href="{issue_stat['url']}">Github Reference</a>
                                </div>
                            </li>
                        """
    html_code = template.substitute(
        is_protected=data["payload"]["protected"],
        reviewer_count=data["payload"]["approving_review_count"],
        open_issues=issue_stats["open_issues"],
        closed_issues=issue_stats["closed_issues"],
        issues_stats=list_items,
    )

    return html_code


def contributors_component(data):

    html_code = ""

    template = Template(
        template="""
     <div class="contributors-content">
        <div class="d-flex w-100 mb-3">
            <div class="d-flex w-100 flex-column align-items-start">
                <b>TOTAL COMMITS</b>
                <h5>$total_commits</h5>
            </div>
            <div class="d-flex w-100 flex-column align-items-start">
                <b>LEGIT CONTRIBUTORS</b>
                <h5>$legit_contri_count</h5>
            </div>
        </div>
        <div class="mb-3">
            <h6 class="text-start ps-3 pt-1 mb-0">CONTRIBUTORS COMPANY</h6>
            <p>$companies</p>
            <div class="issues-list-wrapper">
                <ul class="issues-list d-flex m-0 px-0 py-1 w-100 list-group">
                    $contributors_items
                </ul>
            </div>
        </div>
    </div>
    """
    )

    list_items = ""

    for contributor_login, contributor_stats in data["payload"][
        "legit_contributors"
    ].items():
        list_items += f"""
        
        <li class="list-group-item">
            <div class="d-flex justify-content-between">
                <b>{contributor_login}</b>
                <small>{contributor_stats['commits_count']}</small>
                <small>{contributor_stats['company']}</small>
            </div>
            <p class="m-0">{(", ".join(contributor_stats['orgs'])).rstrip(', ')}</p>
        </li>
        """

    html_code = template.substitute(
        total_commits=data["payload"]["total_commits"],
        legit_contri_count=len(data["payload"]["legit_contributors"]),
        companies=(", ".join(data["payload"]["distinct_companies"])).rstrip(", "),
        contributors_items=list_items,
    )

    return html_code


def dependency_check_component(data1, data2):

    html_code = ""

    template = Template(
        template=f"""
        <p><b><a href="{data1['payload']}">Dependency Update tool</a></b></p>
        <div class="accordion-wrapper">
            <div class="accordion" id="accordionExample">
                <div class="accordion-item">
                    <h2 class="accordion-header" id="headingOne">
                        <button class="accordion-button" type="button" data-bs-toggle="collapse"
                            data-bs-target="#collapseOne" aria-expanded="false"
                            aria-controls="collapseOne">
                            $dep_name
                        </button>
                    </h2>
                    <div id="collapseOne" class="accordion-collapse collapse"
                        aria-labelledby="headingOne" data-bs-parent="#accordionExample">
                        <div class="accordion-body">
                            <p class="m-0"><b>CVSS score:</b> 2.1</p>
                            <p class="m-0"><b>Severity</b> HIGH</p>
                            <p class="m-0">Description</p>
                            <p class="m-0"><a href="">Ref</a></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """
    )

    pass


def license_security_component(data):
    pass


def maintenance_component(data):
    pass


def generate_html_report(json_report_path: str):
    with open(json_report_path, "r") as f:
        report_data = json.load(f)
        print(report_data)

    pass


# generate_html_report("test.json")
