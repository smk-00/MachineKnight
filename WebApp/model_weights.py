from __future__ import print_function

import io

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload

credz = {
"type": "service_account",
  "project_id": "gdrivedownload-359013",
  "private_key_id": "35c5fb77c7b54325184fbd50954905574438e154",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDExBk/2cTqAcNs\nAuCnxUQpGcHFh0Ah/gC5HUiSqEIw0eYCKyKHGe87y3hRfPUlIElRaXWcFecrlk9l\nN0FK4nuC9ZrFJxsQhBRWrB27Y+zErpOIKeCdVvTqOxm9o1E0IL+XadQEp8XdY4/P\n2ORb0b6pggId85abpfJ0V88FUhK6EzfIQlZwfn4g/CjFDu96Gj45/sqoCN6R7GKO\nPSEm7FtNHD+LfmD4DAYLG6cM8OWVZSzRzsNLJs1or45eqMo/VZnWyt34YZdQHsXK\nskurH/fO1cTNVuWlxobsq/VswzuS0zhuU4toSkAVt1mL6nOIocPrkaGmv/jGhVDa\nIxvIxdcPAgMBAAECggEASqOIYGwfAhVBKAu/ZGS0AlM+6crwTPSpGY8+JEOnOBWn\nBlOOeWkhErGQJnkcFMU2iqdSca7tTd9qpp5bKijXaUn5N6gp4A36GRaZAKha/BCs\n7g3UolqF9QQOM51sBDYX9zuxrUJnEB/gQZuopBvgEzS50NrB2rEMU42rff0wFVzh\nVSN/xHRYYv0l8ThJss5TLlta5KXqnDgMthVX3ZGOReaaDzK1A6WLlLC9pPqGpGB7\npfFmEeIVbdpjKEfjnHjaerC6g8c1ozy7pODwo9l6EysbWQ9WqdVHcph1B9O1vOvy\n7NZXmuW6VTxIG6LEvtjOaaG50Bh6R98K0C7oBUecgQKBgQD9keuwfEg+L7CSUZyn\n/ZDSDT6nWA+iOIhLvpIpR1t4hurKOX6y59FKhBDV0KU9RCECrjoHx1l7092P/q5G\n3/3jozSgz8sYkXRHEJmdgjtsOVG93t+7oIzx64JZ70lMjl486f3/o1W+lXVlm30o\n/kvvfEUTl8Z1lKfW/cLqGUMuHwKBgQDGptJVofP3H9Mtg5H3TC3Au3M42ua/rynr\nFgAW3CHreJS6a3JaQeEG9z4I00Hwve+uqmMjh1fEgQJsaK37ZfgzjKY1XkhiDQcF\nUko3kEz8Jsh1xhy2WE6eBs5/Wp8ST7HnsjUf1khbfiFGXM+miy8uFOzf7UHRnkPu\nRg2lWNlZEQKBgQCOKqoCISw/8W0GHEvAxCHWIyblnDHnudpw3UAFdMSMJtis2N94\nXxCwvqrRtlFusCvx3M0cX2CEVJz8hsYfZqZqYq63Gsm71JFk5qG59bJrUxfJZJP8\nFl/voyNKWSa3jXq4nFiUY3dHi3Ruq2bY/PqGIx53hbj3Y4lWuJ/3sIJB8QKBgQCH\nONlmZxbNuoEiszPyFY3zauX05rU59/9dwh0Pcos4YV1ERI2TuNJ3zmcQ1NVHDdOQ\nnvVbIu7wmSzQJLWBspiwZmZhX6t/6wRDcA+LIRP2dGPyH4g964Cge1unP0WWzl74\nq8sTv+aDOSlnXxgOcyILiTzw9Ozfxo7RLChvzDovMQKBgHQZ6tjhacC97mCSkLnj\n5aG/s8JIvyvNybTayy2+kaZ02mtfj5q932Ok08NY9S1u032zhdby0z9b+/AWmcYt\nffCcbg/HOGoaAeEeIU8mH69fIUkN4B895ilNGNQTcYMpPUyhl4emBk7d1yZ+s5GX\nDthXUZg2qLlxfnQM5NphcGop\n-----END PRIVATE KEY-----\n",
  "client_email": "gd-downloader@gdrivedownload-359013.iam.gserviceaccount.com",
  "client_id": "105997150736805490085",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gd-downloader%40gdrivedownload-359013.iam.gserviceaccount.com"
}

def download_file(real_file_id, path):
    print("Downloading - "+path)
    creds = service_account.Credentials.from_service_account_info(credz)

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
	
        file_id = real_file_id

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id, supportsAllDrives=True, supportsTeamDrives=True)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            #print(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    # Write the stuff
    with open(path, "wb") as f:
        f.write(file.getbuffer())

    return file.getvalue()


def download():
    download_file(real_file_id='', path='')

download()

