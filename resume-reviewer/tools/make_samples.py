"""Development-only fixture generator; requires reportlab."""
from pathlib import Path
from reportlab.pdfgen import canvas
ROOT = Path(__file__).resolve().parents[1]
lines = (ROOT / 'samples/resume.txt').read_text().splitlines()
for name in ['simple','columns','two-pages']:
    c = canvas.Canvas(str(ROOT / 'samples' / f'resume-{name}.pdf'), pagesize=(612,792))
    c.setTitle('Fictional resume - '+name)
    if name == 'columns':
        c.setFont('Helvetica-Bold',18); c.drawString(40,740,'Alex Morgan | Fictional Resume')
        c.setFont('Helvetica',10)
        left = ['Education','B.S. Computer Science','Expected May 2027','Skills','Python, SQL, Git','communication']
        right = ['PROJECT EXPERIENCE','Built a Python script to clean survey data.',
                 'Used SQL queries to combine three tables.', 'Collaborated with classmates using Git.',
                 'Presented findings using communication skills.']
        for i,line in enumerate(left): c.drawString(40,690-i*24,line)
        for i,line in enumerate(right): c.drawString(230,690-i*24,line)
    else:
        c.setFont('Helvetica',11)
        import textwrap
        y=740
        for i,line in enumerate(lines):
            if name=='two-pages' and i==3:
                c.showPage(); c.setFont('Helvetica',11); y=740
            for part in textwrap.wrap(line,82): c.drawString(40,y,part); y-=20
            y-=10
    c.save()
