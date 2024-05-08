import requests


class FedoraObject:
    def __init__(self, auth, fedora_uri, pid):
        self.auth = auth
        self.fedora_uri = fedora_uri
        self.pid = f"{pid.replace('info:fedora/','').strip()}"

    @staticmethod
    def __guess_extension(content_type):
        mimetypes = {
            "image/tiff": "tif",
            "image/jp2": "jp2",
            "application/xml": "xml",
            "application/pdf": "pdf",
            "audio/vnd.wave": "wav",
            "image/jpeg": "jpg",
            "text/plain": "txt",
            "text/x-asm": "vtt",
            "text/x-c++": "vtt",
            "text/x-c": "vtt",
            "video/dv": "dv",
        }
        return mimetypes.get(content_type, "bin")

    def getDatastream(self, dsid, output):
        r = requests.get(
            f"{self.fedora_uri}/objects/{self.pid}/datastreams/{dsid}/content",
            auth=self.auth,
            allow_redirects=True,
        )
        if r.status_code == 200:
            open(
                f'{output}/{self.pid}_{dsid}.{self.__guess_extension(r.headers.get("Content-Type", "application/binary"))}',
                "wb",
            ).write(r.content)
        else:
            print(f"{r.status_code} on {self.pid}.")
        return
