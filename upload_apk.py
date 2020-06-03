import dropbox
import os
import re
import sys


def upload(file, apks_dir, oauth2_access_token):
    max_version = "0.0"
    for apk in os.listdir(apks_dir):
        match = re.search(r"(\d+(\.\d)*)", apk)
        if match is not None:
            version = match.group(1)
            if float(version) > float(max_version):
                max_version = version
    new_version = os.path.join(
        apks_dir, "sciq_v." + (float(max_version) + 0.1) + ".apk"
    )
    os.rename(
        os.path.join(apks_dir, file),
        os.path.join(apks_dir, "sciq_v." + max_version + ".apk"),
    )
    dbx = dropbox.Dropbox(oauth2_access_token=oauth2_access_token)
    dbx.files_upload(open(new_version, "rb").read(), "/" + new_version)


if __name__ == "__main__":
    upload(sys.argv[1], sys.argv[2], sys.argv[3])
