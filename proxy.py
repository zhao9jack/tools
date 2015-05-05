import urllib2
 
of = open('proxy.txt' , 'w')
 
for page in range(1, 160):
    html_doc = urllib2.urlopen('http://www.xici.net.co/nn/' + str(page) ).read()
    soup = BeautifulSoup(html_doc)
    trs = soup.find('table', id='ip_list').find_all('tr')
    for tr in trs[1:]:
        tds = tr.find_all('td')
        ip = tds[1].text.strip()
        port = tds[2].text.strip()
        protocol = tds[5].text.strip()
        if protocol == 'HTTP' or protocol == 'HTTPS':
            of.write('%s=%s:%s\n' % (protocol, ip, port) )
            print '%s=%s:%s' % (protocol, ip, port)
 
of.close()




import httplib
import time
import urllib
import threading
 
inFile = open('proxy.txt', 'r')
outFile = open('available.txt', 'w')
 
lock = threading.Lock()
 
def test():
    while True:
        lock.acquire()
        line = inFile.readline().strip()
        lock.release()
        if len(line) == 0: break
        protocol, proxy = line.split('=')
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': ''}
        try:
            conn = httplib.HTTPConnection(proxy, timeout=3.0)
            conn.request(method='POST', url='http://baidu.com', body='n=1', headers=headers )
            res = conn.getresponse()
            ret_headers = str( res.getheaders() ) 
            html_doc = res.read().decode('utf-8')
            print html_doc.encode('gbk')
            if ret_headers.find(u'/m/account/login/') > 0:
                lock.acquire()
                print 'add proxy', proxy
                outFile.write(proxy + '\n')
                lock.release()
            else:
                print '.',
        except Exception, e:
            print e
 
all_thread = []
for i in range(50):
    t = threading.Thread(target=test)
    all_thread.append(t)
    t.start()
    
for t in all_thread:
    t.join()
 
inFile.close()
outFile.close()
