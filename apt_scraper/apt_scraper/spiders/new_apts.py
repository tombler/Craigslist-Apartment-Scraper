import scrapy
import json
import sys
import smtplib
from datetime import datetime

base_url = 'https://losangeles.craigslist.org'
results_file = 'searched.json'
log_file = 'log.txt'

class NewAptsSpider(scrapy.Spider):
    name = "new_apts"
    start_urls = ['https://losangeles.craigslist.org/search/apa?sort=date&search_distance=6&postal=90034&max_price=2100&availabilityMode=0&pets_cat=1']

    def log(self, content):
        with open(log_file, 'a') as f:
            f.write(str(content))
            f.write('\n')
            f.close()

    def parse(self, response):
        self.log("Starting search at %s" % datetime.now())

        this_search = []

        with open(results_file, 'r') as data_file:    
            searched_apts = json.load(data_file)['urls']

        for url in response.xpath('//a[contains(@class, "result-title")]/@href').extract():
            if url not in searched_apts:
                this_search.append(str(url))

        updated_search = searched_apts + this_search
        
        if len(this_search) > 0:
            self.log("New apts found:")
            self.log(this_search)

            with open(results_file, 'w') as data_file:
                json.dump({"urls": updated_search}, data_file)

            self.send_email(this_search)

        else:
            self.log("No new apartments found.")

    def send_email(self,this_search):
        to = self.settings['MAIL_TO']
        cc = []
        subject = "New apartments found on Craigslist"
        email_content = "New apartments on Craigslist:\n\n"
        for item in this_search:
            email_content += base_url + item
            email_content += "\n"
        mailer = scrapy.mail.MailSender.from_settings(self.settings)
        mailer.send(to=to,subject=subject,body=email_content)

