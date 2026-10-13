"""Create review sheets from rendered pages and check text stays within margins."""
from pathlib import Path
import argparse
import json
from PIL import Image, ImageDraw
import pdfplumber

parser = argparse.ArgumentParser()
parser.add_argument('pdf')
parser.add_argument('--prefix', default='memory')
parser.add_argument('--report', type=Path, help='Optional structured margin evidence')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
temporary = root / 'tmp/pdfs'
pages = sorted(temporary.glob(f'{args.prefix}-[0-9]*.png'))
for start in range(0, len(pages), 12):
    sheet = Image.new('RGB', (1100, 1270), '#d7dfe2')
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(pages[start:start + 12]):
        img = Image.open(path).convert('RGB')
        img.thumbnail((250, 365))
        x, y = 20 + (index % 4) * 275, 20 + (index // 4) * 420
        sheet.paste(img, (x, y + 20))
        draw.text((x, y), path.stem, fill='black')
    sheet.save(temporary / f'{args.prefix}-review-{start // 12 + 1}.png')
issues = []
with pdfplumber.open(root / args.pdf) as document:
    for number, page in enumerate(document.pages, 1):
        for char in page.chars:
            if char['text'].strip() and (char['x0'] < 35 or char['x1'] > page.width - 35 or char['top'] < 25 or char['bottom'] > page.height - 20):
                issues.append((number, char['text']))
print(f'{len(pages)} rendered pages; margin issues: {len(issues)}')
if args.report:
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps({'pdf': args.pdf, 'rendered_pages': len(pages),
        'margin_issues': len(issues), 'passed': not issues,
        'limits': 'Geometric character margins only; not proof of no overlap or screenshot legibility. Visual review remains necessary.'}, indent=2), encoding='utf-8')
if issues:
    print(issues[:20])
    raise SystemExit(1)
