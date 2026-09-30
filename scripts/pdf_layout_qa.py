"""Create review sheets from rendered pages and check text stays within margins."""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw
import pdfplumber

parser = argparse.ArgumentParser()
parser.add_argument('pdf')
parser.add_argument('--prefix', default='memory')
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
if issues:
    print(issues[:20])
    raise SystemExit(1)
