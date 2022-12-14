from bs4 import BeautifulSoup
import requests.cookies
import json
from Company import Company
from Contact import Contact
from datetime import datetime
import numpy as np


class Parser:
    soup = None
    cookies = None
    list_url = 'https://ati.su/rating/?skip=0&take=20={"PageNumber":%s,"ItemsPerPage":1000,"Geo":{"value":"0_1"}}'
    company_url = 'https://ati.su/Tables/InfoNew.aspx?ID=%s&nrdrt=1&layout=0'
    sid_cookie = ''
    did_cookie = ''

    def __init__(self, repository):
        self.repository = repository

    def parse(self):
        self.get_firm_short_info()
        self.get_firms_info()

    def get_firm_short_info(self):
        i = 1
        while True:
            result = requests.get(self.list_url % i).text
            data = json.loads(result)
            np.save(r'C:\projects\parcer\result\current_time_{}.npy', data)

            for firm in data['data']['firms']:
                company = Company()
                company.remote_id = firm['firm']['id']
                company.name = firm['firm']['mainPartName']
                company.city = firm['firm']['fullCityName']
                company.profile = firm['firm']['profile']

                now = datetime.now()
                # current_time = now.strftime("%H_%M_%S")
                # print("Current Time =", current_time)

                # .to_json(, orient='records')

                # self.repository.save(company)

            if not data['data']['firms']:
                break

            print("Page", i, "have parsed")
            i += 1

    def get_cookies(self):
        if self.cookies is not None:
            return self.cookies

        cookies = requests.cookies.RequestsCookieJar()
        cookies.set('sid', self.sid_cookie, domain='.ati.su', path='/')
        cookies.set('did', self.did_cookie, domain='.ati.su', path='/')
        self.cookies = cookies
        return self.cookies

    def get_firms_info(self):
        for companyDocument in self.repository.find_all(Company.collection()):
            response = requests.get(self.company_url % companyDocument['remote_id'], cookies=self.get_cookies()).text
            self.soup = BeautifulSoup(response, "html.parser")

            company = Company(companyDocument)
            company.inn = self.get_element_by_id("lblINN")
            company.ogrn = self.get_element_by_id("lblOGRN")
            company.country = self.get_element_by_id("lblCountry")
            company.address = self.get_element_by_id("lblAddress")
            if not company.inn:
                company.paid_only = True
            self.repository.save(company)

            self.get_contacts_info(companyDocument)

            print("Company", company.name, "have imported")

    def get_contacts_info(self, document):
        self.repository.delete(Contact.collection(), {"remote_id": document['remote_id']})
        i = 0
        while True:
            if not self.get_element_by_id("rptContact_ctl0" + str(i) + "_lblUserName"):
                break

            contact = Contact()
            contact.remote_id = document['remote_id']
            contact.company_id = document['_id']
            contact.name = self.get_element_by_id("rptContact_ctl0" + str(i) + "_lblUserName")
            contact.phone = self.get_element_by_id("rptContact_ctl0" + str(i) + "_lblPhone", True)
            contact.mobile = self.get_element_by_id("rptContact_ctl0" + str(i) + "_lblMobile", True)
            contact.fax = self.get_element_by_id("rptContact_ctl0" + str(i) + "_lblFax", True)
            contact.icq = self.get_element_by_id("rptContact_ctl0" + str(i) + "_lblICQNumber")
            contact.skype = self.get_element_by_id("rptContact_ctl0" + str(i) + "_lblSkype")
            self.repository.insert(contact)
            i += 1

    def get_element_by_id(self, element_id, with_href=False, tag="span"):
        try:
            element = self.soup.find(tag, {"id": element_id})
            if with_href:
                element = element.find("a")
            if element is None:
                return
            else:
                return element.string
        except AttributeError:
            return None
