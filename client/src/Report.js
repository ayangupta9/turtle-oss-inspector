import report from "./../../result1.json";
import React, { useEffect, useState } from "react";
export default function Report(props) {
  const [data, setData] = useState(null);
  useEffect(() => {
    setData(report);
    console.log(data);
  }, [report]);

  return data ? (
    <div className="w-100 container mt-4 mb-5">
      <header className="d-flex justify-content-center p-3">
        <h1 className="fw-bold">
          <a
            href={data?.repo_is_pack_result.payload[0].repository_url}
            className="link-primary text-decoration-none"
          >
            Repository: {data?.criticality_score_result.payload.name}
            {/* REPOSITORY OWNER */}/
            {data?.criticality_score_result.payload.name}
            {/* REPOSITORY NAME */}
          </a>
        </h1>
      </header>
      <main className="w-100">
        <div className="d-flex w-100 flex-wrap row">
          <div className="col-4 d-flex flex-column gap-5 h-100">
            <section className="card p-4 binary-artifacts ">
              <h3 className="text-center">BINARY ARTIFACTS</h3>
              <div className="d-flex binary-artifacts-content">
                <h1 className="flex-grow-1 center-element w-100">
                  {data?.binary_artifacts_result.payload.executables.length}
                </h1>
                <br />
                <ul className="list-unstyled flex-grow-1 center-element w-100 flex-column align-items-start">
                  {data?.binary_artifacts_result.payload.executables.map(
                    (item, idx) => {
                      return (
                        <li key={idx}>
                          <code>{item}</code>
                        </li>
                      );
                    }
                  )}
                  {/* <li>
                    <code>AAAAAA</code>
                  </li>
                  <li>
                    <code>BBBBB</code>
                  </li>
                  <li>
                    <code>CCCCC</code>
                  </li>
                  <li>
                    <code>DDDDDDDD</code>
                  </li> */}
                </ul>
              </div>
            </section>
            <section className="card p-4 badges">
              <h3 className="text-center">BEST PRACTICE BADGE</h3>
              <div className="d-flex flex-column badges-content align-items-center">
                <div className="d-flex justify-content-evenly py-3 w-100">
                  <h1 className="flex-grow-1 center-element w-100">
                    {data?.badge_result.payload.tiered_percentage}%
                  </h1>

                  <h1 className="flex-grow-1 center-element w-100">
                    {data?.badge_result.payload.badge_level}
                  </h1>
                </div>
                <ul className="impl-langs d-flex m-0 px-0 py-1 w-100 list-group-horizontal">
                  {data?.badge_result.payload.implementation_languages.map(
                    (item, idx) => {
                      return (
                        <li key={idx} className="list-group-item">
                          {item}
                        </li>
                      );
                    }
                  )}
                  {/* <li className="list-group-item">Python</li>
                  <li className="list-group-item">Python</li>
                  <li className="list-group-item">Python</li>
                  <li className="list-group-item">Python</li>
                  <li className="list-group-item">Python</li>
                  <li className="list-group-item">Python</li>
                  <li className="list-group-item">Java</li>
                  <li className="list-group-item">SQL</li> */}
                </ul>
              </div>
            </section>
            <section className="card p-4 code-review">
              <h3 className="text-center text-wrap">
                CODE REVIEW AND AWARENESS
              </h3>
              <div className="code-review-content">
                <h2 className="text-center py-2">PROTECTED</h2>
                <h4 className="text-center py-2">REVIEWER COUNT: 8</h4>
                <div className="issues-content">
                  <div className="d-flex justify-content-evenly align-items-center py-2 w-100">
                    <h6 className="w-50 text-center">
                      OPEN ISSUES :{" "}
                      {
                        data?.code_review_result.payload.issues_stats
                          .open_issues
                      }
                    </h6>
                    <h6 className="w-50 text-center">
                      CLOSED ISSUES :{" "}
                      {
                        data?.code_review_result.payload.issues_stats
                          .closed_issues
                      }
                    </h6>
                  </div>
                  <ul className="issues-list d-flex m-0 px-0 py-1 w-100 list-group-horizontal">
                    <li className="list-group-item">
                      <div>
                        {/* <div class="d-flex justify-content-between"> */}
                        <h4 className="mb-0">BUG</h4>
                        <small>count</small>
                        <br />
                        {/* </div> */}
                        <a
                          href={
                            data?.code_review_result.payload.issues_stats
                              .bug_issues["confirmed-bug"].url
                          }
                        >
                          bugs reference link
                        </a>
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
            </section>
          </div>
          <div className="col-4 d-flex flex-column gap-5 h-100">
            <section className="card p-4 contributors">
              <h3 className="text-center text-wrap">CONTRIBUTORS</h3>
              <div className="contributors-content">
                <div className="d-flex w-100 mb-3">
                  <div className="d-flex w-100 flex-column align-items-start">
                    <b>TOTAL COMMITS</b>
                    <h5>{data?.contri_result.payload.total_commits}</h5>
                  </div>
                  <div className="d-flex w-100 flex-column align-items-start">
                    <b>LEGIT CONTRIBUTORS</b>
                    <h5>
                      {
                        Object.keys(
                          data?.contri_result.payload.legit_contributors
                        ).length
                      }
                    </h5>
                  </div>
                </div>
                <div className="mb-3">
                  <h6 className="text-start ps-3 pt-1 mb-0">
                    CONTRIBUTORS COMPANY
                  </h6>
                  <p>
                    {data?.contri_result.payload.distinct_companies.map(
                      (item, idx) => {
                        return <span key={idx}>{item}, </span>;
                      }
                    )}
                  </p>
                  <div className="issues-list-wrapper">
                    <ul className="issues-list d-flex m-0 px-0 py-1 w-100 list-group">
                      {Object.keys(
                        data?.contri_result.payload.legit_contributors
                      ).map(function (key, idx) {
                        return (
                          <li className="list-group-item" key={idx} value={key}>
                            {/* {
                              data?.contri_result.payload.legit_contributors[
                                key
                              ]
                            } */}
                            <div className="d-flex justify-content-between">
                              <b>COMMIT AUTHOR:{key}</b>
                              <small>{key.commits_count}</small>
                              <small>{key.company}</small>
                            </div>
                            <p className="m-0">
                              {/* {key.orgs.map((item, idx) => {
                                return <span key={idx}>{item}</span>;
                              })} */}
                            </p>
                          </li>
                        );
                      })}

                      {/* <li className="list-group-item">
                        <li>
                          <div className="d-flex justify-content-between">
                            <b>COMMIT AUTHOR</b>
                            <small>count</small>
                            <small>Company</small>
                          </div>
                          <p className="m-0">org1, org2, org3, ...</p>
                        </li>
                        <div className="d-flex justify-content-between">
                          <b>COMMIT AUTHOR</b>
                          <small>count</small>
                          <small>Company</small>
                        </div>
                        <p className="m-0">org1, org2, org3, ...</p>
                      </li>
                      <li className="list-group-item">
                        <div className="d-flex justify-content-between">
                          <b>COMMIT AUTHOR</b>
                          <small>count</small>
                          <small>Company</small>
                        </div>
                        <p className="m-0">org1, org2, org3, ...</p>
                      </li>
                      <li className="list-group-item">
                        <div className="d-flex justify-content-between">
                          <b>COMMIT AUTHOR</b>
                          <small>count</small>
                          <small>Company</small>
                        </div>
                        <p className="m-0">org1, org2, org3, ...</p>
                      </li>
                      <li className="list-group-item">
                        <div className="d-flex justify-content-between">
                          <b>COMMIT AUTHOR</b>
                          <small>count</small>
                          <small>Company</small>
                        </div>
                        <p className="m-0">org1, org2, org3, ...</p>
                      </li>
                      <li className="list-group-item">
                        <div className="d-flex justify-content-between">
                          <b>COMMIT AUTHOR</b>
                          <small>count</small>
                          <small>Company</small>
                        </div>
                        <p className="m-0">org1, org2, org3, ...</p>
                      </li> */}
                    </ul>
                  </div>
                </div>
              </div>
            </section>
            <section className="card p-4 dependency-update-tool">
              <p>
                <b>
                  <a href="">Dependency Update tool</a>
                </b>
              </p>
              <div className="accordion-wrapper">
                <div className="accordion" id="accordionExample">
                  <div className="accordion-item">
                    <h2 className="accordion-header" id="headingOne">
                      <button
                        className="accordion-button"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#collapseOne"
                        aria-expanded="false"
                        aria-controls="collapseOne"
                      >
                        DEP NAME #1
                      </button>
                    </h2>
                    <div
                      id="collapseOne"
                      className="accordion-collapse collapse"
                      aria-labelledby="headingOne"
                      data-bs-parent="#accordionExample"
                    >
                      <div className="accordion-body">
                        <p className="m-0">
                          <b>CVSS score:</b> 2.1
                        </p>
                        <p className="m-0">
                          <b>Severity</b> HIGH
                        </p>
                        <p className="m-0">Description</p>
                        <p className="m-0">
                          <a href="">Ref</a>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="accordion-item">
                    <h2 className="accordion-header" id="headingTwo">
                      <button
                        className="accordion-button collapsed"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#collapseTwo"
                        aria-expanded="false"
                        aria-controls="collapseTwo"
                      >
                        DEP NAME #2
                      </button>
                    </h2>
                    <div
                      id="collapseTwo"
                      className="accordion-collapse collapse"
                      aria-labelledby="headingTwo"
                      data-bs-parent="#accordionExample"
                    >
                      <div className="accordion-body">
                        <p className="m-0">
                          <b>CVSS score:</b> 2.1
                        </p>
                        <p className="m-0">
                          <b>Severity</b> HIGH
                        </p>
                        <p className="m-0">Description</p>
                        <p className="m-0">
                          <a href="">Ref</a>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="accordion-item">
                    <h2 className="accordion-header" id="headingThree">
                      <button
                        className="accordion-button collapsed"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#collapseThree"
                        aria-expanded="false"
                        aria-controls="collapseThree"
                      >
                        DEP NAME #3
                      </button>
                    </h2>
                    <div
                      id="collapseThree"
                      className="accordion-collapse collapse"
                      aria-labelledby="headingThree"
                      data-bs-parent="#accordionExample"
                    >
                      <div className="accordion-body">
                        <p className="m-0">
                          <b>CVSS score:</b> 2.1
                        </p>
                        <p className="m-0">
                          <b>Severity</b> HIGH
                        </p>
                        <p className="m-0">Description</p>
                        <p className="m-0">
                          <a href="">Ref</a>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="accordion-item">
                    <h2 className="accordion-header" id="headingThree">
                      <button
                        className="accordion-button collapsed"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#collapseThree"
                        aria-expanded="false"
                        aria-controls="collapseThree"
                      >
                        DEP NAME #4
                      </button>
                    </h2>
                    <div
                      id="collapseThree"
                      className="accordion-collapse collapse"
                      aria-labelledby="headingThree"
                      data-bs-parent="#accordionExample"
                    >
                      <div className="accordion-body">
                        <p className="m-0">
                          <b>CVSS score:</b> 2.1
                        </p>
                        <p className="m-0">
                          <b>Severity</b> HIGH
                        </p>
                        <p className="m-0">Description</p>
                        <p className="m-0">
                          <a href="">Ref</a>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="accordion-item">
                    <h2 className="accordion-header" id="headingThree">
                      <button
                        className="accordion-button collapsed"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#collapseThree"
                        aria-expanded="false"
                        aria-controls="collapseThree"
                      >
                        DEP NAME #5
                      </button>
                    </h2>
                    <div
                      id="collapseThree"
                      className="accordion-collapse collapse"
                      aria-labelledby="headingThree"
                      data-bs-parent="#accordionExample"
                    >
                      <div className="accordion-body">
                        <p className="m-0">
                          <b>CVSS score:</b> 2.1
                        </p>
                        <p className="m-0">
                          <b>Severity</b> HIGH
                        </p>
                        <p className="m-0">Description</p>
                        <p className="m-0">
                          <a href="">Ref</a>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="accordion-item">
                    <h2 className="accordion-header" id="headingThree">
                      <button
                        className="accordion-button collapsed"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#collapseThree"
                        aria-expanded="false"
                        aria-controls="collapseThree"
                      >
                        DEP NAME #6
                      </button>
                    </h2>
                    <div
                      id="collapseThree"
                      className="accordion-collapse collapse"
                      aria-labelledby="headingThree"
                      data-bs-parent="#accordionExample"
                    >
                      <div className="accordion-body">
                        <p className="m-0">
                          <b>CVSS score:</b> 2.1
                        </p>
                        <p className="m-0">
                          <b>Severity</b> HIGH
                        </p>
                        <p className="m-0">Description</p>
                        <p className="m-0">
                          <a href="">Ref</a>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="accordion-item">
                    <h2 className="accordion-header" id="headingThree">
                      <button
                        className="accordion-button collapsed"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#collapseThree"
                        aria-expanded="false"
                        aria-controls="collapseThree"
                      >
                        DEP NAME #7
                      </button>
                    </h2>
                    <div
                      id="collapseThree"
                      className="accordion-collapse collapse"
                      aria-labelledby="headingThree"
                      data-bs-parent="#accordionExample"
                    >
                      <div className="accordion-body">
                        <p className="m-0">
                          <b>CVSS score:</b> 2.1
                        </p>
                        <p className="m-0">
                          <b>Severity</b> HIGH
                        </p>
                        <p className="m-0">Description</p>
                        <p className="m-0">
                          <a href="">Ref</a>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="accordion-item">
                    <h2 className="accordion-header" id="headingThree">
                      <button
                        className="accordion-button collapsed"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#collapseThree"
                        aria-expanded="false"
                        aria-controls="collapseThree"
                      >
                        DEP NAME #8
                      </button>
                    </h2>
                    <div
                      id="collapseThree"
                      className="accordion-collapse collapse"
                      aria-labelledby="headingThree"
                      data-bs-parent="#accordionExample"
                    >
                      <div className="accordion-body">
                        <p className="m-0">
                          <b>CVSS score:</b> 2.1
                        </p>
                        <p className="m-0">
                          <b>Severity</b> HIGH
                        </p>
                        <p className="m-0">Description</p>
                        <p className="m-0">
                          <a href="">Ref</a>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="accordion-item">
                    <h2 className="accordion-header" id="headingThree">
                      <button
                        className="accordion-button collapsed"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#collapseThree"
                        aria-expanded="false"
                        aria-controls="collapseThree"
                      >
                        DEP NAME #9
                      </button>
                    </h2>
                    <div
                      id="collapseThree"
                      className="accordion-collapse collapse"
                      aria-labelledby="headingThree"
                      data-bs-parent="#accordionExample"
                    >
                      <div className="accordion-body">
                        <p className="m-0">
                          <b>CVSS score:</b> 2.1
                        </p>
                        <p className="m-0">
                          <b>Severity</b> HIGH
                        </p>
                        <p className="m-0">Description</p>
                        <p className="m-0">
                          <a href="">Ref</a>
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="accordion-item">
                    <h2 className="accordion-header" id="headingThree">
                      <button
                        className="accordion-button collapsed"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#collapseThree"
                        aria-expanded="false"
                        aria-controls="collapseThree"
                      >
                        DEP NAME #10
                      </button>
                    </h2>
                    <div
                      id="collapseThree"
                      className="accordion-collapse collapse"
                      aria-labelledby="headingThree"
                      data-bs-parent="#accordionExample"
                    >
                      <div className="accordion-body">
                        <p className="m-0">
                          <b>CVSS score:</b> 2.1
                        </p>
                        <p className="m-0">
                          <b>Severity</b> HIGH
                        </p>
                        <p className="m-0">Description</p>
                        <p className="m-0">
                          <a href="">Ref</a>
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>
          <div className="col-4 d-flex flex-column gap-5 h-100">
            <section className="card p-4 license-security">
              <div className="d-flex justify-content-between align-items-center mb-2">
                <h2 className="m-0">LICENSE</h2>
                <h5 className="m-0">
                  <b>
                    {
                      data?.license_result.payload.license_stats_results
                        ?.repo_license.name
                    }
                  </b>
                </h5>
              </div>
              <div>
                <div className="row mb-4">
                  <div className="d-flex flex-row w-100 justify-content-between">
                    {/* <div> */}
                    <p className="m-0">
                      <b>spdx id</b>
                    </p>
                    <small>
                      {
                        data?.license_result.payload.license_stats_results
                          ?.repo_license.key
                      }
                    </small>
                  </div>
                  {/* </div> */}
                  {/* <div> */}
                  <div className="d-flex flex-row w-100 justify-content-between">
                    <p className="m-0">
                      <b>Deprecated</b>
                    </p>
                    <small>
                      {
                        data?.license_result.payload.license_stats_results
                          ?.license_data.isDeprecatedLicenseId
                      }
                    </small>
                  </div>
                  {/* <div> */}
                  <div className="d-flex flex-row w-100 justify-content-between">
                    <p className="m-0">
                      <b>OSI Approved</b>
                    </p>
                    <small>
                      {
                        data?.license_result.payload.license_stats_results
                          ?.license_data.isOsiApproved
                      }
                    </small>
                  </div>
                  {/* <div> */}
                  <div className="d-flex flex-row w-100 justify-content-between">
                    <p className="m-0">
                      <b>Reference</b>
                    </p>
                    <small>
                      <a
                        href={
                          data?.license_result.payload.license_stats_results
                            ?.license_data.reference
                        }
                      >
                        LICENSE
                      </a>
                    </small>
                  </div>
                </div>
                <h1>SECURITY</h1>
                <div className="row">
                  <h5>
                    <a href={data?.security_result.payload}>SECURITY FILE</a>
                  </h5>
                </div>
              </div>
            </section>
            <section className="card p-4 maintenance">
              <div className="d-flex flex-column justify-content-between align-items-center">
                <h4>NOT ARCHIVED / ARCHIVED</h4>
                <div className="commits-stats-list-wrapper w-100">
                  <ul className="commits-stats-list w-100 list-group">
                    <li className="list-group-item d-flex flex-row justify-content-evenly">
                      <b>Week #1</b>
                      <small>1251</small>
                    </li>
                    <li className="list-group-item d-flex flex-row justify-content-evenly">
                      <b>Week #1</b>
                      <small>1251</small>
                    </li>
                    <li className="list-group-item d-flex flex-row justify-content-evenly">
                      <b>Week #1</b>
                      <small>1251</small>
                    </li>
                    <li className="list-group-item d-flex flex-row justify-content-evenly">
                      <b>Week #1</b>
                      <small>1251</small>
                    </li>
                    <li className="list-group-item d-flex flex-row justify-content-evenly">
                      <b>Week #1</b>
                      <small>1251</small>
                    </li>
                    <li className="list-group-item d-flex flex-row justify-content-evenly">
                      <b>Week #1</b>
                      <small>1251</small>
                    </li>
                    <li className="list-group-item d-flex flex-row justify-content-evenly">
                      <b>Week #1</b>
                      <small>1251</small>
                    </li>
                    <li className="list-group-item d-flex flex-row justify-content-evenly">
                      <b>Week #1</b>
                      <small>1251</small>
                    </li>
                    <li className="list-group-item d-flex flex-row justify-content-evenly">
                      <b>Week #1</b>
                      <small>1251</small>
                    </li>
                    <li className="list-group-item d-flex flex-row justify-content-evenly">
                      <b>Week #1</b>
                      <small>1251</small>
                    </li>
                  </ul>
                </div>
              </div>
            </section>
            <section className="card p-4 package-criticality-score">
              <div>
                <h5 className="fw-bold">REPO is associated with a package</h5>
                <div className="d-flex justify-content-between">
                  <div>
                    <p className="m-0 fw-bold">Reference</p>
                    <a href="#">Express</a>
                  </div>
                  <div>
                    <p className="m-0 fw-bold">Platform</p>
                    <p>NPM</p>
                  </div>
                  <div>
                    <p className="m-0 fw-bold">Version</p>
                    <p>@1.0.0</p>
                  </div>
                </div>
              </div>
              <div className="d-flex flex-row">
                <h5 className="fw-bold flex-fill">CRITICALITY SCORE</h5>
                <h5 className="fw-bold flex-fill">
                  {data?.criticality_score_result.payload.criticality_score}
                </h5>
              </div>
            </section>
          </div>
        </div>
      </main>
    </div>
  ) : (
    <></>
  );
}
