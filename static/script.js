
const codeInput = document.getElementById("codeInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const fixBtn = document.getElementById("fixBtn");
const statusText = document.getElementById("status");
const summary = document.getElementById("summary");
const issuesContainer = document.getElementById("issues");
const fixedSection = document.getElementById("fixedSection");
const diffContainer = document.getElementById("diffContainer");
const useFixedBtn = document.getElementById("useFixedBtn");

let latestFixedCode = "";

function setBusy(busy) {
    analyzeBtn.disabled = busy;
    fixBtn.disabled = busy;
}

function showMessage(title, message) {
    summary.replaceChildren();

    const heading = document.createElement("h2");
    heading.textContent = title;

    const paragraph = document.createElement("p");
    paragraph.textContent = message;

    summary.append(heading, paragraph);
}



function renderDiff(rows) {
    diffContainer.replaceChildren();


    for (const row of rows) {
        const line = document.createElement("div");
        line.className = `diff-row diff-${row.type}`;

        const original = document.createElement("div");
        original.className = "diff-cell";

        const corrected = document.createElement("div");
        corrected.className = "diff-cell";

        const oldCode = document.createElement("code");
        const newCode = document.createElement("code");

        if (row.type === "removed") {
            oldCode.textContent = `− ${row.original}`;
            newCode.textContent = " ";
            original.classList.add("diff-cell-removed");
        } else if (row.type === "added") {
            oldCode.textContent = " ";
            newCode.textContent = `+ ${row.fixed}`;
            corrected.classList.add("diff-cell-added");
        } else if (row.type === "changed") {
            oldCode.textContent = `− ${row.original}`;
            newCode.textContent = `+ ${row.fixed}`;
            original.classList.add("diff-cell-removed");
            corrected.classList.add("diff-cell-added");
        } else {
            oldCode.textContent = row.original || " ";
            newCode.textContent = row.fixed || " ";
        }

        original.append(oldCode);
        corrected.append(newCode);
        line.append(original, corrected);
        diffContainer.append(line);
    }

    if (rows.length === 0) {
        const message = document.createElement("p");
        message.textContent = "No line changes were needed.";
        diffContainer.append(message);
    }
}



function showIssues(issues) {
    issuesContainer.replaceChildren();

    if (!issues || issues.length === 0) {
        const paragraph = document.createElement("p");
        paragraph.textContent = "No code-quality issues found.";
        issuesContainer.append(paragraph);
        return;
    }

    for (const issue of issues) {
        const card = document.createElement("div");
        card.className = "issue";

        const title = document.createElement("strong");
        title.textContent = `${issue.code} · Line ${issue.line}`;

        const description = document.createElement("p");
        description.textContent = issue.message;

        card.append(title, description);
        issuesContainer.append(card);
    }
}

analyzeBtn.addEventListener("click", async () => {
    setBusy(true);
    statusText.textContent = "Analyzing your code...";
    fixedSection.hidden = true;
    issuesContainer.replaceChildren();

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code: codeInput.value })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Analysis failed.");
        }

        if (!data.syntax.valid) {
            showMessage(
                "Syntax error detected",
                `${data.syntax.message} (line ${data.syntax.line ?? "unknown"})`
            );
            statusText.textContent = "Fix syntax errors before continuing.";
            return;
        }

        showMessage("Syntax check passed", data.quality.message);
        showIssues(data.quality.issues);
        statusText.textContent = "Analysis complete.";
    } catch (error) {
        statusText.textContent = error.message || "Could not connect to the server.";
    } finally {
        setBusy(false);
    }
});

fixBtn.addEventListener("click", async () => {
    setBusy(true);
    statusText.textContent = "Applying safe automatic fixes...";
    fixedSection.hidden = true;

    try {
        const response = await fetch("/api/fix", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code: codeInput.value })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Auto-fix failed.");
        }

        
        latestFixedCode = data.fixed_code;

        if (Array.isArray(data.diff_rows)) {
            renderDiff(data.diff_rows);
        } else {
            renderDiff([]);
        }

        fixedSection.hidden = false;
    
        const hasChanges = Array.isArray(data.diff_rows)
            && data.diff_rows.some(row => row.type !== "same");

        statusText.textContent = hasChanges
            ? "Automatic fixes applied. Review the highlighted changes below."
            : "No further automatic fixes available. Review the remaining issues below.";
    } catch (error) {
        statusText.textContent = error.message || "Could not connect to the server.";
    } finally {
        setBusy(false);
    }
});

useFixedBtn.addEventListener("click", () => {
    codeInput.value = latestFixedCode;
    statusText.textContent =
        "Corrected code loaded into the editor. Analyze it again to review.";
});
