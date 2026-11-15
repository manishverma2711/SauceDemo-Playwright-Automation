
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "allure-results"
REPORT = ROOT / "allure-report"


def customize_allure():
    index_file = REPORT / "index.html"

    if not index_file.exists():
        print("ERROR: Generate Allure report first.")
        return

    test_cases = []

    for file in RESULTS.glob("*-result.json"):
        data = json.loads(file.read_text(encoding="utf-8"))

        start = data.get("start", 0)
        stop = data.get("stop", 0)

        test_cases.append({
            "name": data.get("name", "Unknown Test"),
            "status": data.get("status", "unknown"),
            "duration": round(max(0, stop - start) / 1000, 2)
        })

    if not test_cases:
        print("ERROR: No test results found.")
        return

    test_cases.sort(
        key=lambda t: [
            int(x) if x.isdigit() else x.lower()
            for x in re.split(r"(\d+)", t["name"])
        ]
    )

    test_data = json.dumps(test_cases).replace("<", "\\u003c")

    css = """
    <style id="simple-allure-style">
      #simple-allure-report {
        background: #ffffff;
        padding: 24px;
        margin: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px #00000012;
        color: #222;
      }

      #simple-allure-report h2 {
        margin: 0 0 20px;
        font-size: 22px;
      }

      .simple-summary {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-bottom: 20px;
      }

      .simple-card {
        background: #f1f4f8;
        padding: 15px 24px;
        border-radius: 8px;
      }

      .simple-card strong {
        display: block;
        font-size: 24px;
      }

      .simple-table {
        width: 100%;
        border-collapse: collapse;
      }

      .simple-table th,
      .simple-table td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #e5e7eb;
      }

      .simple-table th {
        background: #f3f4f6;
      }

      .simple-badge {
        font-size: 12px;
        font-weight: bold;
        padding: 5px 12px;
        border-radius: 15px;
      }

      .simple-passed {
        background: #dcfce7;
        color: #166534;
      }

      .simple-failed {
        background: #fee2e2;
        color: #991b1b;
      }

      .simple-broken {
        background: #fef3c7;
        color: #92400e;
      }

      .simple-skipped {
        background: #e5e7eb;
        color: #374151;
      }
    </style>
    """

    javascript = """
    <script id="simple-allure-script">
    (() => {
      const tests = __TEST_DATA__;

      function updateReport() {
        const hash = window.location.hash;
        const overview = (
          hash === "" ||
          hash === "#" ||
          hash === "#/" ||
          hash === "#overview"
        );

        const grid = document.querySelector(".widgets-grid");
        const existing = document.getElementById(
          "simple-allure-report"
        );

        if (!overview) {
          if (existing) existing.remove();
          if (grid) grid.style.display = "";
          return;
        }

        if (!grid) return;

        grid.style.display = "none";
        if (existing) return;

        const report = document.createElement("div");
        report.id = "simple-allure-report";

        const title = document.createElement("h2");
        title.textContent = "SauceDemo Automation Test Report";
        report.appendChild(title);

        const summary = document.createElement("div");
        summary.className = "simple-summary";

        const statuses = [
          ["Total", tests.length],
          ["Passed", tests.filter(t => t.status === "passed").length],
          ["Failed", tests.filter(t => t.status === "failed").length],
          ["Broken", tests.filter(t => t.status === "broken").length],
          ["Skipped", tests.filter(t => t.status === "skipped").length]
        ];

        statuses.forEach(([label, count]) => {
          const card = document.createElement("div");
          card.className = "simple-card";

          const number = document.createElement("strong");
          number.textContent = count;

          card.appendChild(number);
          card.appendChild(document.createTextNode(label));
          summary.appendChild(card);
        });

        report.appendChild(summary);

        const table = document.createElement("table");
        table.className = "simple-table";

        const header = table.createTHead().insertRow();
        ["Sr. No.", "Test Case", "Duration", "Status"]
          .forEach(label => {
            const th = document.createElement("th");
            th.textContent = label;
            header.appendChild(th);
          });

        const body = table.createTBody();

        tests.forEach((test, index) => {
          const row = body.insertRow();

          [
            index + 1,
            test.name,
            test.duration + " sec"
          ].forEach(value => {
            const cell = row.insertCell();
            cell.textContent = value;
          });

          const statusCell = row.insertCell();
          const badge = document.createElement("span");

          badge.className =
            "simple-badge simple-" + test.status;
          badge.textContent = test.status.toUpperCase();

          statusCell.appendChild(badge);
        });

        report.appendChild(table);
        grid.parentNode.insertBefore(report, grid);
      }

      window.addEventListener("hashchange", updateReport);

      const observer = new MutationObserver(updateReport);

      document.addEventListener("DOMContentLoaded", () => {
        observer.observe(document.body, {
          childList: true,
          subtree: true
        });
        updateReport();
      });
    })();
    </script>
    """

    javascript = javascript.replace("__TEST_DATA__", test_data)

    html = index_file.read_text(encoding="utf-8")

    # Avoid inserting duplicate customization.
    if 'id="simple-allure-script"' in html:
        print("Report already customized. Regenerate it first.")
        return

    if "</body>" not in html:
        print("ERROR: Cannot find closing body tag.")
        return

    html = html.replace(
        "</body>",
        css + javascript + "</body>",
        1
    )

    index_file.write_text(html, encoding="utf-8")

    print(f"SUCCESS: Added {len(test_cases)} test cases.")
    print(f"Customized report: {index_file}")


if __name__ == "__main__":
    customize_allure()
