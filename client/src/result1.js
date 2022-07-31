const report = {
  binary_artifacts_result: {
    signal: true,
    payload: { executables: ["black.exe", "python3.dll"] },
    message: "Repository has binary artifacts. Be careful",
  },
  branch_protection_result: {
    signal: true,
    payload: {
      branch_protection_score: 7,
      branch_protection_output: {
        branch_protected: true,
        not_allow_force_pushes: true,
        enforce_admins: true,
        requires_pull_request_reviews: true,
        required_approving_review_count: true,
        requires_status_checks: false,
        strict_status_checks: false,
        requires_commit_signatures: true,
      },
    },
    message: "Branch is protected and branch protection stats is accessible.",
  },
  badge_result: {
    signal: true,
    payload: {
      implementation_languages: ["JavaScript", "C++", "Python (CII estimate)"],
      tiered_percentage: 107,
      badge_level: "passing",
    },
    message: "Found CII Best practice badges",
  },
  code_review_result: {
    signal: true,
    payload: {
      archived: false,
      approving_review_count: null,
      protected: true,
      issues_stats: {
        open_issues: 1635,
        closed_issues: 13198,
        bug_issues: {
          "confirmed-bug": {
            url: "https://api.github.com/repos/nodejs/node/labels/confirmed-bug",
            count: 63,
          },
        },
      },
    },
    message: null,
  },
  contri_result: {
    signal: true,
    payload: {
      commits_since: "2022-07-24 19:34:54.864700",
      distinct_companies: [
        "tu wien",
        "aws",
        "postmanlabs",
        "igalia",
        "mongodb",
        "slackhq",
        "msft",
        "red hat",
        "testimio",
        "disney",
      ],
      legit_contributors: {
        MoLow: {
          company: "testimio",
          commits_count: 7,
          orgs: ["Node.js", "Testim.io"],
        },
        RaisinTen: {
          company: "postmanlabs",
          commits_count: 2,
          orgs: [
            "FOSSASIA",
            "Node.js",
            "Postman Inc.",
            "Electron",
            "Node.js Core Security",
            "First Contributions",
            "pkgjs",
            "The V++ Programming Language",
            "EddieHub",
            "WinterCG",
          ],
        },
        VerteDinde: {
          company: "slackhq",
          commits_count: 1,
          orgs: [
            "Electron",
            "Women Who Code Portland",
            "CrimethInc.",
            "The Collab Lab",
          ],
        },
        tniessen: {
          company: "tu wien",
          commits_count: 8,
          orgs: ["Node.js", "WebAssembly", "pkgjs", "None", "None", "WinterCG"],
        },
        addaleax: {
          company: "mongodb",
          commits_count: 1,
          orgs: ["Node.js", "Istanbul Code Coverage"],
        },
        danielleadams: {
          company: "aws",
          commits_count: 1,
          orgs: [
            "None",
            "Node.js",
            "Women Who Code NYC",
            "Cloud Native Buildpacks",
            "AWS Amplify",
            "pkgjs",
          ],
        },
        GeoffreyBooth: {
          company: "disney",
          commits_count: 1,
          orgs: ["CoffeeScript", "Node.js"],
        },
        BethGriggs: {
          company: "red hat",
          commits_count: 1,
          orgs: [
            "Ecma TC39",
            "Node.js",
            "None",
            "NodeShift by Red Hat",
            "pkgjs",
          ],
        },
        codebytere: {
          company: "msft",
          commits_count: 1,
          orgs: [
            "Ecma TC39",
            "Microsoft",
            "Node.js",
            "Electron",
            "Electron Userland",
            "OpenJS Foundation",
            "pkgjs",
            "QueerJS",
            "Continuous Auth",
          ],
        },
        andreubotella: {
          company: "igalia",
          commits_count: 1,
          orgs: ["Igalia", "WHATWG", "None"],
        },
      },
      total_commits: 66,
    },
    message: null,
  },
  dep_up_tool_result: {
    signal: false,
    payload: null,
    message: "Repository lacks dependency update tool",
  },
  dep_check: {
    signal: true,
    payload: {
      express: [
        {
          id: "sonatype-2012-0022",
          displayName: "sonatype-2012-0022",
          title:
            "[sonatype-2012-0022] CWE-113: Improper Neutralization of CRLF Sequences in HTTP Headers ('HTTP Response Splitting')",
          description:
            "expressjs - HTTP Splitting Attack\n\nThe software receives data from an upstream component, but does not neutralize or incorrectly neutralizes CR and LF characters before the data is included in outgoing HTTP headers.",
          cvssScore: 7.5,
          cvssVector: "CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N",
          cwe: "CWE-113",
          reference:
            "https://ossindex.sonatype.org/vulnerability/sonatype-2012-0022?component-type=npm&component-name=express&utm_source=python-requests&utm_medium=integration&utm_content=2.27.1",
          externalReferences: [],
        },
        {
          id: "sonatype-2021-0078",
          displayName: "sonatype-2021-0078",
          title: "[sonatype-2021-0078] CWE-23: Relative Path Traversal",
          description:
            "express + hbs - Local File Read via Path Traversal\n\nThe software uses external input to construct a pathname that should be within a restricted directory, but it does not properly neutralize sequences such as .. that can resolve to a location that is outside of that directory.",
          cvssScore: 5.9,
          cvssVector: "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N",
          cwe: "CWE-23",
          reference:
            "https://ossindex.sonatype.org/vulnerability/sonatype-2021-0078?component-type=npm&component-name=express&utm_source=python-requests&utm_medium=integration&utm_content=2.27.1",
          externalReferences: [],
        },
      ],
      marked: [
        {
          id: "CVE-2022-21680",
          displayName: "CVE-2022-21680",
          title:
            "[CVE-2022-21680] Marked is a markdown parser and compiler. Prior to version 4.0.10, the regular expression `block.def` may cause catastrophic backtracking against some strings and lead to a regular expression denial of service (ReDoS). Anyone who runs untrusted markdown through a vulnerable version of marked and does not use a worker with a time limit may be affected. This issue is patched in version 4.0.10. As a workaround, avoid running untrusted markdown through marked or run marked on a worker thread and set a reasonable time limit to prevent draining resources.",
          description:
            "Marked is a markdown parser and compiler. Prior to version 4.0.10, the regular expression `block.def` may cause catastrophic backtracking against some strings and lead to a regular expression denial of service (ReDoS). Anyone who runs untrusted markdown through a vulnerable version of marked and does not use a worker with a time limit may be affected. This issue is patched in version 4.0.10. As a workaround, avoid running untrusted markdown through marked or run marked on a worker thread and set a reasonable time limit to prevent draining resources.",
          cvssScore: 7.5,
          cvssVector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
          cwe: "CWE-1333",
          cve: "CVE-2022-21680",
          reference:
            "https://ossindex.sonatype.org/vulnerability/CVE-2022-21680?component-type=npm&component-name=marked&utm_source=python-requests&utm_medium=integration&utm_content=2.27.1",
          externalReferences: [
            "http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2022-21680",
            "https://github.com/markedjs/marked/releases/tag/v4.0.10",
            "https://github.com/markedjs/marked/security/advisories/GHSA-rrrm-qjm4-v8hf",
          ],
        },
      ],
      hbs: [
        {
          id: "sonatype-2021-0078",
          displayName: "sonatype-2021-0078",
          title: "[sonatype-2021-0078] CWE-23: Relative Path Traversal",
          description:
            "express + hbs - Local File Read via Path Traversal\n\nThe software uses external input to construct a pathname that should be within a restricted directory, but it does not properly neutralize sequences such as .. that can resolve to a location that is outside of that directory.",
          cvssScore: 5.9,
          cvssVector: "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N",
          cwe: "CWE-23",
          reference:
            "https://ossindex.sonatype.org/vulnerability/sonatype-2021-0078?component-type=npm&component-name=hbs&utm_source=python-requests&utm_medium=integration&utm_content=2.27.1",
          externalReferences: [],
        },
        {
          id: "CVE-2021-32822",
          displayName: "CVE-2021-32822",
          title:
            "[CVE-2021-32822] CWE-94: Improper Control of Generation of Code ('Code Injection')",
          description:
            "The npm hbs package is an Express view engine wrapper for Handlebars. Depending on usage, users of hbs may be vulnerable to a file disclosure vulnerability. There is currently no patch for this vulnerability. hbs mixes pure template data with engine configuration options through the Express render API. By overwriting internal configuration options a file disclosure vulnerability may be triggered in downstream applications. For an example PoC see the referenced GHSL-2021-020.",
          cvssScore: 5.3,
          cvssVector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
          cwe: "CWE-94",
          cve: "CVE-2021-32822",
          reference:
            "https://ossindex.sonatype.org/vulnerability/CVE-2021-32822?component-type=npm&component-name=hbs&utm_source=python-requests&utm_medium=integration&utm_content=2.27.1",
          externalReferences: [
            "http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2021-32822",
            "https://www.cybersecurity-help.cz/vdb/SB2021082412",
            "https://github.com/advisories/GHSA-7f5c-rpf4-86p8",
            "https://securitylab.github.com/advisories/GHSL-2021-020-pillarjs-hbs/",
          ],
        },
      ],
      eslint: [
        {
          id: "sonatype-2018-0379",
          displayName: "sonatype-2018-0379",
          title:
            "[sonatype-2018-0379] CWE-400: Uncontrolled Resource Consumption ('Resource Exhaustion')",
          description:
            "eslint - catastrophic backtracking\n\nThe software does not properly restrict the size or amount of resources that are requested or influenced by an actor, which can be used to consume more resources than intended.",
          cvssScore: 4.4,
          cvssVector: "CVSS:3.0/AV:L/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H",
          cwe: "CWE-400",
          reference:
            "https://ossindex.sonatype.org/vulnerability/sonatype-2018-0379?component-type=npm&component-name=eslint&utm_source=python-requests&utm_medium=integration&utm_content=2.27.1",
          externalReferences: [],
        },
      ],
      ejs: [
        {
          id: "CVE-2022-29078",
          displayName: "CVE-2022-29078",
          title:
            "[CVE-2022-29078] CWE-74: Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection')",
          description:
            "The ejs (aka Embedded JavaScript templates) package 3.1.6 for Node.js allows server-side template injection in settings[view options][outputFunctionName]. This is parsed as an internal option, and overwrites the outputFunctionName option with an arbitrary OS command (which is executed upon template compilation).",
          cvssScore: 9.8,
          cvssVector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
          cwe: "CWE-74",
          cve: "CVE-2022-29078",
          reference:
            "https://ossindex.sonatype.org/vulnerability/CVE-2022-29078?component-type=npm&component-name=ejs&utm_source=python-requests&utm_medium=integration&utm_content=2.27.1",
          externalReferences: [
            "http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2022-29078",
            "https://eslam.io/posts/ejs-server-side-template-injection-rce/",
            "https://github.com/mde/ejs/issues/451",
          ],
        },
        {
          id: "sonatype-2021-0438",
          displayName: "sonatype-2021-0438",
          title:
            "[sonatype-2021-0438] CWE-94: Improper Control of Generation of Code ('Code Injection')",
          description:
            "ejs - Remote Code Execution (RCE)\n\nThe software constructs all or part of a code segment using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the syntax or behavior of the intended code segment.",
          cvssScore: 9.8,
          cvssVector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
          cwe: "CWE-94",
          reference:
            "https://ossindex.sonatype.org/vulnerability/sonatype-2021-0438?component-type=npm&component-name=ejs&utm_source=python-requests&utm_medium=integration&utm_content=2.27.1",
          externalReferences: [],
        },
      ],
      mocha: [
        {
          id: "sonatype-2021-1683",
          displayName: "sonatype-2021-1683",
          title: "[sonatype-2021-1683] Unknown",
          description:
            "mocha - Regular Expression Denial of Service (ReDoS)\n\nmocha - Regular Expression Denial of Service (ReDoS)",
          cvssScore: 7.5,
          cvssVector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
          cwe: "CWE-1333",
          reference:
            "https://ossindex.sonatype.org/vulnerability/sonatype-2021-1683?component-type=npm&component-name=mocha&utm_source=python-requests&utm_medium=integration&utm_content=2.27.1",
          externalReferences: [],
        },
        {
          id: "sonatype-2021-4946",
          displayName: "sonatype-2021-4946",
          title: "[sonatype-2021-4946] Unknown",
          description:
            "mocha - Regular Expression Denial of Service (ReDoS)\n\nmocha - Regular Expression Denial of Service (ReDoS)",
          cvssScore: 7.5,
          cvssVector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
          cwe: "CWE-1333",
          reference:
            "https://ossindex.sonatype.org/vulnerability/sonatype-2021-4946?component-type=npm&component-name=mocha&utm_source=python-requests&utm_medium=integration&utm_content=2.27.1",
          externalReferences: [],
        },
      ],
    },
    message: null,
  },
  license_result: {
    signal: true,
    payload: {
      license_stats_results: {
        exists: true,
        repo_license: {
          key: "mit",
          name: "MIT License",
          spdx_id: "MIT",
          url: "https://api.github.com/licenses/mit",
          node_id: "MDc6TGljZW5zZTEz",
          html_url: "http://choosealicense.com/licenses/mit/",
          description:
            "A short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code.",
          implementation:
            "Create a text file (typically named LICENSE or LICENSE.txt) in the root of your source code and copy the text of the license into the file. Replace [year] with the current year and [fullname] with the name (or names) of the copyright holders.",
          permissions: [
            "commercial-use",
            "modifications",
            "distribution",
            "private-use",
          ],
          conditions: ["include-copyright"],
          limitations: ["liability", "warranty"],
          body: 'MIT License\n\nCopyright (c) [year] [fullname]\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
          featured: true,
        },
        license_data: {
          isDeprecatedLicenseId: false,
          licenseId: "MIT",
          isOsiApproved: true,
          name: "MIT License",
          reference: "https://spdx.org/licenses/MIT.html",
        },
      },
      license_score: 3,
    },
    message: "License data fetched",
  },
  security_result: {
    signal: true,
    payload: "https://github.com/expressjs/express/tree/master/Security.md",
    message: "Security file found",
  },
  maintenance_result: {
    signal: true,
    payload: {
      "2021-08-01 00:00:00": 1,
      "2021-08-08 00:00:00": 2,
      "2021-08-15 00:00:00": 0,
      "2021-08-22 00:00:00": 0,
      "2021-08-29 00:00:00": 2,
      "2021-09-05 00:00:00": 0,
      "2021-09-12 00:00:00": 0,
      "2021-09-19 00:00:00": 0,
      "2021-09-26 00:00:00": 1,
      "2021-10-03 00:00:00": 1,
      "2021-10-10 00:00:00": 0,
      "2021-10-17 00:00:00": 0,
      "2021-10-24 00:00:00": 0,
      "2021-10-31 00:00:00": 1,
      "2021-11-07 00:00:00": 0,
      "2021-11-14 00:00:00": 3,
      "2021-11-21 00:00:00": 1,
      "2021-11-28 00:00:00": 0,
      "2021-12-05 00:00:00": 7,
      "2021-12-12 00:00:00": 8,
      "2021-12-19 00:00:00": 0,
      "2021-12-26 00:00:00": 0,
      "2022-01-02 00:00:00": 0,
      "2022-01-09 00:00:00": 0,
      "2022-01-16 00:00:00": 0,
      "2022-01-23 00:00:00": 1,
      "2022-01-30 00:00:00": 19,
      "2022-02-06 00:00:00": 5,
      "2022-02-13 00:00:00": 5,
      "2022-02-20 00:00:00": 8,
      "2022-02-27 00:00:00": 6,
      "2022-03-06 00:00:00": 1,
      "2022-03-13 00:00:00": 1,
      "2022-03-20 00:00:00": 8,
      "2022-03-27 00:00:00": 4,
      "2022-04-03 00:00:00": 6,
      "2022-04-10 00:00:00": 4,
      "2022-04-17 00:00:00": 3,
      "2022-04-24 00:00:00": 8,
      "2022-05-01 00:00:00": 0,
      "2022-05-08 00:00:00": 0,
      "2022-05-15 00:00:00": 6,
      "2022-05-22 00:00:00": 0,
      "2022-05-29 00:00:00": 0,
      "2022-06-05 00:00:00": 0,
      "2022-06-12 00:00:00": 0,
      "2022-06-19 00:00:00": 0,
      "2022-06-26 00:00:00": 0,
      "2022-07-03 00:00:00": 0,
      "2022-07-10 00:00:00": 0,
      "2022-07-17 00:00:00": 0,
      "2022-07-24 00:00:00": 0,
    },
    message:
      "Fetched commit data. Track frequency of code commits to measure maintenance metric",
  },
  repo_is_pack_result: {
    signal: true,
    payload: [
      {
        dependent_repos_count: 1122978,
        dependents_count: 74366,
        deprecation_reason: null,
        description: "Fast, unopinionated, minimalist web framework",
        forks: 9702,
        homepage: "http://expressjs.com/",
        keywords: [
          "express",
          "framework",
          "sinatra",
          "web",
          "http",
          "rest",
          "restful",
          "router",
          "app",
          "api",
          "javascript",
          "nodejs",
          "server",
        ],
        language: "JavaScript",
        latest_download_url:
          "https://registry.npmjs.org/express/-/express-4.18.1.tgz",
        latest_release_number: "4.18.1",
        latest_release_published_at: "2022-04-29T19:33:40.441Z",
        latest_stable_release_number: "4.18.1",
        latest_stable_release_published_at: "2022-04-29T19:33:40.441Z",
        license_normalized: false,
        licenses: "MIT",
        name: "express",
        normalized_licenses: ["MIT"],
        package_manager_url: "https://www.npmjs.com/package/express",
        platform: "NPM",
        rank: 32,
        repository_license: "MIT",
        repository_url: "https://github.com/expressjs/express",
        stars: 57180,
        status: "",
      },
    ],
    message: "Repository has package(s) associated with it",
  },
  criticality_score_result: {
    signal: true,
    payload: {
      name: "express",
      url: "https://github.com/expressjs/express",
      language: "JavaScript",
      description: "Fast, unopinionated, minimalist web framework for node.",
      created_since: 159,
      updated_since: 2,
      contributor_count: 317,
      watchers_count: 57804,
      org_count: 9,
      commit_frequency: 2.1,
      recent_releases_count: 5,
      updated_issues_count: 94,
      closed_issues_count: 42,
      comment_frequency: 2.0,
      dependents_count: 5758,
      criticality_score: 0.6708,
    },
    message: "Calculated criticality score with other repository stats",
  },
};
export default report;
