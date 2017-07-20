import scrapy
import json
from datetime import datetime

class NewAptsSpider(scrapy.Spider):
    name = "new_apts"
    start_urls = ['https://losangeles.craigslist.org/search/apa?sort=date&search_distance=5&postal=90034&max_price=2100&min_bedrooms=1&max_bedrooms=1&availabilityMode=0&pets_cat=1']

    def log(self, content):
        with open(self.settings['CUSTOM_LOG_FILE'], 'a') as f:
            f.write(str(content))
            f.write('\n')
            f.close()

    def parse(self, response):
        self.log("Starting search at %s" % datetime.now())

        this_search = []

        with open(self.settings['RESULTS_FILE'], 'r') as data_file:    
            searched_apts = json.load(data_file)['urls']

        for url in response.xpath('//a[contains(@class, "result-title")]/@href').extract():
            if url not in searched_apts:
                this_search.append(str(url))

        updated_search = searched_apts + this_search
        
        if len(this_search) > 0:
            self.log("New apts found:")
            self.log(this_search)

            with open(self.settings['RESULTS_FILE'], 'w') as data_file:
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
            email_content += self.settings['BASE_URL'] + item
            email_content += "\n"
        mailer = scrapy.mail.MailSender.from_settings(self.settings)
        mailer.send(to=to,subject=subject,body=email_content,cc=self.settings['MAIL_CC'])

