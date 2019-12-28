import poplib
import email
import os.path, os
from email.header import decode_header, make_header
import time




class GetMailAttach(object):
    def __init__(self,server,user,password,savedir):

        self.connection = poplib.POP3(server, 110)
        self.connection.set_debuglevel(1)
        self.connection.user(user)
        self.connection.pass_(password)


        self.savedir=savedir

        self.save_attach_to_local_directory()        

    def save_attach_to_local_directory(self):
        
        emails, total_bytes = self.connection.stat()
        print("{0} emails in the inbox, {1} bytes total".format(emails, total_bytes))
        msg_list = self.connection.list()
        print(msg_list)
        self.savedir=self.savedir+time.strftime("/%Y/%m/%d/%H..%M/")
        os.makedirs(self.savedir, exist_ok=True)
        for i in range(emails):
  
            response = self.connection.retr(i+1)
            raw_message = response[1]
            str_message = email.message_from_bytes(b'\n'.join(raw_message))
            fromTxt= str(make_header(decode_header(str_message["From"]))).replace('"', '').replace(' ', '_')
            fromTxt=fromTxt[fromTxt.find("<")+1:fromTxt.find(">")]

            tmpSubdir=self.savedir+fromTxt
            os.makedirs(tmpSubdir, exist_ok=True)
        

            for part in str_message.walk():
                print(part.get_content_type())
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    print("no content dispo")
                    continue

                filename = part.get_filename()
                if decode_header(filename)[0][1] is not None:
                    filename = decode_header(filename)[0][0].decode(decode_header(filename)[0][1])
                if not(filename): filename = "bad_filename.txt"
                print(filename)
         
                fp = open(os.path.join(tmpSubdir, filename), 'wb')
                fp.write(part.get_payload(decode=1))
                fp.close
            self.connection.dele(i+1)
        self.connection.quit()

      
        
        
    

GetMailAttach(server="pop3 server addres", user=" name of user", password="password of user",savedir="place of save")
