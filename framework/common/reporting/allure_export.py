"""
Generate Allure HTML + exhaustive PDF/Excel summaries + a small HTML hub with download links.

Requires Allure CLI for HTML: https://docs.qameta.io/allure/#_installing_a_commandline
  npm install -g allure-commandline
  (or: scoop install allure)
"""

from __future__ import annotations

import json
import subprocess
import webbrowser
from html import escape
from pathlib import Path
from typing import Any

import pandas as pd
from fpdf import FPDF


def _safe_run(command: list[str], cwd: Path | None = None) -> int:
    try:
        return subprocess.call(command, cwd=cwd)
    except FileNotFoundError:
        print(f"[allure_export] Command not found (install Allure CLI): {' '.join(command)}")
        return 127


def _flatten_labels(labels: list[dict[str, Any]] | None) -> str:
    if not labels:
        return ""
    parts = []
    for lb in labels:
        parts.append(f"{lb.get('name', '')}={lb.get('value', '')}")
    return "; ".join(parts)


def parse_allure_results(results_dir: Path) -> list[dict[str, Any]]:
    """Parse *-result.json files into flat rows for Excel/PDF."""
    rows: list[dict[str, Any]] = []
    for file in sorted(results_dir.glob("*-result.json")):
        try:
            payload = json.loads(file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        start = payload.get("start")
        stop = payload.get("stop")
        duration_ms = ""
        if isinstance(start, int) and isinstance(stop, int) and stop >= start:
            duration_ms = str(stop - start)

        status_details = payload.get("statusDetails") or {}
        message = status_details.get("message") or ""
        trace = status_details.get("trace") or ""
        if len(trace) > 500:
            trace = trace[:500] + "…"

        attachments = payload.get("attachments") or []
        attach_count = len(attachments)

        rows.append(
            {
                "uuid": payload.get("uuid", ""),
                "name": payload.get("name", ""),
                "fullName": payload.get("fullName", ""),
                "status": payload.get("status", ""),
                "description": (payload.get("description") or "")[:500],
                "start": start,
                "stop": stop,
                "duration_ms": duration_ms,
                "message": str(message)[:1000],
                "trace_excerpt": trace,
                "labels": _flatten_labels(payload.get("labels")),
                "attachments_count": attach_count,
                "source_file": file.name,
            }
        )
    return rows


def _ascii(s: str) -> str:
    return (s or "").encode("ascii", "replace").decode("ascii")


def _write_pdf(rows: list[dict[str, Any]], pdf_path: Path, title: str) -> None:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, _ascii(title), ln=True)
    pdf.set_font("Helvetica", size=8)
    pdf.cell(0, 6, f"Rows: {len(rows)}", ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 7)
    headers = ["status", "name", "duration_ms", "uuid"]
    col_w = [22, 85, 25, 55]
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 6, h[:40], border=1)
    pdf.ln()

    pdf.set_font("Helvetica", size=6)
    for row in rows[:200]:
        vals = [
            _ascii(str(row.get("status", "")))[:20],
            _ascii(str(row.get("name", "")))[:80],
            _ascii(str(row.get("duration_ms", ""))),
            _ascii(str(row.get("uuid", "")))[:36],
        ]
        for i, v in enumerate(vals):
            pdf.cell(col_w[i], 5, v, border=1)
        pdf.ln()
    if len(rows) > 200:
        pdf.set_font("Helvetica", "I", 8)
        pdf.cell(0, 8, f"... {len(rows) - 200} more rows (see Excel for full data).", ln=True)

    pdf.output(str(pdf_path))


def _write_excel(rows: list[dict[str, Any]], excel_path: Path) -> None:
    if not rows:
        df = pd.DataFrame([{"info": "No *-result.json files found in allure-results"}])
    else:
        df = pd.DataFrame(rows)
    df.to_excel(excel_path, index=False, engine="openpyxl")


def _write_report_hub(session_root: Path, rel: dict[str, str]) -> None:
    """Single HTML page with links to Allure HTML, PDF, Excel, and media folders."""
    hub = session_root / "report_hub.html"
    lines = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Test report hub</title>",
        "<style>body{font-family:system-ui,sans-serif;margin:2rem;max-width:56rem}",
        "h1{font-size:1.25rem}a{display:block;margin:.5rem 0}</style></head><body>",
        f"<h1>Automation report — {escape(rel.get('folder', ''))}</h1>",
        "<p>Downloads and viewers for this session (same data in different formats).</p>",
        "<h2>Reports</h2>",
    ]
    for label, href in [
        ("Allure interactive HTML", rel.get("allure_html_index", "#")),
        ("Summary PDF", rel.get("pdf", "#")),
        ("Summary Excel", rel.get("excel", "#")),
    ]:
        lines.append(f"<a href=\"{escape(href)}\">{escape(label)}</a>")

    lines.append("<h2>Media</h2>")
    lines.append(f"<a href=\"{escape(rel.get('screenshots', ''))}\">Screenshots folder</a>")
    lines.append(f"<a href=\"{escape(rel.get('videos', ''))}\">Videos folder (Playwright)</a>")
    lines.append("<p><small>Open this file via a local static server if browser blocks file:// links to subfolders; "
                   "Allure HTML is best opened via <code>allure open</code> or from the generated <code>allure-html</code> folder.</small></p>")
    lines.append("</body></html>")
    hub.write_text("\n".join(lines), encoding="utf-8")


def export_allure_artifacts(
    reports_root: Path,
    session_root: Path | None = None,
    open_browser: bool = False,
) -> Path | None:
    """
    Generate Allure HTML report + PDF + Excel + report_hub.html.

    :param reports_root: Usually ``framework/common/reports`` (used to resolve latest session).
    :param session_root: Explicit session folder (``.../sessions/<id>_<stamp>/``). If None, uses
                         ``sessions/LATEST_SESSION.txt`` or legacy ``allure-results`` under reports_root.
    :returns: Path to session root that was exported, or None.
    """
    framework_root = reports_root.parent.parent if reports_root.name == "reports" else reports_root

    if session_root is None:
        from common.reporting.allure_session import read_latest_session_root

        session_root = read_latest_session_root(framework_root)

    legacy_results = reports_root / "allure-results"
    legacy_html = reports_root / "allure-html"

    if session_root and (session_root / "allure-results").is_dir():
        results_dir = session_root / "allure-results"
        html_dir = session_root / "allure-html"
        out_pdf = session_root / "allure_summary.pdf"
        out_xlsx = session_root / "allure_summary.xlsx"
        folder_name = session_root.name
    else:
        # Legacy flat layout under common/reports/
        results_dir = legacy_results
        session_root = reports_root
        html_dir = legacy_html
        out_pdf = reports_root / "allure-summary.pdf"
        out_xlsx = reports_root / "allure-summary.xlsx"
        folder_name = "default"

    results_dir.mkdir(parents=True, exist_ok=True)
    html_dir.parent.mkdir(parents=True, exist_ok=True)

    rc = _safe_run(["allure", "generate", str(results_dir), "-o", str(html_dir), "--clean"], cwd=reports_root)
    if rc != 0:
        print(
            "[allure_export] Skipped or failed Allure HTML generation. "
            "Install CLI: npm i -g allure-commandline"
        )

    rows = parse_allure_results(results_dir)
    _write_excel(rows, out_xlsx)
    try:
        _write_pdf(rows, out_pdf, f"Allure summary - {folder_name}")
    except Exception as exc:
        print(f"[allure_export] PDF skipped: {exc}")

    rel = {
        "folder": folder_name,
        "allure_html_index": "allure-html/index.html",
        "pdf": out_pdf.name,
        "excel": out_xlsx.name,
        "screenshots": "media/screenshots/",
        "videos": "media/videos/",
    }
    _write_report_hub(session_root, rel)

    print(f"[allure_export] Session: {session_root}")
    print(f"[allure_export] Allure HTML: {html_dir / 'index.html'}")
    print(f"[allure_export] PDF: {out_pdf}")
    print(f"[allure_export] Excel: {out_xlsx}")
    print(f"[allure_export] Hub: {session_root / 'report_hub.html'}")

    index_html = html_dir / "index.html"
    if open_browser and index_html.is_file():
        webbrowser.open(index_html.as_uri())

    return session_root
