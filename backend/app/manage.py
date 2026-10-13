"""Local administration only; never expose these commands through HTTP."""
import argparse
from datetime import timedelta
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from app.db import AccountToken, AiUsage, AuditEvent, LoginSession, User, audit, get_engine, utcnow


def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest='command', required=True)
    admin = commands.add_parser('grant-admin', help='Promote an existing, verified user')
    admin.add_argument('email')
    clean = commands.add_parser('cleanup', help='Remove expired sessions and old audit events')
    clean.add_argument('--audit-days', type=int, default=180)
    clean.add_argument('--apply', action='store_true', help='Without this flag, only show the count')
    args = parser.parse_args()
    with Session(get_engine()) as db:
        if args.command == 'grant-admin':
            user = db.scalar(select(User).where(User.email == args.email.lower()))
            if not user:
                parser.error('Create the account normally before granting its role.')
            user.role = 'admin'
            audit(db, user.id, 'role.admin_granted')
            db.commit()
            print('Administrator role granted to the specified account.')
        else:
            if args.audit_days < 1:
                parser.error('audit-days must be positive')
            conditions = [(LoginSession, LoginSession.expires_at < utcnow()),
                          (AccountToken, AccountToken.expires_at < utcnow()),
                          (AiUsage, AiUsage.expires_at < utcnow()),
                          (AuditEvent, AuditEvent.created_at < utcnow() - timedelta(days=args.audit_days))]
            for model, condition in conditions:
                rows = db.scalars(select(model).where(condition)).all()
                print(f'{model.__tablename__}: {len(rows)} eligible rows')
                if args.apply:
                    db.execute(delete(model).where(condition).execution_options(synchronize_session=False))
            if args.apply:
                db.commit()
            print('Applied.' if args.apply else 'Dry run only. Assessments are not deleted automatically.')


if __name__ == '__main__':
    main()
