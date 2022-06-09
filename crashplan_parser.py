#!/usr/bin/python3
from tkinter.filedialog import askopenfilename, askdirectory

import pandas as pd

from csv_to_html import HtmlConvert


class CrashPlanParse:
    def __init__(self, file_in, user_group, file_out="output.csv"):
        self.file_in = file_in
        self.file_out = file_out
        self.user_group = user_group
        self.user_group = [f"{x}@andrew.cmu.edu" for x in self.user_group]
        self.fieldnames = [
            'archiveGuid', 'orgUid', 'orgName', 'orgExtRef',
            'userUid', 'username', 'email', 'userExtRef', 'deviceUid', 'deviceName',
            'deviceOsHostname', 'deviceExtRef', 'destinationUid', 'destinationName', 'serverUid',
            'serverName', 'version', 'status', 'userStatus', 'alertStates', 'os', 'osVersion',
            'address', 'remoteAddress', 'creationDate', 'selectedBytes', 'backupCompletePercentage',
            'archiveBytes', 'coldStorage', 'lastConnectedDate', 'lastCompletedBackupDate',
            'lastActivity', 'mostRecentUserProfileCreationResult', 'mostRecentUserProfileBackupResult'
        ]
        self.columns = ['username', 'deviceName', 'deviceOsHostname', 'version', 'status', 'userStatus', 'alertStates',
                        'os',
                        'creationDate', 'backupCompletePercentage', 'lastConnectedDate', 'lastCompletedBackupDate',
                        'lastActivity', 'mostRecentUserProfileCreationResult', 'mostRecentUserProfileBackupResult']
        self.fixcolumns = {'username': 'AndrewID', 'deviceName': 'Computer Name',
                           'deviceOsHostname': 'Windows Hostname', 'version': 'Version', 'status': 'Device Status',
                           'userStatus': 'User Status', 'alertStates': 'Alert Status', "os": 'OS',
                           'creationDate': 'Created On', 'backupCompletePercentage': 'Completion %',
                           'lastConnectedDate': 'Last Connected',
                           'lastCompletedBackupDate': 'Last Backup Completed', 'lastActivity': 'Last Activity',
                           "mostRecentUserProfileCreationResult": "Created Account on",
                           "mostRecentUserProfileBackupResult": "Most Recent Backup"}
        self.df = pd.read_csv(self.file_in, names=self.fieldnames, usecols=self.columns, sep=',', skiprows=1)
        self.df = self.df.rename(columns=self.fixcolumns)
        self.df = self.df.sort_values(by='Completion %', ascending=False)

    def get_depts(self):
        df_group = give_group(self.df, self.user_group)
        df_group.to_csv(self.file_out, index=False, header=True)

    def get_alerts(self, selected_dir):

        df_alert = alert_status(self.df)
        df_alert.to_csv(f"{selected_dir}\\alerts.csv", index=False, header=True)


def give_group(df, user_group):
    for i, row in df.iterrows():
        if row['AndrewID'] not in user_group:
            df = df.drop(i)
    return df


def alert_status(df):
    for i, row, in df.iterrows():
        if row['Alert Status'] == "OK":
            df = df.drop(i)
    return df


if __name__ == '__main__':
    group = ["jmckee",
             "sbaldrid",
             "smominee",
             "cjohnso2",
             "bvicini",
             "rspotts",
             "laurenca",
             "kwoessne",
             "trexler",
             "phannay",
             'bschles',
             "djebbia",
             "aperrier",
             "bdunckel",
             "jh8i",
             "rs57",
             "aperrier",
             "lmccord",
             "tdc2",
             "jpastva",
             "ebongiov",
             "lrhercki",
             "awerlini",
             "swelling",
             "sgmartin"
             ]
    importedfile = askopenfilename()
    outdirect = askdirectory()
    cp = CrashPlanParse(importedfile, group, f"{outdirect}\\output.csv")
    try:
        cp.get_depts()
        cp.get_alerts(outdirect)
    except FileNotFoundError:
        print("File or directory not given.")
        exit()
    for i in ["output", "alerts"]:
        conver = HtmlConvert(f'{outdirect}\\{i}.csv', f'{i}.html')
        conver.main()
    print(cp.user_group)

