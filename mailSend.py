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
    option=input("Select an option: ")
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
            option=input("Select an option: ")


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
        print("Pleae select an options: ")
        print("1. Email a contact")
        print("2. Add a new contact")
        print("3. Edit a contact")
        print("4. Delete a contact")
        print("5. Return to main menu")
        opt=input("\nSelect an option: ")
        if str(opt) == "1":
             sendContact()
        elif str(opt) == "2":
            makeContact()
        elif str(opt) == "3":
            editContact()
        elif str(opt) == "4":
            delContact()
        elif str(opt) == "5":
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
    conFile.writelines(name +" "+adr +"\n")
    conFile.close()
    print("\n---Contact made---")
    print("---Retruning to contact list--")
    viewContacts()


#edit contact
def editContact():
    conFile=open("contacts.txt","r")
    arCon = conFile.readlines()
    conFile.close()
    print("\n---Edit Contact---")

    if len(arCon)==0:
        print("There are no contacts")
        input("---Press any key to return to main menu---")
        mainMenu()
    elif len(arCon) > 0:
        for i in range(len(arCon)):
            print(str(i) + ". "+ arCon[i] )

    conID=input("Enter Contact ID to edit: ")
    print("Enter contact details")
    name=input("Name: ")
    adr=input("Email address: ")
    arCon[int(conID)]=name + " "+ adr+ "\n"
    with open("contacts.txt","w") as file:
        file.writelines(arCon)
    
    print("\n---Contact has been edited---")
    input("---Press any key to return to Contact list---")
    viewContacts()

#delete a contact
def delContact():
    conFile=open("contacts.txt","r")
    arCon = conFile.readlines()
    conFile.close()
    print("\n---Edit Contact---")

    if len(arCon)==0:
        print("There are no contacts")
        input("---Press any key to return to main menu---")
        mainMenu()
    elif len(arCon) > 0:
        for i in range(len(arCon)):
            print(str(i) + ". "+ arCon[i] )

    conID=input("Enter Contact ID to delete: ")
    arCon.pop(int(conID))
    
    
    with open("contacts.txt","w") as file:
        file.writelines(arCon)
    
    print("\n---Contact has been deleted---")
    input("---Press any key to return to Contact list---")
    viewContacts()


#send email to contact 
def sendContact():
    conFile=open("contacts.txt","r")
    arCon = conFile.readlines()
    conFile.close()
    print("\n---Send an Email---")

    if len(arCon)==0:
        print("There are no contacts")
        input("---Press any key to return to main menu---")
        mainMenu()
    elif len(arCon) > 0:
        for i in range(len(arCon)):
            print(str(i) + ". "+ arCon[i] )

    conID=input("Enter Contact ID to edit: ")
    adr=arCon[int(conID)].split()[1]
    print("To: "+adr)
    subject=input("Subject: ")
    body = makeBody()

    print("\n---Email review---\n")
    print("From: "+sender)
    print("To: "+adr)
    print("Subject: "+subject)
    print("Body:")
    print("---Begining of body---\n")
    print(body)
    print("---End of body---")
    rev=input("\nDo you want to send this email[y/n]? ").lower()
    if(rev=="n"):
        print("\n---Canceling email---")
        input("---Press any key to return to main menu---")
        mainMenu()
    elif(rev=="y"):
        print("\n---Sending email---")
        
        #making email
        em = EmailMessage()
        em['From']= sender
        em['To']=adr
        em['Subject']=subject
        em.set_content(body)
        
        #sending email
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(sender, passw)
                smtp.sendmail(sender,adr,em.as_string())
                print("---Email has been sent to "+adr + "---")
                input("---Press any key to return to main menu---")
                mainMenu()
        except:
            print("\n---Something went wrong---")
            print("Ensure the correct details where entered")
            input("---Press any key to return to main menu---")
            mainMenu()



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
    mainMenu()
    
   
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
                input("---Press any key to return to main menu---")
                mainMenu()
        except:
            print("\n---Something went wrong---")
            print("Ensure the correct details where entered")
            input("---Press any key to return to main menu---")
            mainMenu()
    
    input("---Press any key to return to main menu---")
    mainMenu()


mainMenu()

'''
TODO:


= make UI

'''