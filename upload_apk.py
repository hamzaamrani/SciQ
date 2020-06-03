import dropbox
import sys


def upload(file, oauth2_access_token):
    dbx = dropbox.Dropbox(oauth2_access_token=oauth2_access_token)
    dbx.files_upload(open(file, "rb").read(), "/" + file)


if __name__ == "__main__":
    upload(sys.argv[1], sys.argv[2])
