#!/usr/bin/env python3
"""
export_monte_carlo_pdf_docx.py
Exports the Monte Carlo methodology document to high-quality PDF and Word (.docx).
"""

import os
import subprocess
import shutil

DOC_MD = "/home/thr/Documents/time-and-consciousness/docs/2026-09-03-monte-carlo-methodology-in-active-inference-and-consciousness-en.md"
VAULT_MD = "/home/thr/Documents/ThRNotes/03-professional/braindumps/2026-09-03-monte-carlo-methodology-in-active-inference-and-consciousness-en.md"

DOCX_OUT = "/home/thr/Documents/time-and-consciousness/docs/Monte_Carlo_Methodology_Active_Inference_Thomas_Riebl.docx"
DOCX_MAIN = "/home/thr/Documents/Monte_Carlo_Methodology_Active_Inference_Thomas_Riebl.docx"

PDF_OUT = "/home/thr/Documents/time-and-consciousness/docs/Monte_Carlo_Methodology_Active_Inference_Thomas_Riebl.pdf"
PDF_MAIN = "/home/thr/Documents/Monte_Carlo_Methodology_Active_Inference_Thomas_Riebl.pdf"
PDF_VAULT = "/home/thr/Documents/ThRNotes/Alle_Braindumps_PDF/2026-09-03-monte-carlo-methodology-in-active-inference-and-consciousness-en.pdf"

def main():
    print("=== Exporting Monte Carlo Methodology Document ===")
    
    # Copy to Vault
    shutil.copy(DOC_MD, VAULT_MD)
    print(f"✓ Copied Markdown to Vault: {VAULT_MD}")
    
    # 1. Generate DOCX via pandoc
    print("Generating Word (.docx)...")
    cmd_docx = [
        "pandoc",
        DOC_MD,
        "-o", DOCX_MAIN,
        "--from=markdown+tex_math_dollars+yaml_metadata_block",
        "--table-of-contents",
        "--toc-depth=2"
    ]
    subprocess.run(cmd_docx, check=False)
    if os.path.exists(DOCX_MAIN):
        shutil.copy(DOCX_MAIN, DOCX_OUT)
        print(f"✓ Created DOCX: {DOCX_MAIN} and {DOCX_OUT}")
        
    # 2. Generate HTML with MathJax and print to PDF via Chromium
    print("Rendering high-quality PDF via Headless Chrome...")
    html_temp = "/home/thr/Documents/time-and-consciousness/docs/temp_mc_render.html"
    
    cmd_html = [
        "pandoc",
        DOC_MD,
        "-o", html_temp,
        "--from=markdown+tex_math_dollars+yaml_metadata_block",
        "--standalone",
        "--mathjax=https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
    ]
    subprocess.run(cmd_html, check=True)
    
    with open(html_temp, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # Custom CSS injection for scientific typography
    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
        
        @page {
            size: A4;
            margin: 20mm 18mm 20mm 18mm;
            @bottom-right {
                content: counter(page);
                font-family: 'Inter', sans-serif;
                font-size: 8pt;
                color: #64748b;
            }
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 9.8pt;
            line-height: 1.6;
            color: #1e293b;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
        }
        
        h1 {
            font-size: 19pt;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.25;
            margin-top: 0;
            margin-bottom: 6px;
            border-bottom: 2.5px solid #3b82f6;
            padding-bottom: 6px;
        }
        
        h2 {
            font-size: 13.5pt;
            font-weight: 700;
            color: #1e3a8a;
            margin-top: 22px;
            margin-bottom: 8px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 4px;
        }
        
        h3 {
            font-size: 11pt;
            font-weight: 600;
            color: #0369a1;
            margin-top: 14px;
            margin-bottom: 6px;
        }
        
        p {
            margin-top: 0;
            margin-bottom: 8px;
            text-align: justify;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 14px 0;
            font-size: 8.8pt;
        }
        
        th, td {
            padding: 7px 10px;
            border: 1px solid #cbd5e1;
            text-align: left;
        }
        
        th {
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
        }
        
        tr:nth-child(even) {
            background-color: #f8fafc;
        }
        
        blockquote {
            margin: 12px 0;
            padding: 10px 14px;
            background-color: #f0fdf4;
            border-left: 4px solid #16a34a;
            color: #166534;
            font-size: 9.3pt;
            border-radius: 0 6px 6px 0;
        }
        
        code {
            font-family: 'JetBrains Mono', monospace;
            font-size: 8.5pt;
            background-color: #f1f5f9;
            padding: 2px 4px;
            border-radius: 4px;
            color: #0f172a;
        }
        
        pre {
            background-color: #0f172a;
            color: #f8fafc;
            padding: 12px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 8.5pt;
            overflow-x: auto;
        }
        
        hr {
            border: none;
            border-top: 1px solid #e2e8f0;
            margin: 18px 0;
        }
        
        .math.display {
            overflow-x: auto;
            margin: 10px 0;
            text-align: center;
        }
    </style>
    """
    
    html_content = html_content.replace("</head>", custom_css + "\n</head>")
    
    with open(html_temp, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    cmd_pdf = [
        "google-chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={PDF_MAIN}",
        html_temp
    ]
    subprocess.run(cmd_pdf, check=True)
    
    if os.path.exists(PDF_MAIN):
        shutil.copy(PDF_MAIN, PDF_OUT)
        shutil.copy(PDF_MAIN, PDF_VAULT)
        print(f"✓ SUCCESS! Exported PDF to:\n  - {PDF_MAIN}\n  - {PDF_OUT}\n  - {PDF_VAULT}")
        
    if os.path.exists(html_temp):
        os.remove(html_temp)

if __name__ == "__main__":
    main()
