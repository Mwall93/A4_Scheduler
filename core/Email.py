import requests
import os.path
import json
from string import Template
from core import Config

# Methods for this file:
# Get email template (tuple of html and text template)
# Send email
def getTemplate(name):
    """ Return a list of the HTML and Text Email Templates """
    if os.path.isfile(os.path.join(os.path.dirname(__file__), '../email_templates/' + name + '.txt')) and os.path.isfile(os.path.join(os.path.dirname(__file__), '../email_template/' + name + '.html')):
        with open(os.path.join(os.path.dirname(__file__), '../email_templates/' + name + '.txt')) as txtFile:
            txtTemplate = txtFile.read()

        with open(os.path.join(os.path.dirname(__file__), '../email_templates/' + name + '.html')) as htmlFile:
            htmlTemplate = htmlFile.read()

        # Get the subject
        with open(os.path.join(os.path.dirname(__file__), '../email_templates/email_templates.json')) as jsonFile:
            jsonData = jsonFile.read().replace('\n', '')
        
        subjects = json.loads(jsonData)

        subject = 'A4 Scheduler'

        if name in subjects:
            subject = subjects[name]

        return [htmlTemplate, txtTemplate, subject]
    else:
        raise ValueError('Template file does not exist.')
    


    return name, name, name

def renderTemplate(templateList, props):
    """ Renders a the HTML and Text emails given the variables """
    # See: https://stackoverflow.com/a/6385940
    templateList[0] = Template(templateList[0]).substitute(props)
    templateList[1] = Template(templateList[1]).substitute(props)
    templateList[2] = Template(templateList[2]).substitute(props)

    return templateList

def sendEmail(recipient, template, vars = {}):
    # Get template, render it then send it using the Mailgun API
    # See: http://docs.python-requests.org/en/master/
    # See: https://documentation.mailgun.com/en/latest/api-sending.html#sending (ignore mime example)

    email = renderTemplate(getTemplate(template), vars)
    
    apiResponse = requests.post(
        'https://api.mailgun.net/v3/mg.a4scheduler.xyz/messages', 
        auth=('api', Config.getValue('MAILGUN_API_KEY')),
        data={
            'from': 'A4 Scheduler <system@a4scheduler.xyz>',
            'to': recipient,
            'subject': email[2],
            'text': email[1],
            'html': email[0]
        }
    )

    return