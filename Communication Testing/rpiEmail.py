import smtplib
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("darwinrpi13@gmail.com", "Darwin2017")
 
msg = "YOUR MESSAGE!"
server.sendmail("darwinrpi13@gmail.com", "reilyblackner@gmail.com", msg)
server.quit()