# imports
import ftplib # connect to FTP
import os # file operations
import pandas as pd # use dataframes

# config values
FTP_SERVER='188.245.121.87'
FTP_USER='preprod'
FTP_PASSWORD='preprod' # UNSAFE - replace hardcoded credentials
FILE_PATH='../MOCK_DATA.csv'
UPLOAD_NAME='test.csv'

# this function uploads a file to the ftp server
def upload_file(path):
    try: 
        # connect to the ftp server
        ftp = ftplib.FTP(FTP_SERVER)
        ftp.login(FTP_USER, FTP_PASSWORD)
        ftp.cwd('uploads')

        # preview the file
        df = pd.read_csv(FILE_PATH)
        print(df.head())

        # open the file to upload  
        with open(os.path.join(path), 'rb') as file:
            # upload the file
            ftp.storbinary('STOR ' + UPLOAD_NAME, file)

        # close the connection
        print('🟢 File uploaded successfully')
        ftp.quit()
    except Exception as e:
        print('🔴 Error uploading file')
        print(str(e))
        ftp.quit()

# driver code
if __name__ == '__main__':
    upload_file(FILE_PATH)