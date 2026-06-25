from cloudinary_storage.storage import MediaCloudinaryStorage, VideoMediaCloudinaryStorage

class CustomMediaCloudinaryStorage(MediaCloudinaryStorage):
    def url(self, name):
        url = super().url(name)
        # Cloudinary returns 404 if the dummy version 'v1' is used with extensions when strict revisions are enabled.
        # Removing the /v1/ from the URL path fixes the issue and allows Cloudinary to serve the image.
        if '/upload/v1/' in url:
            url = url.replace('/upload/v1/', '/upload/')
        return url

class CustomVideoMediaCloudinaryStorage(VideoMediaCloudinaryStorage):
    def url(self, name):
        url = super().url(name)
        if '/upload/v1/' in url:
            url = url.replace('/upload/v1/', '/upload/')
        return url
