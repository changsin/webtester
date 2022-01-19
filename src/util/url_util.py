import re

from urllib.parse import urlparse


def normalize_url(url):
    """
    normalizes url - currently only the ending / or #
    :param url:
    :return:
    """
    if url.endswith("/") or url.endswith("#"):
        url = url[:len(url) - 1]
    return url.lower()


def is_same_page(source_url, target_url):
    """
    True if it's the same sub page regardless of the query string
    :param source_url:
    :param target_url:
    :return:
    """
    source_parsed = urlparse(normalize_url(source_url))
    target_parsed = urlparse(normalize_url(target_url))
    return source_parsed.netloc.lower() == target_parsed.netloc.lower() and \
        source_parsed.path.lower() == target_parsed.path.lower() and \
        source_parsed.query.lower() == target_parsed.query.lower()


def is_same_domain(source_url, target_url):
    """
    True if the target url is within the same domain as the source url
    False otherwise
    :param source_url: source url
    :param target_url:
    :return:
    """
    source_parsed = urlparse(source_url)
    target_parsed = urlparse(target_url)

    # a sub-url has no scheme: e.g., #none /v2/Home
    # don't check whether it is http or https. Just check whether it is a sub-page or not.
    if not target_parsed.scheme or (target_parsed.scheme != 'http' and target_parsed.scheme != 'https'):
        return True

    # NB: not checking the equality of scheme because a site can have both http and https
    return source_parsed.netloc.lower() == target_parsed.netloc.lower()


def is_same_domain_new_page(source_url, target_url):
    """
    True if the target url is within the same domain as the source url
    False otherwise
    :param source_url: source url
    :param target_url:
    :return:
    """
    source_parsed = urlparse(source_url)
    target_parsed = urlparse(target_url)
    return source_parsed.netloc.lower() == target_parsed.netloc.lower() and \
        (source_parsed.path.lower() != target_parsed.path.lower() or
         source_parsed.query.lower() != target_parsed.query.lower())


def is_domain_whitelisted(patterns, target_url):
    """
    a filter consists of two parts: (scope_pattern, select_pattern)
    the scope_pattern prescribes the scope: the set of xpaths that this pattern is applicable to - e.g., /div/div/ul/li
    the select_pattern decides exactly which elements are to be selected for crawling
    :param patterns: domain patterns
    :param target_url: target_url to test
    :return:
    """
    if not patterns or not target_url:
        return False

    target_parsed = urlparse(target_url)
    target_domain = target_parsed.netloc

    for pattern in patterns:
        pattern = pattern.replace('*', '.+')
        pattern_parsed = urlparse(pattern)
        pattern_domain = pattern_parsed.netloc
        matched = re.search(pattern_domain, target_domain)
        if matched:
            return True


def to_file_name(url):
    to_replace_dict = {
        "https": "",
        "http": "",
        "://": "",
        "/": "_",
        "www.": "",
        "?": "-",
        "&": "-",
        "#": "-",
        "=": "-",
        ":": "_"
    }

    filename = url

    for u, v in to_replace_dict.items():
        filename = filename.replace(u, v)

    return filename

