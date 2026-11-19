# Human evaluation worksheet

This is an uncompleted worksheet, not a claim that human testing has occurred.

For each resume/posting pair, have a reviewer label requirements before inspecting model output. Use at least 10 distinct fictional resumes across multiple roles and layouts, including non-matches, partial qualifications, negation, certifications, degrees and years of experience. Layout variants of one resume are not independent semantic examples.

Record: case ID; model and version; PDF readable (yes/no); expected requirement; expected status; predicted status; omitted or extra requirement; quotation relevance; suggestion supported (yes/no); suggestion relevant (yes/no); pipeline seconds; reviewer and date; comments.

## Initial fixture labels (authored test expectations)

| Requirement | Expected status | Supporting resume evidence |
|---|---|---|
| Python | matched | Built a Python script to clean survey data |
| SQL | matched | Used SQL queries to combine three tables |
| Git | matched | Collaborated using Git for version control |
| communication | matched | Presented findings to classmates |
| Tableau | missing_evidence | Not documented |
| AWS | missing_evidence | Not documented |

## Calculations

- PDF success = readable supported PDFs / attempted supported PDFs. Target: at least 90%. Report rejected scans separately.
- Qualification accuracy = correct expected requirement statuses / all expected requirements. Count omissions and uncertain predictions as incorrect when the label is definite. Also report extra requirements and their validity. Target: at least 80%.
- Recommendation accuracy = suggestions judged both relevant and evidence-supported / all displayed suggestions. Target: at least 90%. Quote presence alone is not sufficient.
- Latency: measure from extraction start through final validated analysis. Report cold start, median, maximum and sample count. Target: typical review under 30 seconds.

Do not fill human reviewer fields with automated judgments. Preserve unsuccessful runs and describe fixes.
