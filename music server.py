from http.server import SimpleHTTPRequestHandler
from http import HTTPStatus
import datetime
from http.server import HTTPServer
import html
import io
import os
import sys
import urllib.parse


class RequestHandler(SimpleHTTPRequestHandler):
	def list_directory(self, path):
		try:
			list = os.listdir(path)
		except OSError:
			self.send_error(HTTPStatus.NOT_FOUND, "No permission to list directory")
			return None
		list.sort(key=lambda x: os.path.getmtime(x))
		csort = lambda l: (csort(l[1:]) + l[:1] if l else [])
		list = csort(list)
		r = []
		try:
			displaypath = urllib.parse.unquote(self.path, errors='surrogatepass')
		except UnicodeDecodeError:
			displaypath = urllib.parse.unquote(path)
		displaypath = html.escape(displaypath, quote=False)
		enc = sys.getfilesystemencoding()
		title = 'Directory listing for %s' % displaypath
		r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
				 '"http://www.w3.org/TR/html4/strict.dtd">')
		r.append('<html>\n<head>')
		r.append('<meta http-equiv="Content-Type" '
				 'content="text/html; charset=%s">' % enc)
		r.append('<title>%s</title>\n</head>' % title)
		r.append('<body>')
		r.append('<table>')
		for name in list:
			fullname = os.path.join(path, name)
			displayname = linkname = name
			if os.path.isdir(fullname) or name.find('.mp3') == -1:
				continue
			if os.path.islink(fullname):
				displayname = name + "@"
			r.append(('<tr><td><a href="%s">%s</a> </td><td>' + datetime.datetime.fromtimestamp(
					int(os.path.getmtime(name))).strftime('  %d.%m.%Y %H:%M:%S') + '</td> </tr>') % (
						 urllib.parse.quote(linkname, errors='surrogatepass'), html.escape(displayname, quote=False)))
		r.append('</table>\n<hr>\n</body>\n</html>\n')
		encoded = '\n'.join(r).encode(enc, 'surrogateescape')
		f = io.BytesIO()
		f.write(encoded)
		f.seek(0)
		self.send_response(HTTPStatus.OK)
		self.send_header("Content-type", "text/html; charset=%s" % enc)
		self.send_header("Content-Length", str(len(encoded)))
		self.end_headers()
		return f


httpd = HTTPServer(("", 8000), RequestHandler)
print("serving at port", 8000)
httpd.serve_forever()
