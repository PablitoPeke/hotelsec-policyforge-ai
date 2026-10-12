"""Check your deployment using two temporary fictional accounts, deleted afterwards."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import secrets
from urllib.parse import urlsplit

import httpx


class CheckFailure(Exception):
    pass


def validate_origin(value: str) -> str:
    parsed = urlsplit(value)
    if parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in ('', '/'):
        raise ValueError('Use only the origin, without credentials, path or query.')
    if not parsed.hostname or parsed.scheme not in ('http', 'https'):
        raise ValueError('Use an HTTP(S) origin.')
    if parsed.scheme == 'http' and parsed.hostname not in ('localhost', '127.0.0.1', '::1'):
        raise ValueError('Remote checks require HTTPS; credentials must not travel over HTTP.')
    _ = parsed.port
    return value.rstrip('/')


def expect(response, status, stage):
    if response.status_code != status:
        raise CheckFailure(f'{stage}: HTTP {response.status_code}, expected {status}')
    return response


def sample_assessment():
    return {
        'hotel_profile': {
            'business_name': 'Hotel Demo Verificacion', 'municipality': 'Tias',
            'business_type': 'hotel', 'rooms_count': 20, 'permanent_employees': 5,
            'temporary_employees': 2, 'has_external_it_provider': True, 'uses_pms': True,
            'offers_guest_wifi': True, 'handles_card_payments': True, 'stores_guest_documents': False,
        },
        'security_controls': {
            'uses_mfa': False, 'uses_password_manager': True, 'shared_accounts': False,
            'pms_individual_users': True, 'employee_offboarding_process': False,
            'backup_frequency': 'none', 'backups_tested': False, 'has_antivirus': True,
            'systems_updated': False, 'guest_wifi_separated': False,
            'payment_terminal_isolated': False, 'cctv_or_iot_devices': True,
            'iot_network_separated': False, 'supplier_remote_access': True,
            'supplier_access_controlled': False, 'has_incident_response_plan': False,
            'has_rgpd_breach_protocol': False, 'rgpd_processing_register': False,
            'staff_phishing_training': False,
        },
    }


def verify(primary, secondary, origin: str, with_ai: bool = False) -> dict:
    origin = validate_origin(origin)
    result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'origin': origin,
              'ai_requested': with_ai, 'checks': [], 'passed': False, 'cleanup': []}
    accounts = []
    api = origin + '/api/v1'
    try:
        health = expect(primary.get(api + '/health'), 200, 'health').json()
        if health.get('status') != 'ok':
            raise CheckFailure('health: service not ready')
        result['version'] = health.get('version')
        expect(primary.get(api + '/records'), 401, 'anonymous records')
        result['checks'].append('health_and_authentication_required')
        for client in (primary, secondary):
            client.headers['Origin'] = origin
            password = secrets.token_urlsafe(32)
            email = 'verify-' + secrets.token_hex(10) + '@example.org'
            response = expect(client.post(api + '/auth/register', json={
                'name': 'Verificacion temporal', 'email': email, 'password': password,
            }), 201, 'register')
            client.headers['X-CSRF-Token'] = response.json()['csrf_token']
            accounts.append((client, email, password))
            cookie = response.headers.get('set-cookie', '').lower()
            if 'httponly' not in cookie or 'samesite=lax' not in cookie:
                raise CheckFailure('session cookie: missing HttpOnly or SameSite=Lax')
            if origin.startswith('https://') and '; secure' not in cookie:
                raise CheckFailure('session cookie: missing Secure on HTTPS')
        result['checks'].append('registration_and_cookie_attributes')
        request = {'assessment': sample_assessment(), 'use_ai': with_ai}
        if with_ai:
            request['description'] = 'El correo del hotel utiliza doble factor. El resto del formulario sigue siendo valido.'
        record = expect(primary.post(api + '/records', json=request), 201, 'create record').json()
        if record['input']['hotel_profile']['rooms_count'] != 20 or not record['input']['security_controls']['uses_password_manager']:
            raise CheckFailure('combined input: structured answers were lost')
        if len(record['policy_pack']['policies']) != 10 or not record['actions']:
            raise CheckFailure('bundle: policies or actions missing')
        result['checks'].append('assessment_saved_with_structured_answers')
        if with_ai:
            if not (record['description_by_ai'] and record['policy_pack']['provider'] == 'openai'
                    and record['ai_summary']['generated_by_ai'] and record['ai_summary']['provider'] == 'openai'):
                raise CheckFailure('live AI: a stage used fallback; not a successful live AI check')
            result['checks'].append('live_ai_extraction_policies_and_summary')
        elif record['ai_summary']['provider'] != 'rules' or record['policy_pack']['provider'] != 'rules':
            raise CheckFailure('AI opt-out: expected local rules')
        identifier = record['id']
        route = api + '/records/' + identifier
        action = record['actions'][0]['id']
        expect(primary.patch(route + '/actions/' + action, json={'status': 'done'},
                             headers={'X-CSRF-Token': ''}), 403, 'missing CSRF')
        expect(primary.patch(route + '/actions/' + action, json={'status': 'done'}), 200, 'action progress')
        expect(primary.post(api + '/auth/logout'), 204, 'logout')
        expect(primary.get(route), 401, 'revoked session')
        _, email, password = accounts[0]
        session = expect(primary.post(api + '/auth/login', json={'email': email, 'password': password}), 200, 'login').json()
        primary.headers['X-CSRF-Token'] = session['csrf_token']
        stored = expect(primary.get(route), 200, 'persisted record').json()
        if not any(a['id'] == action and a['status'] == 'done' for a in stored['actions']):
            raise CheckFailure('progress: not retained after login')
        if expect(primary.get(api + '/records'), 200, 'history').json()['total'] != 1:
            raise CheckFailure('history: temporary account does not contain exactly one record')
        result['checks'].append('csrf_logout_history_and_persisted_progress')
        pdf = expect(primary.get(route + '/report.pdf'), 200, 'PDF')
        if not pdf.content.startswith(b'%PDF-') or 'application/pdf' not in pdf.headers.get('content-type', ''):
            raise CheckFailure('PDF: invalid signature or content type')
        result['checks'].append('authenticated_pdf_download')
        if expect(secondary.get(api + '/records'), 200, 'other history').json()['total'] != 0:
            raise CheckFailure('owner isolation: other history is not empty')
        for suffix in ('', '/report.pdf'):
            expect(secondary.get(route + suffix), 404, 'other owner read')
        expect(secondary.patch(route + '/actions/' + action, json={'status': 'done'}), 404, 'other owner edit')
        expect(secondary.delete(route), 404, 'other owner delete')
        expect(primary.get(route), 200, 'original record retained')
        result['checks'].append('cross_account_read_pdf_edit_delete_denied')
        result['passed'] = True
    except CheckFailure as error:
        result['failure'] = str(error)
    except (httpx.HTTPError, KeyError, TypeError, ValueError) as error:
        # Never serialize response bodies, generated passwords, tokens or provider errors.
        result['failure'] = f'Check could not complete: {type(error).__name__}'
    finally:
        for client, _, password in reversed(accounts):
            try:
                response = client.request('DELETE', api + '/auth/account', json={'password': password})
                removed = response.status_code == 204
            except httpx.HTTPError:
                removed = False
            result['cleanup'].append('account_deleted' if removed else 'account_cleanup_failed')
            if not removed:
                result['passed'] = False
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True, help='Your local origin or HTTPS deployment')
    parser.add_argument('--with-ai', action='store_true', help='Consent to sending fictional data; may spend API credit (up to 3 calls)')
    parser.add_argument('--confirm-test-data', action='store_true', help='Authorize creation and deletion of two temporary test accounts')
    parser.add_argument('--output', type=Path, help='Optional sanitized JSON evidence, never credentials or PDF contents')
    args = parser.parse_args()
    if not args.confirm_test_data:
        parser.error('Add --confirm-test-data to authorize the temporary accounts.')
    try:
        origin = validate_origin(args.url)
    except ValueError:
        parser.error('Use localhost HTTP or a remote HTTPS origin, without path or credentials.')
    with httpx.Client(timeout=120, follow_redirects=False) as primary, httpx.Client(timeout=120, follow_redirects=False) as secondary:
        result = verify(primary, secondary, origin, args.with_ai)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
