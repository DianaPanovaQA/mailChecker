from random import choice
from selenium import webdriver
from mail_page import MailPage

def generate_random_str(len):
    alph_and_num = 'abcdefghijklmnopqrstuvwxyz0123456789'
    output = ''
    for i in range(len):
        output += choice(alph_and_num)
    return output

def send_mails(page, login, count):
    subjects_sent = []
    for i in range(count):
        subject = generate_random_str(10)
        body = generate_random_str(10)
        page.send_message_to(subject, body, login)
        subjects_sent.append(subject)

    mails = page.get_mails_data()
    for mail in mails:
        if mail['subject'] in subjects_sent:
            subjects_sent.remove(mail['subject'])

    if subjects_sent:
        send_mails(page, login, len(subjects_sent))

def make_dict(page):
    message_dict = {}
    mails = page.get_mails_data()
    for mail in mails:
        subject = mail["subject"]
        body = page.get_mail_body(mail["view_link"])
        message_dict[subject] = body    
    return message_dict

def send_report_and_delete_others(message_dict, page, login):
    report_body = ""
    for subject, body in message_dict.items():
        digits = 0
        letters = 0
        for symbol in body:
            if symbol in 'abcdefghijklmnopqrstuvwxyz':
                letters += 1
            elif symbol in '0123456789':
                digits += 1
        report_body += "Received mail on theme " + subject + " with message: " + body + \
                       ".It contains " + str(letters) + " letters and " + str(digits) + " numbers\n"

    page.send_message_to('Report', report_body, login)

    mails = page.get_mails_data()
    for i in range(1, len(mails)):
        page.select_mail(mails[i]["mail_id"])

    page.delete_selected()

driver = webdriver.Chrome()
login = "qa17test@i.ua"
password = "AS123456"
page = MailPage(driver)
page.login(login, password)
send_mails(page, login, 15)
message_dict = make_dict(page)
print(message_dict)
send_report_and_delete_others(message_dict, page, login)
page.close()
