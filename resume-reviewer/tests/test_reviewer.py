import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch
from pypdf import PdfWriter
from reviewer import analyze, extract_pdf, validate_result, ReviewError, local_model

ROOT = Path(__file__).resolve().parents[1]
RESUME = (ROOT / 'samples/resume.txt').read_text()
JOB = (ROOT / 'samples/job.txt').read_text()

class ReviewTests(unittest.TestCase):
    def test_known_matches_and_gaps(self):
        report = analyze(RESUME, JOB, 'demo')
        status = {r['requirement']: r['status'] for r in report['qualifications']}
        self.assertEqual(status, {'Python':'matched','SQL':'matched','Git':'matched',
                                 'AWS':'missing_evidence','Tableau':'missing_evidence','communication':'matched'})

    def test_negation_not_a_match(self):
        report = analyze('Student with no Python experience. Studied literature and writing.', JOB, 'demo')
        self.assertTrue(all(r['status'] == 'missing_evidence' for r in report['qualifications']))

    def test_word_boundaries(self):
        report = analyze('A student used JavaScript for a classroom web application.', 'Required: Java programming for backend software development.', 'demo')
        self.assertEqual(report['counts']['matched'], 0)

    def test_empty_and_oversize(self):
        for resume, job in [('', JOB), (RESUME, ''), ('x'*16001, JOB)]:
            with self.assertRaises(ReviewError): analyze(resume, job, 'demo')

    def test_invalid_pdf(self):
        for data in [b'', b'not a pdf', b'%PDF-broken']:
            with self.assertRaises(ReviewError): extract_pdf(data)

    def test_blank_and_encrypted_pdf(self):
        for encrypted in [False, True]:
            writer = PdfWriter(); writer.add_blank_page(612, 792)
            if encrypted: writer.encrypt('secret')
            stream = io.BytesIO(); writer.write(stream)
            with self.assertRaises(ReviewError): extract_pdf(stream.getvalue())

    def test_sample_layouts(self):
        for name in ['resume-simple.pdf', 'resume-columns.pdf', 'resume-two-pages.pdf']:
            text = extract_pdf((ROOT / 'samples' / name).read_bytes())
            for token in ['Python', 'SQL', 'Git', 'communication']:
                self.assertIn(token, text)

    def test_fabricated_evidence_downgraded(self):
        raw = {'qualifications':[{'requirement':'Python','job_quote':'Python','resume_quote':'Invented evidence',
            'status':'matched','suggestion':'Invented advice'}]}
        result = validate_result(raw, RESUME, JOB)
        self.assertEqual(result['qualifications'][0]['status'], 'uncertain')
        self.assertTrue(result['warnings'])

    def test_fabricated_job_rejected(self):
        raw = {'qualifications':[{'requirement':'pilot','job_quote':'Pilot license','resume_quote':'',
            'status':'missing_evidence','suggestion':'Get a license'}]}
        with self.assertRaises(ReviewError): validate_result(raw, RESUME, JOB)

    def test_malformed_model_output(self):
        for raw in [None, {}, {'qualifications':[]}, {'qualifications':[{}]}]:
            with self.assertRaises(ReviewError): validate_result(raw, RESUME, JOB)

    def test_missing_evidence_advice_conditional(self):
        result = analyze(RESUME, JOB, 'demo')
        for row in result['qualifications']:
            if row['status']=='missing_evidence': self.assertTrue(row['suggestion'].startswith('If you have'))

    def test_model_failure_explained(self):
        with patch('urllib.request.urlopen', side_effect=TimeoutError()):
            with self.assertRaisesRegex(ReviewError, 'Local AI unavailable'): local_model(RESUME, JOB)

if __name__ == '__main__': unittest.main()
