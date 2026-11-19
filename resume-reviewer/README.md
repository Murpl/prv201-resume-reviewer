# Resume Review - PRV 201 M3

A local Python pipeline that compares a PDF resume with a pasted job description and returns matching qualifications, missing evidence, and revision suggestions. Group: Ryan Kropac, Vincent Wang, Emiliano Gutierrez.

On the computer where this project was created, `start-on-this-computer.bat` uses the already available Codex Python runtime, so no Python package installation is needed. If the app is already running, open http://127.0.0.1:8765 instead. That convenience launcher is machine-specific; other computers should use the portable setup below.

## Free setup (Windows)

Requires Python 3.10+ and [Ollama](https://ollama.com/download). No paid API, account, subscription, or hosted deployment is needed. Model inference uses your computer's memory and CPU/GPU. The first download needs internet; subsequent local reviews can run offline.

Open a terminal in this folder:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
ollama pull qwen2.5:3b
.venv\Scripts\python app.py
```

Open http://127.0.0.1:8765 in your browser. Keep Ollama running (start its app, or run `ollama serve` in another terminal). After setup, `start.bat` starts the Python app. To stop it, press Ctrl+C.

On macOS/Linux use `.venv/bin/python` instead of `.venv\Scripts\python`.

## Three-minute demonstration

1. Select **Load fictional example**, or upload `samples/resume-simple.pdf` and paste `samples/job.txt`.
2. Check the extracted resume text. Try the column and two-page PDFs as well.
3. Select **Local AI**, leave the model as `qwen2.5:3b`, and click **Review my resume**.
4. Explain the quoted job and resume evidence. The fixture has Python, SQL, Git, and communication evidence; Tableau and AWS are not documented.
5. Download the JSON report. Missing evidence does not imply the applicant lacks a skill.
6. Try an empty input or a non-readable PDF to demonstrate error handling.

If Ollama is unavailable, **Offline demo** exercises the interface and pipeline using a limited keyword baseline. It is explicitly not AI and does not validate LLM quality. The app never silently falls back to this mode.

## Verification

```powershell
.venv\Scripts\python -m unittest discover -s tests -v
.venv\Scripts\python tools/run_evaluation.py
.venv\Scripts\python tools/run_evaluation.py --local
```

Execution traces and screenshots are in `evidence/`. The local evaluator overwrites only its named trace. Use fictional or anonymized inputs for saved reports. The app processes inputs in memory and does not persist uploads; exported reviews include quotations and should be treated as personal documents.

## Repository map

- `app.py`: loopback web server and input endpoints.
- `reviewer.py`: PDF extraction, prompts, Ollama adapter, output validation, demo baseline.
- `index.html`: responsive upload/review interface with extraction preview and download.
- `samples/`: fictional resume, posting, and three PDF layouts.
- `tests/`: input, parsing, grounding, model-failure and lexical regression tests.
- `tools/run_evaluation.py`: reproducible pipeline execution.
- `docs/M3-design.md` and `docs/M3-design.pdf`: design, evidence, rubric mapping, limitations.
- `docs/manual-evaluation.md`: worksheet for human review of M2 targets.

The app's only Python runtime dependency is pypdf. Fixture and document generation additionally require ReportLab; browser verification requires Playwright and Edge. These development tools are not needed to use the app.

## Limits and troubleshooting

- Text-based PDFs only, at most 5 MB / 10 pages. Each input is limited to 16,000 characters. OCR and full resume rewriting are outside M2 scope.
- An unavailable model produces a clear error. Verify the name with `ollama list`, or pull it again.
- Inference has a 180-second timeout. The M2 30-second target depends on hardware and is evaluated separately.
- Quotation checks verify text presence, not the truth or relevance of a claim. Small local models can overlook qualifications or give weak advice. Always review output.
- This loopback-only server is a course prototype, not a production multi-user service. Do not expose it publicly.
- If port 8765 is in use, stop the other instance first.

## Technical sources

- [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs): JSON-schema-constrained responses.
- [Ollama generate API](https://docs.ollama.com/api/generate): local generation endpoint.
- [Qwen 2.5 model library](https://ollama.com/library/qwen2.5): local model options.
- [pypdf text extraction](https://pypdf.readthedocs.io/en/stable/user/extract-text.html): extraction behavior and limitations.

See the design document for how the M2 proposal maps to M3. No human evaluation scores or group contributions are fabricated.
