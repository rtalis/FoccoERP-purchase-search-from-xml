import os
import shutil
from datetime import datetime, timedelta

# Configuration
DB_PATH = 'instance/data.db'  # Path to your SQLite database file
BACKUP_DIR = 'instance'  # Directory where backups will be stored
DAILY_BACKUP_RETENTION = 7  # Keep daily backups for the last 7 days
WEEKLY_BACKUP_RETENTION = 4  # Keep weekly backups for the last 4 weeks

# Ensure backup directory exists
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

def create_backup():
    """Create a new backup of the SQLite database."""
    today = datetime.now()
    daily_backup_filename = f"daily_backup_{today.strftime('%Y%m%d')}.db"
    backup_path = os.path.join(BACKUP_DIR, daily_backup_filename)

    try:
        shutil.copyfile(DB_PATH, backup_path)
        print(f"Database backup successful: {backup_path}")
    except Exception as e:
        print(f"Failed to backup database: {e}")

def remove_old_backups():
    """Remove old backups beyond the retention period."""
    today = datetime.now()

    # List all backup files in the backup directory
    for filename in os.listdir(BACKUP_DIR):
        file_path = os.path.join(BACKUP_DIR, filename)

        # Determine if the backup is a daily or weekly backup based on its filename
        if filename.startswith('daily_backup_'):
            # Calculate the backup date
            backup_date = datetime.strptime(filename[len('daily_backup_'):-3], '%Y%m%d')
            age = (today - backup_date).days

            # Remove daily backups older than the retention period
            if age > DAILY_BACKUP_RETENTION:
                os.remove(file_path)
                print(f"Removed old daily backup: {filename}")

        elif filename.startswith('weekly_backup_'):
            # Calculate the backup date
            backup_date = datetime.strptime(filename[len('weekly_backup_'):-3], '%Y%m%d')
            age = (today - backup_date).days

            # Remove weekly backups older than the retention period
            if age > WEEKLY_BACKUP_RETENTION * 7:
                os.remove(file_path)
                print(f"Removed old weekly backup: {filename}")

def promote_daily_backup_to_weekly():
    """Promote the last daily backup to a weekly backup if necessary."""
    today = datetime.now()

    # Check if today is the end of the weekly backup cycle (e.g., Sunday)
    if today.weekday() == 6:  # Sunday
        # Find the latest daily backup
        latest_daily_backup = None
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith('daily_backup_'):
                backup_date = datetime.strptime(filename[len('daily_backup_'):-3], '%Y%m%d')
                if latest_daily_backup is None or backup_date > latest_daily_backup:
                    latest_daily_backup = backup_date

        if latest_daily_backup:
            weekly_backup_filename = f"weekly_backup_{latest_daily_backup.strftime('%Y%m%d')}.db"
            daily_backup_path = os.path.join(BACKUP_DIR, f"daily_backup_{latest_daily_backup.strftime('%Y%m%d')}.db")
            weekly_backup_path = os.path.join(BACKUP_DIR, weekly_backup_filename)

            # Copy the daily backup to a weekly backup
            shutil.copyfile(daily_backup_path, weekly_backup_path)
            print(f"Promoted daily backup to weekly backup: {weekly_backup_filename}")

if __name__ == "__main__":
    create_backup()  # Create today's backup
    remove_old_backups()  # Clean up old backups
    promote_daily_backup_to_weekly()  # Promote a daily backup to a weekly backup if necessary
