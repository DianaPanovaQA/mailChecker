from urllib3.util import parse_url
from base_page import BasePage

class MailPage(BasePage):
    def return_to_main(self):
        self.load_page("https://mbox2.i.ua/list/INBOX")

    def send_message_to(self, subject, body, to):
        self.element_click("//p[@class='make_message']")
        self.element_send_keys("//span/textarea[@name='to']", to)
        self.element_send_keys("//span/input[@name='subject']", subject)
        self.element_send_keys("//div/textarea[@name='body']", body)
        self.element_click("//p/input[@name='send']")
        self.return_to_main()

    def get_mails_data(self):
        data = []
        links_elements_list = self.find_elements_by_xpath("//*[@id='mesgList']/form/div/a")
        for link_element in links_elements_list:
            view_link = link_element.get_attribute("href")
            link_parsed = parse_url(view_link)
            mail_id = link_parsed.path[12:][:-1]
            data.append({
                "mail_id": mail_id,
                "view_link": view_link,
                "subject": link_element.find_element_by_xpath("./span[@class='sbj']/span").text,
                "select_checkbox": self.find_element_by_xpath(f"//input[@value='" + mail_id + "'and@type='checkbox']"),
            })
        return data

    def get_mail_body(self, link):
        self.load_page(link)
        body = self.find_element_by_xpath("/html/body/div[1]/div[6]/div[2]/div[2]/ul/li/div[1]/div/div[3]/pre").text
        return body.split("\n")[0]

    def select_mail(self, mail_id):
        self.element_click(f"//input[@value='" + mail_id + "'and@type='checkbox']")

    def login(self, login, password):
        self.load_page('https://www.i.ua/')
        self.element_send_keys("//input[@name='login']", login)
        self.element_send_keys("//input[@name='pass']", password)
        self.element_click("/html/body/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/form/p/input")

    def delete_selected(self):
        self.element_click("//span[@buttonname='del']")
        self.accept_alert()
