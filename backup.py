import re
import utils
from config import backup_folders, backup_databases, retention_days

def createBackup():
    """
    Create the backup of Given Folders and Databases and upload it to Google Drive

    """

    # Clean the temp folder before starting the backup
    print(":: Cleaning the temp folder...")
    utils.cleanTempFolder()

    finalZipFiles = []

    # Take the backup of the given folders and zip them
    if len(backup_folders) > 0:
        print(":: Zipping the folders for backup...")
        zippedFile = utils.zipFolders(backup_folders)
        finalZipFiles.append(zippedFile)
        print("------ Zip file: " + zippedFile)

    # Take the backup of the given databases and zip them
    if len(backup_databases) > 0:
        print(":: Dumping the databases for backup...")
        dbFile = utils.backupDatabase(backup_databases)
        finalZipFiles.append(dbFile)
        print("------ Database file: " + dbFile)

    # Create a final zip file that combines the zipped folders and the database dump
    print(":: Creating a final zip file...")
    finalZipFile = utils.createFinalZipFile(finalZipFiles)
    print("------ Final zip file: " + finalZipFile)

    # Upload the final zip file to Google Drive
    print(":: Uploading the final zip file to Google Drive...")
    utils.uploadFileToGoogleDrive(finalZipFile)

def deleteOldBackups():
    """
    Delete the old backups from the Google Drive Backup folder

    """

    # Get all the files from the Google Drive Backup folder
    print(":: Getting all the files from the Google Drive Backup Folder...")
    files = utils.getAllFilesFromGoogleDrive()
    print("------ Files: ", files)

    # Get the files older then the retention_days
    print(f":: Getting the files older then {retention_days} days...")
    files = utils.filesOlderThenDays(files, retention_days)
    print("------ Files: ", files)

    # Delete the files using rclone
    print(":: Deleting the files using rclone...")
    utils.deleteFiles(files)

if __name__ == "__main__":
    finalZipFile = createBackup()
    deleteOldBackups()





