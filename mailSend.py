import smtplib
from email.message import EmailMessage
import ssl

#get password via a text file
passFile =open("passw.txt","r")
passw = passFile.read(16)
passFile.close()

#test email: dev.sk.testing@gmail.com
sender = 'stiaandev@gmail.com'
receiver = input("\nTo: ").lower()

#function to make body
def makeBody():
    print("\n---Enter '--x' in a new line to stop typing---\n") 
    txt = ""
    while True:
        line = input()
        if(line == "--x"):
            return txt
            break
        else:
            txt += (line +"\n")

#make email
subject = input("Subject: ")
body = makeBody()
em = EmailMessage()
em['From']= sender
em['To']=receiver
em['Subject']=subject
em.set_content(body)

#email review:
print("\n---Email review---\n")
print("From: "+sender)
print("To: "+receiver)
print("Subject: "+subject)
print("Body:")
print("---Begining of body---\n")
print(body)
print("---End of body---")
rev=input("\nDo you want to send this email[y/n]? ").lower()
if(rev=="n"):
    print("\n---Canceling email---")
elif(rev=="y"):
    print("\n---Sending email---")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(sender, passw)
        smtp.sendmail(sender,receiver,em.as_string())

    print("---Email has been sent to "+receiver + "---")



