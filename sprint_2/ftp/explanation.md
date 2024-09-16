# Data Sources
> using data from ftp, web scraping and databases for data science

### FTP as a data source
+ reads data from a remote server
+ supports text, csv and other files with 2D table structure
+ supports file compression and parallel reads from multiple files

- ftp servers do not distinguish between data types

##### Test FTP server
> using vsftpd on ubuntu
- ftp://188.245.121.87
- user: preprod

##### Uploading a file
> using inetutils-ftp on mac
run `upload.py` to upload `MOCK_DATA.csv` to the FTP server

##### Reading data from FTP server
> using 
