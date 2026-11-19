"""Build the one-page M3 submission document."""
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

ROOT = Path(__file__).resolve().parents[1]
sections = [
('What was built', 'A working resume reviewer that accepts a text-based PDF resume and a pasted job description. It identifies matching qualifications, missing evidence and uncertain matches, then provides revision suggestions with supporting quotations. Users can preview extracted text and download the review as JSON. Missing evidence does not mean the applicant lacks a skill.'),
('Architecture and M2 alignment', 'The pipeline follows M2: PDF upload -> pypdf text extraction -> local LLM analysis -> evidence validation -> feedback in a Python web interface. It uses Ollama with Qwen 2.5 3B, requiring no paid API or subscription. A local model replaces a hosted API to keep costs at zero. Suggestions use verified-evidence templates to reduce unsupported claims. A separate offline keyword demo is labeled as non-AI. Scanned PDFs and full resume rewriting remain outside scope.'),
('Engineering and safeguards', 'The code separates the web server (app.py), analysis pipeline (reviewer.py) and interface (index.html). It handles empty inputs, unreadable or encrypted PDFs, oversized files, invalid model responses and model timeouts. PDFs are limited to 5 MB and 10 pages. Quotations are checked against the supplied documents; unsupported matches are marked uncertain. Documents are processed locally and uploads are not saved by the app.'),
('Execution evidence and results', 'All 12 automated tests passed, including extraction across three PDF layouts, input validation and fabricated-evidence handling. Browser checks passed for PDF upload, AI review, mobile layout and error messages. The recorded model test correctly classified 5 of 6 qualifications (83.3%), missing Python evidence, and took 35.016 seconds. This exceeded the M2 30-second target. The small synthetic sample does not establish general accuracy; the 90% recommendation-quality target still requires human evaluation.'),
('How to run and inspect', 'Follow README.md to install the Python requirements and Ollama model, then run python app.py and open http://127.0.0.1:8765. Load the fictional example, select Local AI and click Review my resume. On the original computer, start-on-this-computer.bat uses the available Python runtime. Inspect evidence/local-trace.json, test-results.txt and the browser screenshots for execution evidence. Full setup and test commands are in README.md.'),
('Rubric coverage and next steps', 'M3.1-M3.2: working pipeline and planned components. M3.3: runnable source, saved traces and screenshots. M3.4: modular code, validation and tests. M3.5: M2 architecture retained, with changes explained above. M3.6: this summary and README run instructions. Next steps are broader labeled testing, human review of suggestions and improved model accuracy and speed.'),
]
docs = ROOT / 'docs'
title = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=21, leading=25, textColor=colors.HexColor('#183d37'), spaceAfter=7)
meta = ParagraphStyle('Meta', fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor('#57675c'), spaceAfter=9)
heading = ParagraphStyle('Heading', fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=colors.HexColor('#176448'), spaceBefore=8, spaceAfter=4)
body = ParagraphStyle('Body', fontName='Helvetica', fontSize=10, leading=13, spaceAfter=3)
story = [Paragraph('AI-Powered Resume Reviewer', title), Paragraph('PRV 201 | M3 Prototype / Draft | Track A<br/>Ryan Kropac, Vincent Wang, Emiliano Gutierrez', meta)]
markdown = ['# AI-Powered Resume Reviewer\n', 'PRV 201 | M3 Prototype / Draft | Track A\n\nRyan Kropac, Vincent Wang, Emiliano Gutierrez\n']
for label, text in sections:
    story.extend([Paragraph(escape(label), heading), Paragraph(escape(text), body)])
    markdown.extend(['## ' + label + '\n', text + '\n'])
story.extend([Spacer(1, 8), Paragraph('Prepared with AI assistance. Technical references and detailed evaluation materials are included in the repository.', meta)])
def footer(canvas, doc):
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor('#57675c'))
    canvas.drawString(44, 26, 'PRV 201 | M3 Design Summary')
    canvas.drawRightString(568, 26, str(doc.page))
SimpleDocTemplate(str(docs / 'M3-design.pdf'), pagesize=(612, 792), leftMargin=44, rightMargin=44, topMargin=35, bottomMargin=40).build(story, onFirstPage=footer, onLaterPages=footer)
(docs / 'M3-design.md').write_text('\n'.join(markdown), encoding='utf-8')
print('Built concise design PDF and Markdown.')
