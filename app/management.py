import subprocess
import sys
from pathlib import Path

from app.core.db import init_db


def run_alembic_command(command: str):
    """Run an alembic command"""
    try:
        result = subprocess.run(
            ["alembic"] + command.split(),
            cwd=Path(__file__).parent,
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running alembic command: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        sys.exit(1)


def create_migration(message: str):
    """Create a new migration"""
    print(f"Creating migration: {message}")
    run_alembic_command(f"revision --autogenerate -m '{message}'")


def upgrade_database():
    """Upgrade database to latest migration"""
    print("Upgrading database...")
    run_alembic_command("upgrade head")


def downgrade_database(revision: str = "-1"):
    """Downgrade database by one revision"""
    print(f"Downgrading database to {revision}...")
    run_alembic_command(f"downgrade {revision}")


def show_migration_history():
    """Show migration history"""
    print("Migration history:")
    run_alembic_command("history")


def show_current_revision():
    """Show current database revision"""
    print("Current revision:")
    run_alembic_command("current")


def create_tables_directly():
    """Create tables directly without migrations (for development)"""
    print("Creating tables directly...")
    try:
        init_db()
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python management.py <command> [args...]")
        print("Commands:")
        print("  create-migration <message>  - Create a new migration")
        print("  upgrade                     - Upgrade database")
        print("  downgrade [revision]        - Downgrade database")
        print("  history                     - Show migration history")
        print("  current                     - Show current revision")
        print("  create-tables               - Create tables directly")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create-migration":
        if len(sys.argv) < 3:
            print("Error: Migration message required")
            sys.exit(1)
        create_migration(sys.argv[2])
    elif command == "upgrade":
        upgrade_database()
    elif command == "downgrade":
        revision = sys.argv[2] if len(sys.argv) > 2 else "-1"
        downgrade_database(revision)
    elif command == "history":
        show_migration_history()
    elif command == "current":
        show_current_revision()
    elif command == "create-tables":
        create_tables_directly()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
