# imports
import ftplib # connect to FTP
import os # file operations
import pandas as pd # use dataframes

# config values
FTP_SERVER='188.245.121.87'
FTP_USER='preprod'
FTP_PASSWORD='preprod'
FILE_NAME='MOCK_DATA.csv'
DOWNLOAD_PATH='sprint_2/FTP_DATA.csv'

# this function downloads a file from the ftp server
def download_file(path):
    try: 
        # connect to the ftp server
        ftp = ftplib.FTP(FTP_SERVER)
        ftp.login(FTP_USER, FTP_PASSWORD)
        ftp.cwd('uploads')

        # open the file to download
        with open((DOWNLOAD_PATH), 'wb') as file:
            # download the file
            ftp.retrbinary('RETR ' + FILE_NAME, file.write)

        # preview file
        df = pd.read_csv(DOWNLOAD_PATH)
        print(df.head())

        # close the connection
        print('🟢 File downloaded successfully')
        ftp.quit()
    except Exception as e:
        print('🔴 Error downloading file')
        print(str(e))
        ftp.quit()

# driver code
if __name__ == '__main__':
    download_file(DOWNLOAD_PATH)