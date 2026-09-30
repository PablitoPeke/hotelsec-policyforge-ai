"""Create a private local Compose configuration without overwriting secrets."""
from pathlib import Path
import secrets
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=8085)
args = parser.parse_args()
if not 1024 <= args.port <= 65535:
    parser.error('Choose a port between 1024 and 65535.')
target = Path(__file__).resolve().parents[1] / '.env.local'
if target.exists():
    print('.env.local already exists; no changes made.')
else:
    with target.open('x', encoding='utf-8') as stream:
        stream.write(f'POSTGRES_PASSWORD={secrets.token_hex(32)}\nAPP_ENV=development\n'
                     f'APP_URL=http://localhost:{args.port}\nCORS_ORIGINS=http://localhost:{args.port}\n'
                     f'HTTP_PORT={args.port}\nCOOKIE_SECURE=false\nOPENAI_API_KEY=\n'
                     'OPENAI_MODEL=gpt-4o-mini\nAI_REQUESTS_PER_HOUR=20\n')
    print(f'Local configuration created. Open http://localhost:{args.port} after Compose starts.')
