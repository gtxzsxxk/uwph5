#!/usr/bin/python3
import socket
import threading
import time
import traceback
import os
import re
from urllib.parse import unquote
import io

# 设置本地主机名
host = '0.0.0.0'
port = 8080

# 设置服务器Agent
servername = "STATIC RESOURCES SERVER"

# MIME
MIME_TYPE = {'323': 'text/h323', 'acx': 'application/internet-property-stream', 'ai': 'application/postscript', 'aif': 'audio/x-aiff', 'aifc': 'audio/x-aiff', 'aiff': 'audio/x-aiff', 'asf': 'video/x-ms-asf', 'asr': 'video/x-ms-asf', 'asx': 'video/x-ms-asf', 'au': 'audio/basic', 'avi': 'video/x-msvideo', 'axs': 'application/olescript', 'bas': 'text/plain', 'bcpio': 'application/x-bcpio', 'bin': 'application/octet-stream', 'bmp': 'image/bmp', 'c': 'text/plain', 'cat': 'application/vnd.ms-pkiseccat', 'cdf': 'application/x-cdf', 'cer': 'application/x-x509-ca-cert', 'class': 'application/octet-stream', 'clp': 'application/x-msclip', 'cmx': 'image/x-cmx', 'cod': 'image/cis-cod', 'cpio': 'application/x-cpio', 'crd': 'application/x-mscardfile', 'crl': 'application/pkix-crl', 'crt': 'application/x-x509-ca-cert', 'csh': 'application/x-csh', 'css': 'text/css', 'dcr': 'application/x-director', 'der': 'application/x-x509-ca-cert', 'dir': 'application/x-director', 'dll': 'application/x-msdownload', 'dms': 'application/octet-stream', 'doc': 'application/msword', 'dot': 'application/msword', 'dvi': 'application/x-dvi', 'dxr': 'application/x-director', 'eps': 'application/postscript', 'etx': 'text/x-setext', 'evy': 'application/envoy', 'exe': 'application/octet-stream', 'fif': 'application/fractals', 'flr': 'x-world/x-vrml', 'gif': 'image/gif', 'gtar': 'application/x-gtar', 'gz': 'application/x-gzip', 'h': 'text/plain', 'hdf': 'application/x-hdf', 'hlp': 'application/winhlp', 'hqx': 'application/mac-binhex40', 'hta': 'application/hta', 'htc': 'text/x-component', 'htm': 'text/html', 'html': 'text/html', 'htt': 'text/webviewhtml', 'ico': 'image/x-icon', 'ief': 'image/ief', 'iii': 'application/x-iphone', 'ins': 'application/x-internet-signup', 'isp': 'application/x-internet-signup', 'jfif': 'image/pipeg', 'jpe': 'image/jpeg', 'jpeg': 'image/jpeg', 'jpg': 'image/jpeg', 'js': 'application/x-javascript', 'latex': 'application/x-latex', 'lha': 'application/octet-stream', 'lsf': 'video/x-la-asf', 'lsx': 'video/x-la-asf', 'lzh': 'application/octet-stream', 'm13': 'application/x-msmediaview', 'm14': 'application/x-msmediaview', 'm3u': 'audio/x-mpegurl', 'man': 'application/x-troff-man', 'mdb': 'application/x-msaccess', 'me': 'application/x-troff-me', 'mht': 'message/rfc822', 'mhtml': 'message/rfc822', 'mid': 'audio/mid', 'mny': 'application/x-msmoney', 'mov': 'video/quicktime', 'movie': 'video/x-sgi-movie', 'mp2': 'video/mpeg', 'mp3': 'audio/mpeg', 'mpa': 'video/mpeg', 'mpe': 'video/mpeg', 'mpeg': 'video/mpeg', 'mpg': 'video/mpeg', 'mpp': 'application/vnd.ms-project', 'mpv2': 'video/mpeg', 'ms': 'application/x-troff-ms', 'mvb': 'application/x-msmediaview', 'nws': 'message/rfc822', 'oda': 'application/oda', 'p10': 'application/pkcs10', 'p12': 'application/x-pkcs12', 'p7b': 'application/x-pkcs7-certificates',
             'p7c': 'application/x-pkcs7-mime', 'p7m': 'application/x-pkcs7-mime', 'p7r': 'application/x-pkcs7-certreqresp', 'p7s': 'application/x-pkcs7-signature', 'pbm': 'image/x-portable-bitmap', 'pdf': 'application/pdf', 'pfx': 'application/x-pkcs12', 'pgm': 'image/x-portable-graymap', 'pko': 'application/ynd.ms-pkipko', 'pma': 'application/x-perfmon', 'pmc': 'application/x-perfmon', 'pml': 'application/x-perfmon', 'pmr': 'application/x-perfmon', 'pmw': 'application/x-perfmon', 'pnm': 'image/x-portable-anymap', 'pot,': 'application/vnd.ms-powerpoint', 'ppm': 'image/x-portable-pixmap', 'pps': 'application/vnd.ms-powerpoint', 'ppt': 'application/vnd.ms-powerpoint', 'prf': 'application/pics-rules', 'ps': 'application/postscript', 'pub': 'application/x-mspublisher', 'qt': 'video/quicktime', 'ra': 'audio/x-pn-realaudio', 'ram': 'audio/x-pn-realaudio', 'ras': 'image/x-cmu-raster', 'rgb': 'image/x-rgb', 'rmi': 'audio/mid', 'roff': 'application/x-troff', 'rtf': 'application/rtf', 'rtx': 'text/richtext', 'scd': 'application/x-msschedule', 'sct': 'text/scriptlet', 'setpay': 'application/set-payment-initiation', 'setreg': 'application/set-registration-initiation', 'sh': 'application/x-sh', 'shar': 'application/x-shar', 'sit': 'application/x-stuffit', 'snd': 'audio/basic', 'spc': 'application/x-pkcs7-certificates',
             'spl': 'application/futuresplash', 'src': 'application/x-wais-source', 'sst': 'application/vnd.ms-pkicertstore', 'stl': 'application/vnd.ms-pkistl', 'stm': 'text/html', 'svg': 'image/svg+xml', 'sv4cpio': 'application/x-sv4cpio', 'sv4crc': 'application/x-sv4crc', 'swf': 'application/x-shockwave-flash', 't': 'application/x-troff', 'tar': 'application/x-tar', 'tcl': 'application/x-tcl', 'tex': 'application/x-tex', 'texi': 'application/x-texinfo', 'texinfo': 'application/x-texinfo', 'tgz': 'application/x-compressed', 'tif': 'image/tiff', 'tiff': 'image/tiff', 'tr': 'application/x-troff', 'trm': 'application/x-msterminal', 'tsv': 'text/tab-separated-values', 'txt': 'text/plain', 'uls': 'text/iuls', 'ustar': 'application/x-ustar', 'vcf': 'text/x-vcard', 'vrml': 'x-world/x-vrml', 'wav': 'audio/x-wav', 'wcm': 'application/vnd.ms-works', 'wdb': 'application/vnd.ms-works', 'wks': 'application/vnd.ms-works', 'wmf': 'application/x-msmetafile', 'wps': 'application/vnd.ms-works', 'wri': 'application/x-mswrite', 'wrl': 'x-world/x-vrml', 'wrz': 'x-world/x-vrml', 'xaf': 'x-world/x-vrml', 'xbm': 'image/x-xbitmap', 'xla': 'application/vnd.ms-excel', 'xlc': 'application/vnd.ms-excel', 'xlm': 'application/vnd.ms-excel', 'xls': 'application/vnd.ms-excel', 'xlt': 'application/vnd.ms-excel', 'xlw': 'application/vnd.ms-excel', 'xof': 'x-world/x-vrml', 'xpm': 'image/x-xpixmap', 'xwd': 'image/x-xwindowdump', 'z': 'application/x-compress', 'zip': 'application/zip'}


def MakeError(title, content, foot):
    html = "<!DOCTYPE html><html><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1,user-scalable=0\"><title>Unhandled Exception</title><style>.window{margin-left:auto;margin-right:auto;width:auto;left:0;right:0;margin-top:100px;border-radius:8px;border-width:1px;border:solid;padding:10px}</style></head><body><div class=\"window\"><h1>%s</h1><h2>%s</h2><p></p><hr><h5>%s</h5></div></body></html>"
    return html % (title, content, foot)


def MakeReturn(url):
    #Access-Control-Allow-Origin
    source = "HTTP/1.1 200 OK\r\n" +\
        "Server: STATIC HTML DEBUGER\r\n" +\
        "Content-Type: text/html; charset=utf-8\r\n" +\
        "Access-Control-Allow-Origin: *\r\n" +\
        "Connection: close\r\n\r\n"
    try:
        path = url[1:]
        if os.path.exists(path):
            if os.path.isfile(path):
                # application/octet-stream
                file = open(path, 'rb')
                content = file.read()
                file.close()
                type="application/octet-stream"
                basename=os.path.basename(path)
                suffix=basename.split('.')[basename.split('.').__len__()-1]
                if suffix in MIME_TYPE.keys():
                    type=MIME_TYPE[suffix]
                source = "HTTP/1.1 200 OK\r\n" +\
                    "Server: STATIC HTML DEBUGER\r\n" +\
                    "Content-Type: %s; charset=utf-8\r\n"%type +\
                    "Content-Length: %d\r\n" % content.__len__() +\
                    "Access-Control-Allow-Origin: *\r\n" +\
                    "Connection: close\r\n\r\n"
                return (bytes(source, encoding='utf-8')+content, 'bin')
            else:
                return (source+MakeError("format error", "your request has a invalid auth.", servername), 'text')
        else:
            return (source+MakeError("404 File Not Found", "No file you requested existsZ", servername), 'text')
    except Exception as e:
        traceback.print_exc()
        return source+MakeError("Unhandled Exception", traceback.format_exc().replace('\n', '<br />'), servername)


class HttpThread(threading.Thread):
    clientSocket: socket.socket = None
    addr = None

    def __init__(self, clientsock, addr):
        threading.Thread.__init__(self)
        self.clientSocket = clientsock
        self.addr = addr

    def run(self):
        while(True):
            try:
                dstr = self.clientSocket.recv(2048)
                revdata = dstr.decode('utf-8')
                # print(revdata)
                param = revdata.split('\r\n')[0].split(' ')
                print(param)
                if param[0] == 'GET':
                    ret = MakeReturn(param[1])
                    if ret[1] == 'bin':
                        self.clientSocket.send(ret[0])
                    elif ret[1] == 'text':
                        self.clientSocket.send(bytes(ret[0], encoding='utf-8'))
                self.clientSocket.close()
            except Exception as e:
                traceback.print_exc()
                self.clientSocket.close()
                del self.clientSocket
            finally:
                return


# 创建 socket 对象
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
# 绑定端口号
serversocket.bind((host, port))
# 设置最大连接数，超过后排队
serversocket.listen(5)
print("服务器开始监听", host, port)
while True:
    # 建立客户端连接
    clientsocket, addr = serversocket.accept()
    print("%s %s连接服务器" %
          (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), str(addr)))
    httptd = HttpThread(clientsocket, addr)
    httptd.start()
