Nice — ambitious and exactly the right direction, Rohit. Below I’ll compare the two approaches side-by-side (Playwright MCP vs your Selenium MCP) for your goal — triggering + self-healing pytest Selenium scripts inside an existing framework — and then give a concrete, actionable implementation plan (components, endpoints, meta-flow, prompts, heuristics, CI, monitoring, safety). I’ll also include small example snippets you can drop into your Selenium MCP to get started with “run test” + self-heal.


---

Summary recommendation (quick)

If you want minimum friction to keep using your existing pytest Selenium test suite, build an enhanced Selenium MCP (what you already started). It fits directly into pytest, drivers, existing libraries, and is simplest to make “run and self-heal” tests.

If you want the cleanest LLM + semantic input (best for robust action reasoning), use Playwright’s accessibility snapshot as the context provider (or use Chromium CDP via Selenium to get the same tree). Best final architecture: hybrid — accessibility snapshots (Playwright or CDP) for LLM reasoning + Selenium MCP to execute and patch existing tests.



---

Side-by-side comparison

1) Purpose & Fit

Playwright MCP

Purpose-built MCP for Playwright interactions and accessibility snapshots.

Designed to let LLMs reason with semantic accessibility trees easily.

Not natively designed to execute an existing pytest Selenium test suite.


Selenium MCP (your repo)

Directly executes Selenium WebDriver and integrates with existing pytest tests and test fixtures.

Natural fit for teams that already have large Selenium/test frameworks.



2) Capturing page context for LLMs

Playwright

page.accessibility.snapshot() — structured, semantically rich, cross-browser (Chromium/Firefox/WebKit).

Great for LLMs to infer user intent (roles, names).


Selenium

Raw DOM via element.get_attribute('outerHTML') (what you already have).

Can get accessibility tree via Chrome DevTools Protocol: driver.execute_cdp_cmd("Accessibility.getFullAXTree", {}) — yields the same kind of tree as Playwright (Chromium-only).

Best approach: use CDP accessibility + raw HTML (hybrid).



3) Triggering existing tests

Playwright MCP

Could run shell commands from MCP server to launch pytest, but Playwright MCP’s native tools focus on Playwright actions — not running external pytest scripts.

Triggering pytest from Playwright MCP is possible but awkward (would require subprocess + mapping back results).


Selenium MCP

Native fit. Add a tool run_pytest that spawns pytest (or pytest -k testname --json-report) and streams/returns results. Easier to correlate logs, failures, and stack traces.



4) Self-healing capability (practicality)

Playwright + Accessibility

LLM receives semantic snapshot and can suggest robust selectors (role+name, ARIA, text).

But patching existing Selenium tests requires translating semantic locators into Selenium locators and committing patches — so extra glue needed.


Selenium MCP

Easier to implement self-heal: when a pytest fails, capture context (DOM snippet, accessibility tree via CDP, screenshot, stack trace), run LLM to generate fallback locators or replacement code, validate by running small locator verification steps, patch test file, re-run failing test. Directly touches the Python files that run in CI.



5) Cross-browser & WebComponent/Shadow DOM

Playwright

Strong cross-browser support and handles shadow DOM semantics in Accessibility snapshot.


Selenium

Raw DOM capture works; CDP accessibility is Chromium-only (so limited for Firefox/WebKit unless you use vendor-specific mechanisms or Playwright). Shadow DOM may need manual traversal (open), closed shadow roots are browser-dependent.



6) Performance & stability

Playwright snapshot is small and semantic — good for LLM tokens + faster reasoning.

Selenium raw HTML snapshots are larger (noisy) but you can compress/summarize. CDP accessibility output is similar to Playwright but heavier.


7) Security / Execution Risks

Running pytest / patching tests requires elevated permissions on the MCP server; ensure sandboxing, auth, and audit logs. Both approaches require careful security controls.



---

What needs to be implemented (concrete plan)

Below I outline a practical architecture and stepwise feature list to achieve your goal: Selenium MCP server that triggers, diagnoses failures, uses LLM to propose fixes, validates fixes, and patches pytest Selenium tests.

Architecture (high level)

1. Selenium MCP server (your existing FastMCP app) — orchestration & tools (start/stop browser, navigate, capture_html, capture_accessibility_tree)


2. Test runner tool — a tool in MCP to run pytest (single test or test module), streaming logs and exit code.


3. Failure snapshot collector — collects:

failing test stack trace

browser screenshot

accessibility tree (CDP) and outerHTML of relevant element(s)

network logs or console logs (optional)



4. LLM agent — prompt templates + model call(s) to:

propose locator alternatives

propose code patch (diff or AST edits)

produce rationale and confidence score



5. Validator — runs quick verification checks (verify candidate locators find target element, perform click, check expected result)


6. Patcher — applies code edits to pytest test (AST-aware preferred), opens PR or commit, or writes to branch.


7. Human approval loop (optional): show patch; allow accept/reject.


8. Monitoring & metrics — success rate, healing rate, false positives, time to heal.



Required MCP tools (Selenium MCP)

Add these endpoints/tools to your server.py:

capture_accessibility_tree() — uses CDP to return AX tree.

capture_html(locator?) — already exists; maybe add scope param for whole page.

run_pytest(test_path_or_nodeid, extra_args) — runs pytest and returns JSON report (use pytest --json-report or custom reporter).

collect_failure_context(pytest_json_report) — reads failing test ID, capture page context for that test.

generate_healing_candidates(context) — calls LLM with structured prompt and returns list of candidate patches/locator strategies.

validate_candidate(candidate) — execute small step(s) to verify candidate works.

apply_test_patch(patch, method='ast'|'regex') — apply the patch; generate PR/commit.

re_run_test_after_patch(nodeid) — re-run test to confirm.


Implementation details & code snippets

1) Capture accessibility (Chromium) — add to browser_manager / server:

# in server.py
@app.tool("capture_accessibility_tree")
def capture_accessibility_tree():
    driver = browser_manager.get_active_driver()
    try:
        ax = driver.execute_cdp_cmd("Accessibility.getFullAXTree", {})
        return {"tree": ax}
    except Exception as e:
        return {"error": str(e)}

2) Run pytest and return JSON report

Use pytest --maxfail=1 --json-report --json-report-file=report.json (requires pytest-json-report plugin) or parse JUnit/xUnit output.

Example run tool:

import subprocess, json, tempfile, os

@app.tool("run_pytest")
def run_pytest(nodeid: str = None, args: list[str] = None):
    args = args or []
    cmd = ["pytest", "--maxfail=1", "--capture=no", "--json-report", "--json-report-file=report.json"]
    if nodeid:
        cmd.append(nodeid)
    cmd += args
    proc = subprocess.run(cmd, cwd=PROJECT_ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out = proc.stdout
    report = {}
    try:
        with open(os.path.join(PROJECT_ROOT, "report.json")) as f:
            report = json.load(f)
    except Exception:
        report = {"error": "no json report", "stdout": out}
    return {"returncode": proc.returncode, "stdout": out, "report": report}

3) Failure context collector (called after run_pytest returns with failure)

Parse report to find nodeid, traceback, failing assertion.

In browser session: take screenshot (driver.save_screenshot()), get page.url, page.title, Accessibility.getFullAXTree, outerHTML for selectors referenced in test (if known; or capture largest clickable elements).


4) LLM prompt template (structured)

Feed LLM a JSON package (make it small):

short failing stack trace

failing assertion text

screenshot (optional, base64)

accessibility snippet (pruned to nodes near failure)

outerHTML snippet of the element under ref if test used ref or if found by name


Prompt example (shortened):

You are an automation assistant. Given:
- failing pytest node id: tests/test_login.py::test_login
- traceback: AssertionError: expected 'Welcome' in page
- accessibility snippet (json): {...}
- outerHTML snippet: "<button class='btn' id='login' ...>Login</button>"
Goal: produce a validated Selenium-compatible locator list (css, xpath, by role+text), and a minimal code patch to replace the failing locator in the test file.
Return JSON: { "candidates": [{ "locator": {"type":"css","value":"button#login"}, "confidence":0.9 }], "patch": { "file": "...", "diff": "...", "explanation": "..." } }

5) Validator (quick verification)

For each candidate locator:

driver.find_elements(By.CSS_SELECTOR, candidate) — if found and visible, try the action (click/fill) that test expects (wrapped in try/except and rollback).

If candidate completes expected assertion (or reaches expected page state), mark as validated.


6) Apply patch (safe)

Use lib2to3 / ast to perform AST-level edits where possible (e.g., change find_element(By.ID, 'x') to find_element(By.CSS_SELECTOR, 'y')).

If AST method is too heavy, use regex with strict anchors, or create a new helper locator at top of test file and refer. Create a git branch and make commit + create PR (optional).


Example patcher (regex):

def apply_patch(file_path, old_locator_pattern, new_locator_code):
    text = open(file_path).read()
    new_text = re.sub(old_locator_pattern, new_locator_code, text, count=1)
    open(file_path, "w").write(new_text)
    # commit ...

7) Re-run the single test to confirm. If success, record healing success metric, send PR/email.


---

Self-healing heuristics & locator generation rules

When LLM or heuristic suggests alternatives, prefer:

1. Accessibility-first: role + accessible name (e.g. role=button name="Login") — map to Selenium via getByRole equivalent or xpath using normalize-space() and @role.

Example XPath: //button[normalize-space(.)='Login' or @aria-label='Login']



2. Stable attributes: data-testid, data-qa, aria-*, id (if stable).


3. CSS fallback: use combinations like button.btn-primary[data-action='login'].


4. Contextual XPath: //form[.//input[@name='username']]//button[contains(.,'Login')]


5. Text plus position as last resort.



Confidence scoring:

Check uniqueness (how many elements matched).

Check visibility and enabled state.

Check whether element’s ancestor has stable attributes.



---

CI/CD & Workflow integration

Pre-commit/PR: any auto-patch should be opened as a PR with full details + failing run attached.

Nightly auto-heal: schedule a nightly run to auto-heal flaky tests; require human review for changes to core flows.

Metrics: create dashboard (Healing attempts / Success rate / Flaky tests per suite).

Audit log: every auto-patch must be recorded with before/after code and validation artifacts.



---

Security & governance

Authentication to MCP server (API tokens, IP allowlist).

Sandboxing: run tests in ephemeral containers or VMs.

No direct commits to main: create branches and PRs; require approvals.

Limit LLM abilities: LLM may generate nonsensical patches — require automated validation steps before applying.



---

Pros & Cons — condensed

Selenium MCP (build on your repo)

Pros:

Directly integrates with pytest and your existing codebase.

Easier to run, validate, patch Python tests.

Simple to implement run_pytest, collect_context, apply_patch.


Cons:

Accessibility snapshot requires CDP (Chromium only).

Need to add semantic summarization layer for LLM to reason well.


Playwright MCP (adopt Playwright)

Pros:

Semantic accessibility snapshot is native and richer.

Cross-browser snapshots and built-in tools for LLM-friendly context. Cons:

Not designed to run/test existing Selenium pytest code — you still need to call subprocesses or build glue.

Migration cost if you must move tests to Playwright.



---

Suggested implementation timeline & milestones

1. Week 1: Add run_pytest, capture_accessibility_tree, enhanced capture_html to Selenium MCP. Add JSON reporter to pytest.


2. Week 2: Implement collect_failure_context (screenshot + AX tree + outerHTML + trace).


3. Week 3: Build small LLM prompt + local mock LLM or rapid OpenAI call to generate candidate locators. Build validate_candidate.


4. Week 4: Implement apply_patch (AST approach) and re_run_test_after_patch. Integrate with git to open PRs.


5. Week 5: Add metrics, logging, human approval workflow, CI hooks.


6. Ongoing: Tune prompts, failure heuristics, fallback rules, broader cross-browser support.




---

Example: Minimal flow in your server.py to run & heal one failing test (skeleton)

# 1) run pytest
res = run_pytest(nodeid="tests/test_login.py::test_login")

if res["returncode"] != 0:
    # 2) collect context
    report = res["report"]
    nodeid = find_failing_node(report)
    screenshot = save_screenshot(driver)
    ax = driver.execute_cdp_cmd("Accessibility.getFullAXTree", {})
    html_snip = driver.execute_script("return document.documentElement.outerHTML;")[:20000]

    context = {
        "nodeid": nodeid,
        "traceback": get_trace(report, nodeid),
        "screenshot_b64": encode_image(screenshot),
        "ax": prune_ax_tree(ax),
        "html": html_snip
    }

    # 3) ask LLM for candidates
    candidates = llm_generate_locators(context)

    # 4) validate
    for c in candidates:
        if validate_locator(driver, c):
            # 5) apply patch
            patch = generate_patch_for_test_file(nodeid, c)
            apply_patch(patch)
            # 6) re-run single test
            r2 = run_pytest(nodeid=nodeid)
            if r2["returncode"] == 0:
                record_success(nodeid, c)
                break


---

Prompt engineering: example LLM prompt (concise)

Context:
- failing test nodeid: {nodeid}
- failing assertion: {assertion_line}
- accessibility snippet (JSON): {ax_snip}
- outerHTML snippet: {html_snip}
- screenshot: (base64 attached)

Task:
1) Propose 3 candidate Selenium locators (type + value + rationale + confidence).
2) Provide a minimal Python patch snippet to update the failing locator (show exact diff).
3) Return JSON: {candidates:[{type, value, reason, confidence}], patch: "diff text"}
Constraints: Prefer data-testid, ARIA, role+name, then stable classes or contextual XPaths. Keep replacements minimal.


---

Final notes, cautions & next steps

Start small: implement the run_pytest + capture_accessibility_tree + collect_failure_context + validator. Validate the whole feedback loop on a small flaky test set.

Human-in-loop first: auto-patch → PR approach reduces risk.

Hybrid architecture: strongly consider using Playwright accessibility snapshots as the context provider for the LLM even while executing and patching with Selenium. CDP accessibility gives parity with Playwright.

Edge cases: dynamically generated IDs, closed shadow roots, single-page apps with client routing — test carefully.



---

If you want, I can:

(A) Generate the code for run_pytest + capture_accessibility_tree + generate_candidate_locators (LLM prompt wrapper) and drop it into your server.py.

(B) Create an example AST-based patcher that edits a find_element call reliably.

(C) Draft the exact LLM prompt templates with few-shot examples for locator generation and patch diffs.


Which one should I produce next?
