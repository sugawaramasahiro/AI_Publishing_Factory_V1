import os,zipfile,datetime,html
def export_to_epub(title,author,full_text):
    os.makedirs('output',exist_ok=True)
    safe=''.join(c for c in title if c.isalnum() or c in ' _').rstrip()
    path=f'output/{safe}_{datetime.datetime.now():%Y%m%d%H%M%S}.epub'
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml','''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>''')
        z.writestr('OEBPS/content.opf',f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="2.0">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:title>{html.escape(title)}</dc:title><dc:creator>{html.escape(author)}</dc:creator><dc:language>ja</dc:language>
<dc:identifier id="bookid">urn:uuid:{datetime.datetime.now().isoformat()}</dc:identifier></metadata>
<manifest><item id="c1" href="chap1.xhtml" media-type="application/xhtml+xml"/></manifest>
<spine><itemref idref="c1"/></spine></package>''')
        z.writestr('OEBPS/chap1.xhtml',f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja"><head><title>{html.escape(title)}</title></head>
<body><h1>{html.escape(title)}</h1><pre>{html.escape(full_text)}</pre></body></html>''')
    return path
