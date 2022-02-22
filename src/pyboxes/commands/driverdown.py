# !/usr/bin/env python
"""Download files in folder in Google Drive.

@Filename:    driver_down.py
@Author:      YangyangLi
@contact:     li002252@umn.edu
@license:     MIT Licence
@Time:        2/22/22 3:55 PM
"""
import io
import os
import pickle

import click
from apiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/drive"]


# To list folders
def listfolders(service, filid, des):
    """List files in a folder."""
    results = (
        service.files()
        .list(
            pageSize=1000,
            q="'" + filid + "'" + " in parents",
            fields="nextPageToken, files(id, name, mimeType)",
        )
        .execute()
    )
    # logging.debug(folder)
    folder = results.get("files", [])
    for item in folder:
        if str(item["mimeType"]) == "application/vnd.google-apps.folder":
            if not os.path.isdir(des + "/" + item["name"]):
                os.mkdir(path=des + "/" + item["name"])
            print(item["name"])
            listfolders(
                service, item["id"], des + "/" + item["name"]
            )  # LOOP un-till the files are found
        else:
            downloadfiles(service, item["id"], item["name"], des)
            print(item["name"])
    return folder


# To Download Files
def downloadfiles(service, dowid, name, dfilespath):
    """Download a file's content."""
    request = service.files().get_media(fileId=dowid)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with open(dfilespath + "/" + name, "wb") as f:
        fh.seek(0)
        f.write(fh.read())


def login(json_file):
    """Log in to Google Drive."""
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_pickle = "token.pickle"
    if os.path.exists(token_pickle):
        with open(token_pickle, "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                json_file, SCOPES
            )  # credentials.json download from drive API
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(token_pickle, "wb") as token:
            pickle.dump(creds, token)


@click.command(options_metavar="[options]")
@click.argument("json-file", type=click.Path(exists=True), metavar="<json>")
@click.argument("fid", type=click.STRING, metavar="<folder_id>")
def cli(json_file, fid) -> None:
    """Download files in folders in Google Drive.
    \b
    Usage:
    python driverdown <json-file> <folder_id>
    """
    creds = None
    login(json_file)
    service = build("drive", "v3", credentials=creds)
    # Call the Drive v3 API

    folder_id = f"'{fid}'"  # Enter The Downloadable folder ID From Shared Link

    results = (
        service.files()
        .list(
            pageSize=1000,
            q=folder_id + " in parents",
            fields="nextPageToken, files(id, name, mimeType)",
        )
        .execute()
    )
    items = results.get("files", [])
    if not items:
        print("No files found.")
    else:
        print("Files:")
        for item in items:
            print(f"{item['name']} {item['id']} {item['mimeType']}")

            if item["mimeType"] == "application/vnd.google-apps.folder":
                if not os.path.isdir("Folder"):
                    os.mkdir("Folder")
                bfolderpath = os.getcwd() + "/Folder/"
                if not os.path.isdir(bfolderpath + item["name"]):
                    os.mkdir(bfolderpath + item["name"])

                folderpath = bfolderpath + item["name"]
                listfolders(service, item["id"], folderpath)
            else:
                if not os.path.isdir("Folder"):
                    os.mkdir("Folder")
                bfolderpath = os.getcwd() + "/Folder/"
                if not os.path.isdir(bfolderpath + item["name"]):
                    os.mkdir(bfolderpath + item["name"])

                filepath = bfolderpath + item["name"]
                downloadfiles(service, item["id"], item["name"], filepath)


if __name__ == "__main__":
    cli()
