
import configparser
import pathlib
import ast


def read_config(config_file):
    """
    Read the configuration from the config.ini file

    Parameters:
    config_file (str): Path to the config.ini file (e.g. "config.ini")

    Returns:
    config (ConfigParser): ConfigParser object with the configuration
    """
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration from the file
    config.read(config_file)

    return config


# Get the path to the current file
path = pathlib.Path(__file__).parent.resolve()

# Read the configuration from the config.ini file
config = read_config(path / "config.ini")

remote = config.get('Backup', 'RcloneRemoteName')
backup_folders = ast.literal_eval(config.get('Backup', 'BackupFolders'))
backup_databases = ast.literal_eval(config.get('Backup', 'BackupDatabases'))
temp_dir = config.get('Backup', 'TempDir')
retention_days = int(config.get('Backup', 'RetentionDays'))
# print(backup_folders, backup_databases, temp_dir, retention_days)

mysql_user = config.get('MySQL', 'Username')
mysql_password = config.get('MySQL', 'Password')
# print(mysql_user, mysql_password)

drive_base_folder = config.get('GoogleDrive', 'BaseFolder')
# print(drive_base_folder)
