import report from './assets/reports/expressjs_express'
import React, { useEffect, useState } from 'react'
import Score from './Score'

export default function Report (props) {
  const [data, setData] = useState(null)
  useEffect(() => {
    setData(report)
  }, [])

  return data ? (
    <div className='w-100 container mt-4 mb-5'>
      <header className='d-flex justify-content-center gap-4 align-items-center p-3'>
        <h1 className='fw-bold'>
          <a
            target={'_blank'}
            href={data?.REPO_IS_PACK_RESULT.payload[0].repository_url}
            className='link-primary text-decoration-none'
          >
            Repository: {data?.CRITICALITY_SCORE_RESULT.payload.name}/
            {/* REPOSITORY OWNER */}
            {data?.CRITICALITY_SCORE_RESULT.payload.name}
            {/* REPOSITORY NAME */}
          </a>
        </h1>

        <Score score={data?.RESULT_SCORE} />
      </header>

      <p className='w-100 text-end'>
        For more info, refer <code>JSON file</code> in the{' '}
        <code>assets/reports</code> directory
      </p>

      <main className='w-100'>
        <div className='d-flex w-100 flex-wrap row'>
          <div className='col-4 d-flex flex-column gap-5 h-100'>
            <section className='card p-4 binary-artifacts '>
              <Score score={data?.BINARY_ARTIFACTS_RESULT.score} />
              <h3 className='text-center'>BINARY ARTIFACTS</h3>
              <div className='d-flex binary-artifacts-content'>
                <h1 className='flex-grow-1 center-element w-100'>
                  {data?.BINARY_ARTIFACTS_RESULT.payload.executables.length}
                </h1>
                <br />
                <ul className='list-unstyled flex-grow-1 center-element w-100 flex-column align-items-start'>
                  {data?.BINARY_ARTIFACTS_RESULT.payload.executables.map(
                    (item, idx) => {
                      return (
                        <li key={idx}>
                          <code>{item}</code>
                        </li>
                      )
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
            <section className='card p-4 badges'>
              <Score score={data?.BADGE_RESULT.score} />
              <h3 className='text-center'>BEST PRACTICE BADGE</h3>
              {data?.BADGE_RESULT.signal ? (
                <div className='d-flex flex-column badges-content align-items-center'>
                  <div className='d-flex justify-content-evenly py-3 w-100'>
                    <h1 className='flex-grow-1 center-element w-100'>
                      {data?.BADGE_RESULT.payload.tiered_percentage}%
                    </h1>

                    <h1 className='flex-grow-1 center-element w-100'>
                      {data?.BADGE_RESULT.payload.badge_level}
                    </h1>
                  </div>
                  <ul className='impl-langs d-flex m-0 px-0 py-1 w-100 list-group-horizontal'>
                    {data?.BADGE_RESULT.payload.implementation_languages.map(
                      (item, idx) => {
                        return (
                          <li key={idx} className='list-group-item'>
                            {item}
                          </li>
                        )
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
              ) : (
                <p>No badge found</p>
              )}
            </section>
            <section className='card p-4 code-review'>
              <Score score={data?.CODE_REVIEW_RESULT.score} />
              <h3 className='text-center text-wrap'>
                CODE REVIEW AND AWARENESS
              </h3>
              <div className='code-review-content'>
                <h2 className='text-center py-2'>PROTECTED</h2>
                <h4 className='text-center py-2'>REVIEWER COUNT: 8</h4>
                <div className='issues-content'>
                  <div className='d-flex justify-content-evenly align-items-center py-2 w-100'>
                    <h6 className='w-50 text-center'>
                      OPEN ISSUES :{' '}
                      {
                        data?.CODE_REVIEW_RESULT.payload.issues_stats
                          .open_issues
                      }
                    </h6>
                    <h6 className='w-50 text-center'>
                      CLOSED ISSUES :{' '}
                      {
                        data?.CODE_REVIEW_RESULT.payload.issues_stats
                          .closed_issues
                      }
                    </h6>
                  </div>
                  <ul className='issues-list d-flex m-0 px-0 py-1 w-100 list-group-horizontal'>
                    {Object.entries(
                      data?.CODE_REVIEW_RESULT.payload.issues_stats.bug_issues
                    ).map(bug_issue => {
                      return (
                        <li className='list-group-item'>
                          <div>
                            {/* <div class="d-flex justify-content-between"> */}
                            <h4 className='mb-0'>{bug_issue[0]}</h4>
                            <small>{bug_issue[1].count}</small>
                            <br />
                            <a href={bug_issue[1].url}>bugs reference link</a>
                          </div>
                        </li>
                      )
                    })}
                  </ul>
                </div>
              </div>
            </section>
          </div>
          <div className='col-4 d-flex flex-column gap-5 h-100'>
            <section className='card p-4 contributors'>
              <div className='d-flex justify-content-between align-items-start mb-2'>
                <h3 className='text-center text-wrap'>CONTRIBUTORS</h3>
                <Score score={data?.CONTRI_RESULT.score} />
              </div>

              <div className='contributors-content'>
                <div className='d-flex w-100 mb-3'>
                  <div className='d-flex w-100 flex-column align-items-start'>
                    <b>TOTAL COMMITS</b>
                    <h5>{data?.CONTRI_RESULT.payload.total_commits}</h5>
                  </div>
                  <div className='d-flex w-100 flex-column align-items-start'>
                    <b>LEGIT CONTRIBUTORS</b>
                    <h5>
                      {
                        Object.keys(
                          data?.CONTRI_RESULT.payload.legit_contributors
                        ).length
                      }
                    </h5>
                  </div>
                </div>
                <div className='mb-3'>
                  <h6 className='text-start ps-3 pt-1 mb-0'>
                    CONTRIBUTORS COMPANY
                  </h6>
                  <p>
                    {data?.CONTRI_RESULT.payload.distinct_companies.map(
                      (item, idx) => {
                        return <span key={idx}>{item}, </span>
                      }
                    )}
                  </p>
                  <div className='issues-list-wrapper'>
                    <ul className='issues-list d-flex m-0 px-0 py-1 w-100 list-group'>
                      {Object.keys(
                        data?.CONTRI_RESULT.payload.legit_contributors
                      ).map(function (key, idx) {
                        return (
                          <li className='list-group-item' key={idx} value={key}>
                            <div className='d-flex justify-content-between'>
                              <b>COMMIT AUTHOR:{key}</b>
                              <small>{key.commits_count}</small>
                              <small>{key.company}</small>
                            </div>
                            <p className='m-0'>
                              {key.orgs.map((item, idx) => {
                                return (
                                  <span
                                    className='bg-dark text-light p-1'
                                    key={idx}
                                  >
                                    {item}
                                  </span>
                                )
                              })}
                            </p>
                          </li>
                        )
                      })}
                    </ul>
                  </div>
                </div>
              </div>
            </section>

            <section className='card p-4 dependency-update-tool'>
              <div className='d-flex justify-content-between align-items-start mb-2'>
                <b>
                  {data?.DEP_UP_TOOL_RESULT.signal ? (
                    <a href={data?.DEP_UP_TOOL_RESULT.payload}>
                      Dependency Update tool
                    </a>
                  ) : (
                    'No dependency update tool'
                  )}
                </b>
                <Score score={data?.DEP_UP_TOOL_RESULT.score} />
              </div>

              <div className='accordion-wrapper'>
                <div className='d-flex justify-content-between align-items-start mb-2'>
                  <h6>VULNERABLE DEPENDENCIES</h6>
                  <Score score={data?.DEP_CHECK.score} />
                </div>

                <div className='accordion' id='accordionExample'>
                  {data?.DEP_CHECK.signal &&
                    Object.entries(data?.DEP_CHECK.payload).map(dep => {
                      return (
                        <div className='accordion-item'>
                          <h2
                            className='accordion-header'
                            id={'heading' + dep[0]}
                          >
                            <button
                              className='accordion-button'
                              type='button'
                              data-bs-toggle='collapse'
                              data-bs-target={'#collapse' + dep[0]}
                              aria-expanded='false'
                              aria-controls={'collapse' + dep[0]}
                            >
                              {dep[0]}
                            </button>
                          </h2>
                          <div
                            id={'collapse' + dep[0]}
                            className='accordion-collapse collapse'
                            aria-labelledby={'heading' + dep[0]}
                            data-bs-parent='#accordionExample'
                          >
                            <div className='accordion-body'>
                              <p className='m-0'>
                                <b>CVSS score:</b> dep[1]?.cvssScore
                              </p>
                              <p className='m-0'>
                                <b>dep[1]?.title</b>
                              </p>
                              <p className='m-0'>dep[1]?.description</p>
                              <p className='m-0'>
                                <a href={dep[1]?.reference}>Reference</a>
                              </p>
                            </div>
                          </div>
                        </div>
                      )
                    })}
                </div>
              </div>
            </section>
          </div>

          <div className='col-4 d-flex flex-column gap-5 h-100'>
            <section className='card p-4 license-security'>
              <div className='d-flex justify-content-between align-items-center mb-2'>
                <h2 className='m-0'>LICENSE</h2>
                <h5 className='m-0'>
                  <b>
                    {
                      data?.LICENSE_RESULT.payload?.license_stats_results
                        ?.repo_license.name
                    }
                  </b>
                </h5>
                <Score score={data?.LICENSE_RESULT.score} />
              </div>
              <div>
                <div className='row mb-4'>
                  <div className='d-flex flex-row w-100 justify-content-between'>
                    {/* <div> */}
                    <p className='m-0'>
                      <b>spdx id</b>
                    </p>
                    <small>
                      {
                        data?.LICENSE_RESULT.payload.license_stats_results
                          ?.repo_license.key
                      }
                    </small>
                  </div>
                  {/* </div> */}
                  {/* <div> */}
                  <div className='d-flex flex-row w-100 justify-content-between'>
                    <p className='m-0'>
                      <b>Deprecated</b>
                    </p>
                    <small>
                      {
                        data?.LICENSE_RESULT.payload.license_stats_results
                          ?.license_data.isDeprecatedLicenseId
                      }
                    </small>
                  </div>
                  {/* <div> */}
                  <div className='d-flex flex-row w-100 justify-content-between'>
                    <p className='m-0'>
                      <b>OSI Approved</b>
                    </p>
                    <small>
                      {
                        data?.LICENSE_RESULT.payload.license_stats_results
                          ?.license_data.isOsiApproved
                      }
                    </small>
                  </div>
                  {/* <div> */}
                  <div className='d-flex flex-row w-100 justify-content-between'>
                    <p className='m-0'>
                      <b>Reference</b>
                    </p>
                    <small>
                      <a
                        href={
                          data?.LICENSE_RESULT.payload.license_stats_results
                            ?.license_data.reference
                        }
                      >
                        LICENSE
                      </a>
                    </small>
                  </div>
                </div>
                <div className='d-flex justify-content-between align-items-start mb-2'>
                  <h2>SECURITY</h2>
                  <Score score={data?.SECURITY_RESULT.score} />
                </div>
                <div className='row'>
                  <h5>
                    <a href={data?.SECURITY_RESULT.payload}>SECURITY FILE</a>
                  </h5>
                </div>
              </div>
            </section>
            <section className='card p-4 maintenance'>
              <div className='d-flex flex-column justify-content-between align-items-center'>
                <div className='d-flex justify-content-between w-100'>
                  <Score score={data?.MAINTENANCE_RESULT.score} />
                  <h4>
                    {data?.MAINTENANCE_RESULT.signal
                      ? 'NOT ARCHIVED'
                      : 'ARCHIVED'}
                  </h4>
                </div>
                <div className='commits-stats-list-wrapper w-100'>
                  <ul className='commits-stats-list w-100 list-group'>
                    {Object.entries(data?.MAINTENANCE_RESULT.payload).map(
                      week => {
                        return (
                          <li className='list-group-item d-flex flex-row justify-content-evenly'>
                            <b>{week[0]}</b>
                            <small>{week[1]}</small>
                          </li>
                        )
                      }
                    )}
                  </ul>
                </div>
              </div>
            </section>

            <section className='card p-4 package-criticality-score'>
              <div>
                <Score score={data?.REPO_IS_PACK_RESULT.score} />
                <h5 className='fw-bold'>{data?.REPO_IS_PACK_RESULT.message}</h5>
                {data?.REPO_IS_PACK_RESULT.payload && (
                  <div className='d-flex justify-content-between'>
                    <div>
                      <p className='m-0 fw-bold'>Reference</p>
                      <a
                        href={
                          data?.REPO_IS_PACK_RESULT.payload[0]
                            .package_manager_url
                        }
                      >
                        {data?.REPO_IS_PACK_RESULT.payload[0].name}
                      </a>
                    </div>
                    <div>
                      <p className='m-0 fw-bold'>Platform</p>
                      <p>{data?.REPO_IS_PACK_RESULT.payload[0].platform}</p>
                    </div>
                    <div>
                      <p className='m-0 fw-bold'>Version</p>
                      <p>
                        {
                          data?.REPO_IS_PACK_RESULT.payload[0]
                            .latest_stable_release_number
                        }
                      </p>
                    </div>
                  </div>
                )}
              </div>
              <div className='d-flex  justify-content-between align-items-center my-2'>
                <h5 className='fw-bold flex-fill'>CRITICALITY SCORE</h5>
                <Score
                  score={
                    data?.CRITICALITY_SCORE_RESULT.payload.criticality_score
                  }
                />
              </div>
            </section>
          </div>
        </div>
      </main>
    </div>
  ) : (
    <></>
  )
}
