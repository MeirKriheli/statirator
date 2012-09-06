def parse_rst(content):
    """Parse multilingual rst document. Content should contain a metadata
    section which is the same for all languages, and sections for each
    language. the sections should be separated by comment of "--"". e.g:

        :slug: some-post-title-slugified
        :draft: 1/0 (Default assumes that it's published)
        :date: yyyy-mm-dd hh:mm:ss

        .. --

        :title: Some post title
        :lang: en
        :tags: Tag1, Tag2

        The content of the post

        .. --

        :title: The title in Hebrew
        :lang: he
        :tags: Heb Tag1|slug, Heb Tag2|slug

        The content of the post in hebrew

    Returned value is:

    (common metadata, (metadata, content), (metadata, content) ... )
    """
