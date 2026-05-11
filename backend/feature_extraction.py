def extract_url_features(url):
    return [
        len(url),
        url.count('.'),
        1 if "https" in url else 0,
        int(any(c.isdigit() for c in url)),
        int(any(c in url for c in ['@', '-', '_']))
    ]