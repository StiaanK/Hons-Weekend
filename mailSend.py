import smtplib
from email.message import EmailMessage
import ssl
import imaplib
import email
import email.contentmanager
import sys

#get password via a text file
passFile =open("passw.txt","r")
passw = passFile.read(16)
passFile.close()


#test sender email: stiaandev@gmail.com
#test reciever email: dev.sk.testing@gmail.com
sender = 'stiaandev@gmail.com'


#main menu options
def mainMenu():
    print("\n---Welcome to nuMail---")
    print("\nPlease select an option:")
    print("1. Send an email")
    print("2. Check emails")
    print("3. View Contacts")
    print("4. Exit")
    option=input("Select an options: ")
    while True:
        if(option == "1"):
            sendEmail()
            break
        elif(option == "2"):
            checkEmail()
        elif(option == "3"):
            viewContacts()
            break
        elif(option == "4"):
            print("\n---Exiting nuMail---")
            print("---Have a nice day!---\n")
            sys.exit()
        else:
            print("Please choose a valid option!")
            option=input("Select an options: ")


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


#view contacts 
def viewContacts():
    print("\n---Viewing Contacts---")
    conFile=open("contacts.txt","r")
    arCon=conFile.readlines()
    if len(arCon)==0:
        print("There are no contacts")
        opt=input("\nWould you like to add a new contact[y/n]? ")
        if opt == "y":
            makeContact()
        else:
            print("\n---Returning to main menu---")
            mainMenu()
    elif len(arCon) > 0:
        for i in range(len(arCon)):
            print(str(i) + ". "+ arCon[i] )
        
        opt=input("\nWould you like to add a new contact[y/n]? ")
        if opt == "y":
            makeContact()
        else:
            print("\n---Returning to main menu---")
            mainMenu()
    conFile.close()
   
#make new contact   
def makeContact():
    conFile=open("contacts.txt","a")
    print("\n---Make an contact---")
    print("Enter contact details")
    name=input("Name: ")
    adr=input("Email address: ")
    conFile.writelines(name +" "+adr +" \n")
    conFile.close()
    print("\n---Contact made---")
    print("---Retruning to contact list--")
    viewContacts()



#check email
def checkEmail():
    #making connection
    imap_server = "imap.gmail.com"
    imap =imaplib.IMAP4_SSL(imap_server)
    imap.login(sender, passw)

    #selcting mailbox
    imap.select("Inbox") 

    _, msgnums = imap.search(None, "ALL")
    

    #print((msgnums[0].split())[0])
    print("\nRecieved emails:")
    #displaying emails
    for msgnum in  reversed(msgnums[0].split()):
        _, data =imap.fetch(msgnum, "RFC822")
        

        
        mess = email.message_from_bytes(data[0][1])

        print("====================================================================================================")
        print(f"Email nr: {msgnum}" )
        print(f"From: {mess.get('From')}")
        print(f"Subject: {mess.get('Subject')}")
        #print(f"Body: {mess.get_payload(decode=True).decode()}")
        print("====================================================================================================")
        print("\n")
    input("---Press any key to retrun to main menu")
    
   
#send email
def sendEmail():
    #make email
    receiver = input("\nTo: ").lower()
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
        
        #sending email
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(sender, passw)
                smtp.sendmail(sender,receiver,em.as_string())
                print("---Email has been sent to "+receiver + "---")
        except:
            print("\n---Something went wrong---")
            print("Ensure the correct details where entered")
            input("---Press any key to return to main menu---")
            mainMenu()
    
    print("---Returning to main menu---")
    mainMenu()


mainMenu()

'''
TODO:
- edit contact
- send mail to contact

'''

