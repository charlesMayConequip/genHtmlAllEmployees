import xmlrpc.client as xmlrpclib
import base64
import os
from myVars import *
import datetime as DT
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from slugify import slugify

common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')

uid = common_proxy.login(DB,USER,PASS)
models = xmlrpclib.ServerProxy('{}2/object'.format(url))

# SHOW ALL INFO ABOUT THE MODEL THAT WE ARE PULLING FROM
print(models.execute_kw(DB, uid, PASS, 'hr.employee', 'fields_get', [], {'attributes': ['string', 'help', 'type']}))

# GET ALL DATA FROM ODOO
allData = models.execute_kw(DB, uid, PASS, 'hr.employee', 'search_read', [[['name', '!=', ['Benjamin Krentz', 'Albert Alexander', 'Ryan Loos']]]], {'fields': ['name', 'work_phone', 'department_id', 'job_id', 'job_title', 'work_phone', 'mobile_phone', 'work_email', 'image_256', 'x_studio_exclude_from_website']})

# CONVERT ALL PHOTOS
removeMe = []
for photo in allData:
    with open((f"./photos/{photo['name']}.jpg").replace(" ", "-").lower(), "wb") as fh:
        try:
            fh.write(base64.b64decode((photo['image_256'])))
        except:
            removeMe.append((f"./photos/{photo['name']}.jpg").replace(" ", "-").lower())

for remove in removeMe:
    os.remove(remove)

for idx, person in enumerate(allData):
    if 'x_studio_exclude_from_website' in person:
        if person['x_studio_exclude_from_website'] == True:
            del allData[idx]

# SHOW ALL DEPARTMENTS
departments = []
for department in allData:
    if department['name'] == "Kevin Collier":
        print(department['department_id'][0])
    if department['department_id'][1] not in departments:
        departments.append(department['department_id'][1])

print(departments)

# GENERATE HTML CODE
myHtml.append('<p>At ConEquip, we are proud of the team that we have put together. We strive to be sure that our parts specialists arealways available tolocate the heavy equipment parts that you need. To meet our customer needs, we have teams that are here to handleyour parts requests.Whether it is our fantastic office manager, a parts specialist, or a sales assistant, everyone at ConEquip is welltrained and ready tomeet your needs and exceed your expectations. With former operators on staff, we have a unique understanding of yourequipment that youwon"t find with everyone in the parts industry.</p><div class="divider">&nbsp;</div><div class="text-center pb-5"><h2 class="red">We Are Hiring!</h2><h5>Are you looking for a career in the construction equipment parts business? Contact us today.</h5><h2><a href="{{store url="employment/"}}" class="p-4"><u>Jobs at ConEquip</u></a></h2></div><div class="col-12 col-sm-6"><h2 class="section-title pt-5">Partners</h2><hr /></div><!-- START 3 COLUMN GRID FOUNDERS--><div class="row ctr pt-5"><div class="col-4"> <a href="{{store url="al-alexander"}}"><img class="fade-on-hover border marg10 img-dshadow" src="{{media url="wysiwyg/conequip/employees/al.jpg"}}" alt="Albert Alexander" /></a><h6 class="above-heading ">President / Partner</h6><h3 class="blu">Albert Alexander</h3><p class="d-none d-sm-block">Al is the co-founder of ConEquip and is the friendly voice that many of you areusedto. Al started ConEquip with his business partner Ben and in 2008 and it has been growing ever since.</p><a class="go" href="{{store url="al-alexander"}}">More about Al</a> </div><div class="col-4"> <a href="{{store url="ben-krentz"}}"><img class="fade-on-hover border marg10 img-dshadow" src="{{media url="wysiwyg/conequip/employees/ben.jpg"}}" alt="Ben Krentz - ConEquip" /></a><h6 class="above-heading">Vice-President / Partner</h6><h3 class="blu">Ben Krentz</h3><p class="d-none d-sm-block">Ben Krentz, Co-owner and Sales Manager here at ConEquip Parts. We started thiscompanyin 2008 and have great plans in store for the future...</p><a class="go" href="{{store url="ben-krentz"}}">More about Ben</a> </div><div class="col-4"> <a href="{{store url="ryan-loos"}}"><img class="fade-on-hover border marg10 img-dshadow" src="{{media url="wysiwyg/conequip/employees/ryan.jpg"}}" alt="Ryan Loos - CFO at ConEquip Parts" /></a><h6 class="above-heading ">Chief Financial Officer / Partner</h6><h3 class="blu">Ryan Loos</h3><p class="d-none d-sm-block">Ryan Loos is the CFO at ConEquip Parts. Many in WNY already know Ryan from hisaccounting practice. Ryan brings awealth of accounting and business knowledge to ConEquip.</p><a class="go" href="{{store url="ryan-loos"}}">More about Ryan</a> </div></div>')
myHtml.append("<div>")
myHtml.append('<div class="col-12 col-sm-6"><h2 class="section-title pt-5">Parts Specialists</h2><hr /></div>')
myHtml.append('<div class="row ctr pt-5">')
counter = 0
for person in allData:
    if not (person['department_id'][0] == 2 and person['image_256']):
        continue
    if counter % 6 == 0 and counter != 0:
        myHtml.append('</div><div class="row ctr pt-5">')
    if person['department_id'][0] == 2 and person['image_256']:
        myHtml.append(f'<a href="{{{{store url="{slugify(person["name"])}/"}}}}">')
        myHtml.append(f'<div class="pb-3 col-6 col-sm-4 col-md-3 col-lg-2 filter bunarske">')
        myHtml.append(f'<img class="fade-on-hover border marg10" src="{{{{media url="wysiwyg/conequip/employees/2022/{person["name"].replace(" ", "-").lower()}.jpg"}}}}" alt="{person["name"]} of Conequip" />')
        myHtml.append(f'<h6 class="above-heading">{person["job_title"]}</h6>')
        myHtml.append(f'<h3 class="blu">{person["name"]}</h3>')
        myHtml.append(f'<a href="tel:{person["work_phone"]}">{person["work_phone"]}</a>')
        myHtml.append('</div></a>')
        counter += 1
myHtml.append('</div>')

myHtml.append('<div class="col-12 col-sm-6"><h2 class="section-title pt-5">Human Resources</h2><hr /></div>')
myHtml.append('<div class="row ctr pt-5">')
counter = 0
for person in allData:
    if not (person['department_id'][0] == 11 and person['image_256']):
        continue
    if counter % 6 == 0 and counter != 0:
        myHtml.append('</div><div class="row ctr pt-5">')
    if person['department_id'][0] == 11 and person['image_256']:
        myHtml.append('<div class="pb-3 col-6 col-sm-4 col-md-3 col-lg-2 filter bunarske">')
        myHtml.append(f'<img class="fade-on-hover border marg10" src="{{{{media url="wysiwyg/conequip/employees/2022/{person["name"].replace(" ", "-").lower()}.jpg"}}}}" alt="{person["name"]} of Conequip" />')
        myHtml.append(f'<h6 class="above-heading">{person["job_title"]}</h6>')
        myHtml.append(f'<h3 class="blu">{person["name"]}</h3>')
        myHtml.append(f'<a href="tel:{person["work_phone"]}">{person["work_phone"]}</a>')
        myHtml.append('</div>')
        counter += 1
myHtml.append('</div>')


myHtml.append('<div class="col-12 col-sm-6"><h2 class="section-title pt-5">TLC (Tracking, Logistics, Customer Service)</h2><hr /></div>')
myHtml.append('<div class="row ctr pt-5">')
counter = 0
for person in allData:
    if not (person['department_id'][0] == 7 and person['image_256']):
        continue
    if counter % 6 == 0 and counter != 0:
        myHtml.append('</div><div class="row ctr pt-5">')
    if person['department_id'][0] == 7 and person['image_256']:
        myHtml.append('<div class="pb-3 col-6 col-sm-4 col-md-3 col-lg-2 filter bunarske">')
        myHtml.append(f'<img class="fade-on-hover border marg10" src="{{{{media url="wysiwyg/conequip/employees/2022/{person["name"].replace(" ", "-").lower()}.jpg"}}}}" alt="{person["name"]} of Conequip" />')
        myHtml.append(f'<h6 class="above-heading">{person["job_title"]}</h6>')
        myHtml.append(f'<h3 class="blu">{person["name"]}</h3>')
        myHtml.append(f'<a href="tel:{person["work_phone"]}">{person["work_phone"]}</a>')
        myHtml.append('</div>')
        counter += 1
myHtml.append('</div>')


myHtml.append('<div class="col-12 col-sm-6"><h2 class="section-title pt-5">Parts Trainers</h2><hr /></div>')
myHtml.append('<div class="row ctr pt-5">')
counter = 0
for person in allData:
    if not (person['department_id'][0] == 5 and person['image_256']):
        continue
    if counter % 6 == 0 and counter != 0:
        myHtml.append('</div><div class="row ctr pt-5">')
    if person['department_id'][0] == 5 and person['image_256']:
        myHtml.append('<div class="pb-3 col-6 col-sm-4 col-md-3 col-lg-2 filter bunarske">')
        myHtml.append(f'<img class="fade-on-hover border marg10" src="{{{{media url="wysiwyg/conequip/employees/2022/{person["name"].replace(" ", "-").lower()}.jpg"}}}}" alt="{person["name"]} of Conequip" />')
        myHtml.append(f'<h6 class="above-heading">{person["job_title"]}</h6>')
        myHtml.append(f'<h3 class="blu">{person["name"]}</h3>')
        myHtml.append(f'<a href="tel:{person["work_phone"]}">{person["work_phone"]}</a>')
        myHtml.append('</div>')
        counter += 1
myHtml.append('</div>')

myHtml.append('<div class="col-12 col-sm-6"><h2 class="section-title pt-5">PRO Team</h2><hr /></div>')
myHtml.append('<div class="row ctr pt-5">')
counter = 0
for person in allData:
    if not ((person['department_id'][0] == 16) and person['image_256']):
        continue
    if counter % 6 == 0 and counter != 0:
        myHtml.append('</div><div class="row ctr pt-5">')
    if (person['department_id'][0] == 16) and person['image_256']:
        myHtml.append('<div class="pb-3 col-6 col-sm-4 col-md-3 col-lg-2 filter bunarske">')
        myHtml.append(f'<img class="fade-on-hover border marg10" src="{{{{media url="wysiwyg/conequip/employees/2022/{person["name"].replace(" ", "-").lower()}.jpg"}}}}" alt="{person["name"]} of Conequip" />')
        myHtml.append(f'<h6 class="above-heading">{person["job_title"]}</h6>')
        myHtml.append(f'<h3 class="blu">{person["name"]}</h3>')
        myHtml.append(f'<a href="tel:{person["work_phone"]}">{person["work_phone"]}</a>')
        myHtml.append('</div>')
        counter += 1
myHtml.append('</div>')

myHtml.append('<div class="col-12 col-sm-6"><h3 class="section-title pt-5">Processing</h3></div>')
myHtml.append('<div class="row ctr pt-5">')
counter = 0
for person in allData:
    if not ((person['department_id'][0] == 26) and person['image_256']):
        continue
    if counter % 6 == 0 and counter != 0:
        myHtml.append('</div><div class="row ctr pt-5">')
    if (person['department_id'][0] == 26) and person['image_256']:
        myHtml.append('<div class="pb-3 col-6 col-sm-4 col-md-3 col-lg-2 filter bunarske">')
        myHtml.append(f'<img class="fade-on-hover border marg10" src="{{{{media url="wysiwyg/conequip/employees/2022/{person["name"].replace(" ", "-").lower()}.jpg"}}}}" alt="{person["name"]} of Conequip" />')
        myHtml.append(f'<h6 class="above-heading">{person["job_title"]}</h6>')
        myHtml.append(f'<h3 class="blu">{person["name"]}</h3>')
        myHtml.append(f'<a href="tel:{person["work_phone"]}">{person["work_phone"]}</a>')
        myHtml.append('</div>')
        counter += 1
myHtml.append('</div>')



myHtml.append('<div class="col-12 col-sm-6"><h3 class="section-title pt-5">Returns</h3></div>')
myHtml.append('<div class="row ctr pt-5">')
counter = 0
for person in allData:
    if not ((person['department_id'][0] == 28 or person['department_id'][0] == 27) and person['image_256']):
        continue
    if counter % 6 == 0 and counter != 0:
        myHtml.append('</div><div class="row ctr pt-5">')
    if (person['department_id'][0] == 28 or person['department_id'][0] == 27) and person['image_256']:
        myHtml.append('<div class="pb-3 col-6 col-sm-4 col-md-3 col-lg-2 filter bunarske">')
        myHtml.append(f'<img class="fade-on-hover border marg10" src="{{{{media url="wysiwyg/conequip/employees/2022/{person["name"].replace(" ", "-").lower()}.jpg"}}}}" alt="{person["name"]} of Conequip" />')
        myHtml.append(f'<h6 class="above-heading">{person["job_title"]}</h6>')
        myHtml.append(f'<h3 class="blu">{person["name"]}</h3>')
        myHtml.append(f'<a href="tel:{person["work_phone"]}">{person["work_phone"]}</a>')
        myHtml.append('</div>')
        counter += 1
myHtml.append('</div>')


myHtml.append('<div class="col-12 col-sm-6"><h2 class="section-title pt-5">FOM</h2><hr /></div>')
myHtml.append('<div class="row ctr pt-5">')
counter = 0
for person in allData:
    if not ((person['department_id'][0] == 9) and person['image_256']):
        continue
    if counter % 6 == 0 and counter != 0:
        myHtml.append('</div><div class="row ctr pt-5">')
    if (person['department_id'][0] == 9) and person['image_256']:
        myHtml.append('<div class="pb-3 col-6 col-sm-4 col-md-3 col-lg-2 filter bunarske">')
        myHtml.append(f'<img class="fade-on-hover border marg10" src="{{{{media url="wysiwyg/conequip/employees/2022/{person["name"].replace(" ", "-").lower()}.jpg"}}}}" alt="{person["name"]} of Conequip" />')
        myHtml.append(f'<h6 class="above-heading">{person["job_title"]}</h6>')
        myHtml.append(f'<h3 class="blu">{person["name"]}</h3>')
        myHtml.append(f'<a href="tel:{person["work_phone"]}">{person["work_phone"]}</a>')
        myHtml.append('</div>')
        counter += 1
myHtml.append('</div>')



myHtml.append('<div class="col-12 col-sm-6"><h2 class="section-title pt-5">Accounting</h2><hr /></div>')
myHtml.append('<div class="row ctr pt-5">')
counter = 0
for person in allData:
    if not ((person['department_id'][0] == 6) and person['image_256']):
        continue
    if counter % 6 == 0 and counter != 0:
        myHtml.append('</div><div class="row ctr pt-5">')
    if (person['department_id'][0] == 28 or person['department_id'][0] == 27 or person['department_id'][0] == 6) and person['image_256']:
        myHtml.append('<div class="pb-3 col-6 col-sm-4 col-md-3 col-lg-2 filter bunarske">')
        myHtml.append(f'<img class="fade-on-hover border marg10" src="{{{{media url="wysiwyg/conequip/employees/2022/{person["name"].replace(" ", "-").lower()}.jpg"}}}}" alt="{person["name"]} of Conequip" />')
        myHtml.append(f'<h6 class="above-heading">{person["job_title"]}</h6>')
        myHtml.append(f'<h3 class="blu">{person["name"]}</h3>')
        myHtml.append(f'<a href="tel:{person["work_phone"]}">{person["work_phone"]}</a>')
        myHtml.append('</div>')
        counter += 1
myHtml.append('</div>')


myHtml.append('<div class="col-12 col-sm-6"><h2 class="section-title pt-5">Reception</h2><hr /></div>')
myHtml.append('<div class="row ctr pt-5">')
counter = 0
for person in allData:
    if not (person['department_id'][0] == 8 and person['image_256']):
        continue
    if counter % 6 == 0 and counter != 0:
        myHtml.append('</div><div class="row ctr pt-5">')
    if person['department_id'][0] == 8 and person['image_256']:
        myHtml.append('<div class="pb-3 col-6 col-sm-4 col-md-3 col-lg-2 filter bunarske">')
        myHtml.append(f'<img class="fade-on-hover border marg10" src="{{{{media url="wysiwyg/conequip/employees/2022/{person["name"].replace(" ", "-").lower()}.jpg"}}}}" alt="{person["name"]} of Conequip" />')
        myHtml.append(f'<h6 class="above-heading">{person["job_title"]}</h6>')
        myHtml.append(f'<h3 class="blu">{person["name"]}</h3>')
        myHtml.append(f'<a href="tel:{person["work_phone"]}">{person["work_phone"]}</a>')
        myHtml.append('</div>')
        counter += 1
myHtml.append('</div>')


myHtml.append('<div class="col-12 col-sm-6"><h2 class="section-title pt-5">Marketing</h2><hr /></div>')
myHtml.append('<div class="row ctr pt-5">')
counter = 0
for person in allData:
    if not (person['department_id'][0] == 4 and person['image_256']):
        continue
    if counter % 6 == 0 and counter != 0:
        myHtml.append('</div><div class="row ctr pt-5">')
    if person['department_id'][0] == 4 and person['image_256']:
        myHtml.append('<div class="pb-3 col-6 col-sm-4 col-md-3 col-lg-2 filter bunarske">')
        myHtml.append(f'<img class="fade-on-hover border marg10" src="{{{{media url="wysiwyg/conequip/employees/2022/{person["name"].replace(" ", "-").lower()}.jpg"}}}}" alt="{person["name"]} of Conequip" />')
        myHtml.append(f'<h6 class="above-heading">{person["job_title"]}</h6>')
        myHtml.append(f'<h3 class="blu">{person["name"]}</h3>')
        myHtml.append(f'<a href="tel:{person["work_phone"]}">{person["work_phone"]}</a>')
        myHtml.append('</div>')
        counter += 1
myHtml.append('</div>')



myHtml.append('<div class="col-12 col-sm-6"><h2 class="section-title pt-5">E-Commerce, IT, Development</h2><hr /></div>')
myHtml.append('<div class="row ctr pt-5">')
counter = 0
for person in allData:
    if not (person['department_id'][0] == 3 and person['image_256']):
        continue
    if counter % 6 == 0 and counter != 0:
        myHtml.append('</div><div class="row ctr pt-5">')
    if person['department_id'][0] == 3 and person['image_256']:
        myHtml.append('<div class="pb-3 col-6 col-sm-4 col-md-3 col-lg-2 filter bunarske">')
        myHtml.append(f'<img class="fade-on-hover border marg10" src="{{{{media url="wysiwyg/conequip/employees/2022/{person["name"].replace(" ", "-").lower()}.jpg"}}}}" alt="{person["name"]} of Conequip" />')
        myHtml.append(f'<h6 class="above-heading">{person["job_title"]}</h6>')
        myHtml.append(f'<h3 class="blu">{person["name"]}</h3>')
        myHtml.append(f'<a href="tel:{person["work_phone"]}">{person["work_phone"]}</a>')
        myHtml.append('</div>')
        counter += 1
myHtml.append('</div>')


myHtml.append("</div>")

myHtml.append('<hr /><div class="ctr pt-5 pb-3"><h5>Are you looking for a career in the construction equipment parts business? Contact us today.</h5><h2><a href="{{store url="employment/"}}" class="p-4"><u>Jobs at ConEquip</u></a></h2></div>')
# OUTPUT HTML CODE INTO SEPERATE FOLDERS BASED ON DEPARTMENT
# SNIP FOR MAIN PAGE AND SNIP FOR WHOLE ABOUT PAGE
dateToday = DT.date.today().strftime("%m-%d-%Y")

f = open(f'{dateToday}_markup.html', "w")
f.writelines(myHtml)

import shutil

shutil.make_archive(f'{dateToday}_photos', 'zip', 'photos')

mail_attachment = [f'{dateToday}_markup.html', f'{dateToday}_photos.zip']
mail_attachment_name = [f'{dateToday}_markup.html', f'{dateToday}_photos.zip']

print("Sending Email..")
dateLastWeek = (DT.date.today() - DT.timedelta(days=7)).strftime("%m-%d-%Y")
mail_body = f"Audience changes from {dateLastWeek} to {dateToday}"
mimemsg = MIMEMultipart()
mimemsg['From'] = mail_from
mimemsg['To'] = mail_to
mimemsg['Subject'] = mail_subject
mimemsg['Cc'] = ','.join(mail_CC)
mimemsg.attach(MIMEText(mail_body, 'plain'))

for idx, file in enumerate(mail_attachment):
    with open(mail_attachment[idx], "rb") as attachment:
        mimefile = MIMEBase('application', 'octet-stream')
        mimefile.set_payload(attachment.read())
        encoders.encode_base64(mimefile)
        mimefile.add_header('Content-Disposition', "attachment; filename= %s" % mail_attachment_name[idx])
        mimemsg.attach(mimefile)

connection = smtplib.SMTP(host='smtp.office365.com', port=587)
connection.starttls()
connection.login(email_username, email_password)
connection.send_message(mimemsg)
connection.quit()