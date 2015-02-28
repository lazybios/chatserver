import socket
import select

class ChatServer:
    def __init__(self, port):
        self.port = port
        self.srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.srvsock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srvsock.bind(("", port))
        self.srvsock.listen(5)

        self.deslist = [self.srvsock]
        print 'ChatServer started on port %s' % port

    def run(self):
        while 1:
            (sread, swrite, sexc) = select.select( self.deslist, [], [])
            for sock in sread:
                if sock == self.srvsock:
                    self.accept_new_connection()
                else:
                    str1 = sock.recv(100)

                    if str1 == '':
                        host,port = sock.getpeername()
                        str1 = 'Client left %s:%s\r\n' % (host, port)
                        self.broadcast_string( str1, sock )
                        sock.close
                        self.deslist.remove(sock)
                    else:
                        host,port = sock.getpeername()
                        newstr = '[%s:%s] %s' % (host, port, str1)
                        self.broadcast_string( newstr, sock )


    def accept_new_connection(self):
        newsock, (remhost, remport) = self.srvsock.accept()
        self.deslist.append( newsock )
        newsock.send("You're connected to the Python chatserver\r\n")
        str1 = 'Client joined %s:%s\r\n' % (remhost, remport)
        self.broadcast_string( str1, newsock )


    def broadcast_string(self,msg,omit_sock):
        """docstring for broadcast_string"""
        for sock in self.deslist:
            if sock != self.srvsock and sock != omit_sock:
                sock.send(msg)
                print msg

if __name__ == '__main__':
    myServer = ChatServer(2526)
    myServer.run()

