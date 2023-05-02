import csv
import json
from io import BytesIO
from ftplib import FTP

csv_url = "aftp.cmdl.noaa.gov"
csv_path = "/products/trends/co2/"

# Connect to the FTP server and fetch the CSV file
ftp = FTP(csv_url)
ftp.login()
ftp.cwd(csv_path)
csv_data = BytesIO()
ftp.retrbinary("RETR co2_weekly_mlo.csv", csv_data.write)
csv_data.seek(0)  # Reset the file pointer to the beginning
ftp.quit()

# Read the CSV data and remove comment lines
rows = filter(lambda x: not x.startswith('#'), csv_data.getvalue().decode().splitlines())
csv_reader = csv.reader(rows)
headers = next(csv_reader)  # Read the header row
last_row = None
for row in csv_reader:
    last_row = row

# Convert the last row to a JSON string
json_data = json.dumps(dict(zip(headers, last_row)))

# Print the JSON string
print(json_data)
