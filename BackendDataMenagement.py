import os
import csv 
import datetime
import subprocess

class LicenseStorage:
    # on inicialization of class set the path where the licenses will be stored
    # if the path does not exist, create it
    def __init__(self,path):
        self.FolderPath = path
        if not os.path.exists(self.FolderPath):
            os.makedirs(self.FolderPath)
    
    # create a new project with the name ProjectName witch will be a csv file containing the licenses
    def newProject(self, ProjectName):
        ProjectPath = os.path.join(self.FolderPath, ProjectName + ".csv")
        if not os.path.exists(ProjectPath):
            with open(ProjectPath, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['License','SerialNumber','Status','DateTime'])
        else:
            print(f"Project {ProjectName} already exists.")
        return None
    
    # list all projects in the folder
    def listProjects(self):
        projects = [f[:-4] for f in os.listdir(self.FolderPath) if f.endswith('.csv')]
        return projects
    
    # add a license to the project ProjectName
    def AddSingleLicense(self, ProjectName, License):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ProjectPath = os.path.join(self.FolderPath, ProjectName + ".csv")
        if not os.path.exists(ProjectPath):
            raise FileNotFoundError(f"Project {ProjectName} does not exist.")
        
        with open(ProjectPath, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([License,'','Unused',timestamp])
        return None
    
    # add multiple licenses to the project ProjectName from a set of strings separated by new lines
    def AddLicenses(self, ProjectName, License):
        licenses = License.split('\n')
        for lic in licenses:
            self.AddSingleLicense(ProjectName, lic.strip())
    
    # get the first unused license from a specific project
    def getLicense(self, ProjectName):
        ProjectPath = os.path.join(self.FolderPath, ProjectName + ".csv")
        if not os.path.exists(ProjectPath):
            print(f"Project {ProjectName} does not exist.")
            return None
        with open(ProjectPath, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Status'] == 'Unused':
                    return row['License']
        return None
    
    # change the status of a license in a specific project
    # Status can be 'Used', 'Unused', or 'Expired'
    def changeStatus(self, ProjectName, License, Status):
        if Status not in ['Used', 'Unused', 'Expired']:
            raise ValueError("Invalid status")
        if Status == "Used":
            serialNumber = subprocess.run(["powershell", "-Command", "get-CimInstance -Class Win32_BIOS | Select-Object -ExpandProperty SerialNumber"], capture_output=True, text=True).stdout.strip()
        else:
            serialNumber = ''
        ProjectPath = os.path.join(self.FolderPath, ProjectName + ".csv")
        if not os.path.exists(ProjectPath):
            raise FileNotFoundError(f"Project {ProjectName} does not exist.")
        UpdatedRow = []
        with open(ProjectPath, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['License'] == License:
                    row['Status'] = Status
                    row['SerialNumber'] = serialNumber
                UpdatedRow.append(row)

        with open(ProjectPath, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['License', 'SerialNumber', 'Status', 'DateTime'])
            writer.writeheader()
            writer.writerows(UpdatedRow)
        return None


# for testing purposes
def main():
    storage = LicenseStorage("licenses")
    storage.newProject("TestProject")
    storage.AddSingleLicense("TestProject", "ABC123")

    print(storage.listProjects())
    print(storage.getLicense("TestProject"))
    storage.changeStatus("TestProject", "ABC123", "Used")
    print(storage.getLicense("TestProject"))
    # Example: Paste your licenses as a single string separated by newlines
    licenses = """
XWM8G-NVQ6D-2YBQD-PDFDC-PGYP6
XG8F6-JNTQJ-X6KG9-7KW6T-TJF9G
VVDMH-NVVRY-J79GK-9B2HM-JK8XG
NPJ22-RJM4H-8CWBT-CVYFK-4JRC6
XR4YP-NJQ8G-8DYRB-9VGP8-29XTT
MJXVN-Q6V7K-Y93PY-BDKM7-CYT6T
YQPGF-VNR8P-FKMX2-97XXX-QV66T
XFNK4-7VVJJ-GD4J9-TYFHD-MDWXG
VGQ3J-NQHFF-CFMWB-XTCTC-6JF9G
4VHH8-XN9JY-69PY6-GVRWD-GF4C6
RCDDD-9KN9P-JTPD4-MVR8T-6F4C6
PQPNF-XCPWY-MRWWC-F48TX-8QKTT
VMTFJ-BCN8F-V3MF9-J4KFQ-KKXTT
NGYYF-M2RQV-T4KRM-26M4M-RC2KG
TNCFM-443P3-PXFKM-9Y48C-JB49G
NM8GD-W7FGT-CDDPP-2Q2QR-369TT
V2P68-4GN2K-TMJT6-PM2XK-YDWXG
74NBJ-6FMFQ-2X8KT-C6X3X-MG9TT
MT8XC-2PN8P-6JF7P-QT942-8XCKG
F4WDX-YNBK8-VMGDK-H3RG8-JFG6T
4NXQY-44C7Q-MF3FH-2QF2J-J8F9G
TF6WP-NQWP4-MM6TW-HX9JD-Y4G6T
DTJRN-JMF9T-DXC43-K63WH-CYT6T
3NXGH-44QM2-JXT63-DGM8F-MWRC6
7NPXW-RVFKB-HK72P-R7FXB-YWRC6
8X87T-NVBTD-72X84-43HYQ-4GDGT
7CN4X-QGW8Q-RGP8K-V7DRT-4M49G
""".strip()
    storage.AddLicenses("TestProject", licenses)
    print(storage.listProjects())
    license = storage.getLicense("TestProject")
    print(f"First unused license: {license}")
    storage.changeStatus("TestProject", license, "Used")
    print(storage.getLicense("TestProject"))
if __name__ == "__main__":
    main()