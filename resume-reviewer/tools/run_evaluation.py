"""Record actual pipeline execution; --local enables Ollama."""
import argparse
import json
import re
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from reviewer import analyze, extract_pdf
parser=argparse.ArgumentParser(); parser.add_argument('--local',action='store_true'); parser.add_argument('--model',default='qwen2.5:3b'); args=parser.parse_args()
mode='local' if args.local else 'demo'
job=(ROOT/'samples/job.txt').read_text()
expected={'Python':'matched','SQL':'matched','Git':'matched','communication':'matched','Tableau':'missing_evidence','AWS':'missing_evidence'}
evidence=ROOT/'evidence'; evidence.mkdir(exist_ok=True)
parsing=[]
for filename in ['resume-simple.pdf','resume-columns.pdf','resume-two-pages.pdf']:
    text=extract_pdf((ROOT/'samples'/filename).read_bytes())
    parsing.append({'file':filename,'all_expected_skills_extracted':all(s in text for s in ['Python','SQL','Git','communication'])})
start=time.perf_counter()
resume=extract_pdf((ROOT/'samples/resume-simple.pdf').read_bytes())
report=analyze(resume,job,mode,model=args.model)
report['pipeline_seconds']=round(time.perf_counter()-start,3)
report['fixture']='samples/resume-simple.pdf + samples/job.txt'
report['expected_qualification_labels']=expected
comparison=[]
for skill, expected_status in expected.items():
    hits=[row for row in report['qualifications'] if re.search(r'\b'+re.escape(skill)+r'\b', row['job_quote'], re.I)]
    predicted=hits[0]['status'] if len(hits)==1 else 'omitted_or_duplicate'
    comparison.append({'skill':skill,'expected':expected_status,'predicted':predicted,'correct':predicted==expected_status})
report['fixture_comparison']=comparison
report['fixture_correct']=sum(row['correct'] for row in comparison)
report['fixture_total']=len(comparison)
report['pdf_extraction_cases']=parsing
report['evaluation_note']='Synthetic smoke test only. Human review of semantic correctness and recommendation relevance is required; these results do not establish M2 accuracy targets.'
(evidence/f'{mode}-trace.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
