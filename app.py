import os
import sqlite3
import json

from tornado import websocket, web, ioloop, httpserver, escape


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "uploads")

conn = sqlite3.connect(os.path.join(BASE_DIR, "toz.db"))
c = conn.cursor()


try:
    c.execute('CREATE TABLE files (id INTEGER PRIMARY KEY, filename VARCHAR(255), username VARCHAR(255))')
except sqlite3.OperationalError:
    pass


class BaseHandler(web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class LoginHandler(BaseHandler):
    def get(self):
        self.render("templates/account_tornado/login.html")

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")


class IndexHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.render("templates/account_tornado/index.html")


class UploadHandler(BaseHandler):

    @web.authenticated
    def post(self):
        filename = self.request.files['file /'][0]['filename']
        file = self.request.files['file /'][0]['body']

        if not os.path.exists(MEDIA_DIR):
            os.mkdir(MEDIA_DIR)

        with open(os.path.join(MEDIA_DIR, filename), 'wb') as f:
            f.write(file)
            username = escape.xhtml_escape(self.current_user)
            c.execute('INSERT INTO files (id, filename, username) VALUES (NULL, "%s", "%s")' % (filename, username))
            conn.commit()

        self.redirect("/")


class FilesHandler(websocket.WebSocketHandler):

    def send_files_list(self):
        c.execute("SELECT * FROM files ORDER BY id")
        files = [{'id': f[0], 'filename': f[1], 'username': f[2]} for f in c.fetchall()]
        data = json.dumps(files)
        self.write_message(data)

    def open(self):
        self.send_files_list()

    def on_message(self, message):
        data = json.loads(message)
        action = data.get('action')
        file_id = data.get('file_id')

		c.execute("SELECT filename FROM files WHERE id=%d" % (int(file_id)))
		file = c.fetchall()

        if action == 'delete':
            try:
                os.remove(os.path.join(MEDIA_DIR, file[0][0]))
            except:
                pass

            c.execute("DELETE FROM files WHERE id=%d" % (int(file_id)))
            conn.commit()

        elif action == 'download':
            # TODO
			# https://gist.github.com/alejandrobernardis/1790864
            pass

        self.send_files_list()


urls = [
    (r"/login", LoginHandler),
    (r"/", IndexHandler),
    (r"/upload", UploadHandler),
    (r"/files", FilesHandler),
    (r'/static/(.*)', web.StaticFileHandler, {'path': 'staticfiles'}),
]

settings = {
    "cookie_secret": str(os.urandom(45)),
    "login_url": "/login",
}

application = web.Application(urls, **settings)

if __name__ == "__main__":
    server = httpserver.HTTPServer(application)
    server.listen(1337)
    ioloop.IOLoop.instance().start()
