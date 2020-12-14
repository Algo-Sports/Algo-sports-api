from urllib.parse import quote


def compare_url(quoted_url, raw_url):
    return quoted_url == quote(raw_url)
