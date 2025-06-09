def query_image_content(self, image, content_type=''):
    """**Description**
            Find the image with the tag <image> and return its content.

        **Arguments**
            - image: Input image can be in the following formats: registry/repo:tag
            - content_type: The content type can be one of the following types:
                - os: Operating System Packages
                - npm: Node.JS NPM Module
                - gem: Ruby GEM
                - files: Files

        **Success Return Value**
            A JSON object representing the image content.
        """
    return self._query_image(image, query_group='content', query_type=content_type)