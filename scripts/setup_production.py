"""Generate private production configuration, without replacing existing secrets."""
import argparse
import ipaddress
import os
from pathlib import Path
import re
import secrets


def validate_domain(value: str) -> str:
    domain = value.strip().lower().rstrip('.')
    if len(domain) > 253 or '.' not in domain:
        raise ValueError('Use a full DNS name, without protocol, port or path.')
    try:
        ipaddress.ip_address(domain)
    except ValueError:
        pass
    else:
        raise ValueError('Use a domain with DNS configured, not an IP address.')
    if domain.endswith(('.example', '.test', '.invalid', '.localhost')) or domain in {
        'example.com', 'example.org', 'example.net',
    } or any(domain.endswith('.' + suffix) for suffix in ('example.com', 'example.org', 'example.net')):
        raise ValueError('Replace the example domain with your own DNS name.')
    if any(not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', label) for label in domain.split('.')):
        raise ValueError('Use an ASCII DNS name (punycode for international domains).')
    return domain


def create_configuration(domain: str, target: Path) -> bool:
    domain = validate_domain(domain)
    # Exclusive creation also rejects existing symlinks and never rotates a live DB password.
    try:
        descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        return False
    with os.fdopen(descriptor, 'w', encoding='utf-8', newline='\n') as stream:
        stream.write(f'DOMAIN={domain}\nPOSTGRES_PASSWORD={secrets.token_hex(32)}\n'
                     'OPENAI_API_KEY=\nOPENAI_MODEL=gpt-4o-mini\nAI_REQUESTS_PER_HOUR=20\nAI_GLOBAL_DAILY_LIMIT=50\n')
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--domain', required=True, help='DNS name already pointing at the server')
    args = parser.parse_args()
    target = Path(__file__).resolve().parents[1] / '.env.production'
    try:
        created = create_configuration(args.domain, target)
    except (OSError, ValueError) as error:
        parser.exit(1, f'Configuration not created: {type(error).__name__}. Check domain and permissions.\n')
    if not created:
        print('.env.production already exists; no changes made.')
        return
    print('Private .env.production created. No API key was added. No services were started.')
    if os.name == 'nt':
        print('Windows: review inherited file permissions. Linux uses owner-only mode 600.')


if __name__ == '__main__':
    main()
