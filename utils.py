import re
import os
from datetime import datetime, timedelta
from config import remote, temp_dir, mysql_user, mysql_password, drive_base_folder


def cleanTempFolder():
    """
    Clean the temp folder
    """

    # Delete temp folder if it exists
    if os.path.exists(f'{temp_dir}'):
        os.system(f'rm -rf {temp_dir} > /dev/null')


def zipFolders(backup_folders):
    """
    Zip the folders

    Parameters:
    backup_folders (list): List of folders (e.g. ["example.com", "example2.com"])

    Returns:
    filename (str): Filelocation of the zip file (e.g. ".zip")
    """

    # Delete temp folder if it exists
    if os.path.exists(f'{temp_dir}/folders'):
        os.system(f'rm -rf {temp_dir}/folders > /dev/null')

    # Create temp folder
    os.system(f'mkdir -p {temp_dir}/folders > /dev/null')

    # Create tar.gz files for each folder
    for folder_path in backup_folders:

        # Get the folder name
        folder_name = folder_path.split("/")[-1]

        # Create the tar.gz file
        os.system(
            f'tar -czf {temp_dir}/folders/{folder_name}.tar.gz {folder_path} > /dev/null 2>&1')

    # Zip the folders
    os.system(
        f'zip -rj {temp_dir}/folders.zip {temp_dir}/folders/* > /dev/null')

    # Delete temp folder
    os.system(f'rm -rf {temp_dir}/folders > /dev/null')

    # Get the filename
    filename = f'{temp_dir}/folders.zip'

    return filename


def backupDatabase(backup_databases):
    """
    Backup the databases

    Parameters:
    backup_databases (list): List of databases (e.g. ["example", "example2"])

    Returns:
    filename (str): Filelocation of the zip file (e.g. ".zip")
    """

    # Delete temp folder if it exists
    if os.path.exists(f'{temp_dir}/databases'):
        os.system(f'rm -rf {temp_dir}/databases > /dev/null')

    # Create temp folder
    os.system(f'mkdir -p {temp_dir}/databases > /dev/null')

    # Create sql files for each database
    for database in backup_databases:
        os.system(
            f'mysqldump -u {mysql_user} -p{mysql_password} {database} > {temp_dir}/databases/{database}.sql')

    # Set the filename
    filename = f'{temp_dir}/databases.tar.gz'

    # Tar the databases
    os.system(f'tar -czf {filename} {temp_dir}/databases > /dev/null')

    # Delete temp folder
    os.system(f'rm -rf {temp_dir}/databases > /dev/null')

    return filename


def createFinalZipFile(zip_files):
    """
    Create the final zip file

    Returns:
    filename (str): Filelocation of the zip file (e.g. ".zip")
    """

    finalFilename = f'backup{datetime.now().strftime("%Y%m%d%H%M%S")}'

    # Delete temp folder if it exists
    if os.path.exists(f'{temp_dir}/final'):
        os.system(f'rm -rf {temp_dir}/final > /dev/null')

    # Create temp folder
    os.system(f'mkdir -p {temp_dir}/final > /dev/null')

    # Move the zip files to the temp folder
    for zip_file in zip_files:
        os.system(f'mv {zip_file} {temp_dir}/final > /dev/null')

    # Create the final zip file
    os.system(
        f'zip -rj {temp_dir}/{finalFilename}.zip {temp_dir}/final/* > /dev/null')

    # Delete temp folder
    os.system(f'rm -rf {temp_dir}/final > /dev/null')

    # Get the filename
    filename = f'{temp_dir}/{finalFilename}.zip'

    return filename


def getAllFilesFromGoogleDrive():
    """
    Get all files from Google Drive

    Returns:
    files (list): List of tuples with date_time and filename (e.g. [("2022-12-27 10:03:25", "backup20221227100325")])
    """

    # Get all files from the Google Drive
    files = os.popen(f'rclone lsd "{remote}:{drive_base_folder}"').read()

    files = extractFilenamesAndDateTimes(files)

    return files


def extractFilenamesAndDateTimes(data):
    """
    Extract filenames and dateTimes from the files.txt file

    Parameters:
    data (str): Data from the files.txt file (e.g. "           -1 2022-12-27 10:03:25        -1 backup20221227100325")

    Returns:
    files (list): List of tuples with date_time object and filename (e.g. [("2022-12-27 10:03:25", "backup20221227100325")])
    """

    # Split data into lines
    lines = data.strip().split("\n")

    files = []

    for line in lines:

        # Skip empty lines
        if line.strip() == "":
            continue

        # Extract dateTime and Filename from the line
        date_time, string = extractDateTimeAndFileName(line)

        # Append the Filename to the files list
        files.append((date_time, string))

    return files


def extractDateTimeAndFileName(line):
    """
    Extract dateTime and Filename from the lines

    Parameters:
    line (str): Line from the files.txt file (e.g. "           -1 2022-12-27 10:03:25        -1 backup20221227100325")

    Returns:
    date_time (datetime): Datetime of the file (e.g. "2022-12-27 10:03:25")
    string (str): Filename of the backup (e.g. "backup20221227100325")
    """

    # Extract dateTime
    date_time_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
    date_time_match = re.search(date_time_pattern, line)
    date_time = date_time_match.group(1)

    # Convert date_time to datetime
    date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

    # Extract Filename
    string_pattern = r'(backup(.)*)'
    string_match = re.search(string_pattern, line)
    string = string_match.group(1)

    return date_time, string


def filesOlderThenDays(files, days):
    """
    Get the files older then the given days

    Parameters:
    files (list): List of tuples with date_time and filename (e.g. [("2022-12-27 10:03:25", "backup20221227100325")])

    Returns:
    files_old (list): List of tuples with datetime object and filename (e.g. [(datetime.datetime(2022, 12, 27, 10, 3, 25), "backup20221227100325")])
    """

    # Get the current time
    now = datetime.now()

    # Get the files older then the given days
    files_old = []

    for date_time, string in files:

        # Check if the file is older then the given days
        if now - date_time > timedelta(days=days):
            files_old.append((date_time, string))

    return files_old


def deleteFiles(files):
    """
    Delete the files

    Parameters:
    files (list): List of tuples with date_time and filename (e.g. [("2022-12-27 10:03:25", "backup20221227100325")])
    """

    # Delete the files from the Google Drive (without trash)
    for date_time, string in files:
        os.system(
            f'rclone purge --drive-use-trash=false "{remote}:{drive_base_folder}/{string}" > /dev/null')


def uploadFileToGoogleDrive(filename):
    """
    Upload the file to the Google Drive

    Parameters:
    filename (str): Filelocation of the zip file (e.g. ".zip")
    """

    finalFilename = f'backup{datetime.now().strftime("%Y%m%d%H%M%S")}'

    # Upload the file to the Google Drive
    os.system(
        f'rclone copy "{filename}" "{remote}:{drive_base_folder}/{finalFilename}" > /dev/null')
