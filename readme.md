# Backup to drive
Helps to backup given folders and databases on a linux server to Google Drive Using Rclone.

## Requirements
- Linux Server
- Rclone (`sudo -v ; curl https://rclone.org/install.sh | sudo bash`)
- Python 3.7+
- Zip

## Installation
- Install and configure Rclone (https://rclone.org/)
- Install Python 3.7+
- Install zip command
- Update the config.ini file with your details
- Test the script by running `python3 backup.py`
- Schedule the script to run using Linux Cron
    - `crontab -e`
    - `30 2 * * * /usr/bin/python3 /root/Backup-to-drive/backup.py > /root/Backup-to-drive/backup.log`
    - This will run the script at 2:30 AM everyday and log the output to backup.log file

## License
Apache License 2.0

## Author Information
- [Satyam Gupta](https://imlolman.github.io/)
