def render(html, feed):
    with open(html) as f:
        s = f.read()
    print(s)
    if feed:
        return s.format(**feed).encode('utf-8')
    else:
        return s.encode('utf-8')
