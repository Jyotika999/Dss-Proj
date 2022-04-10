from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from random import randint
import os
import time

connect_flag = 0
user_flag = 0
recv_flag = 0

class Client(DatagramProtocol):
     def __init__ (self, host, port):
          if host == "localhost":
               host = "127.0.0.1"

          self.address = None
          self.id = host, port
          self.server = "127.0.0.1", 9999
          self.name = ""
          self.other_user = ""
          print("Menu commands : ")
          print("__end__ : Stops communication and closes the client")
          print("__users__ : To get a list of current online users")
          print("__connect__ : To connect to other online user")
          print("__chats__ : To get all previous chats")
          print("Working on id:", self.id)

     def startProtocol(self):
          
          name = input("Name: ")
          self.name = name
          line = "ready:"+name
          self.transport.write(line.encode('utf -8'), self.server)
          reactor.callInThread(self.poll_connect)
     

     def poll_connect(self):

          global connect_flag
          global user_flag
          global recv_flag

          while True:
               ip = input("Enter menu command: ")
               if ip == "__users__":
                    user_flag = 1
                    self.transport.write("users".encode('utf -8'), self.server)
                    time.sleep(1)
               elif ip == "__connect__":
                    connect_flag = 1
                    recv_flag = 1
                    name = input("Enter name of user: ")
                    self.other_user = name
                    line = "query:"+name
                    self.transport.write(line.encode('utf -8'), self.server)
                    break
          
          self.transport.write("users".encode('utf -8'), self.server)

     # def endProtocol(self):
     #      self.transport.write("end".encode("utf -8"), self.server)          
     
     def datagramReceived(self, datagram, addr):

          global connect_flag
          global user_flag
          global recv_flag
          
          # print("hi")
          datagram = datagram.decode('utf-8')      
     
          if connect_flag == 1:
               connect_flag = 0
               port = int(datagram)
               self.address = "127.0.0.1" , port
               reactor.callInThread(self.send_message)
          else:
               if datagram == "__end__":
                    print(self.other_user+" has ended the conversation")
                    reactor.stop()
                    os._exit(0)
               
               if user_flag == 1:
                    user_flag = 0
                    print("Users: ",datagram)
               elif recv_flag == 1:
                    if(datagram.startswith("|msg|")):
                         tot = datagram.split(":")
                         msg = tot[2]
                         tim = tot[1]
                         print(self.other_user, " : ", msg)
                         file = open("text_1_1.txt", "a")
                         #from user1837 to user28372 :::: message
                         line = "Sent at : " + tim + ", Recieved at : " + str(time.time()) +" , msg : " + msg + " , from "+self.name+ " to " +self.other_user+"\n"
                         file.write(line)
                         file.close()
               # print("\n-->",end="")
   
     def send_message(self):
          while True:
               ip = input("--> ") 
               if(ip == "__end__"):
                    self.transport.write("end".encode('utf-8'), self.server)
                    self.transport.write("__end__".encode('utf-8'), self.address)
                    reactor.stop()
                    os._exit(0)

               elif(ip == "__users__"):
                    self.transport.write("users".encode('utf-8'), self.server)
               else:
                    self.transport.write(("|msg|:"+str(time.time()) + ":" + ip).encode('utf-8'), self.address)
                    # file = open("text_1_1.txt", "a")
                    # #from user1837 to user28372 :::: message
                    # line = "from user"+self.name+ " to user" +self.other_user+ " :::: "+str(ip)+"\n"
                    # file.write(line)
                    # file.close()

if __name__ == '__main__' :
     port = randint(1025, 7000)
     reactor.listenUDP(port, Client('localhost', port))
     reactor.run()