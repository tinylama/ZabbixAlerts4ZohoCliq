#!/usr/bin/env python3
"""
Version:        0.1b
Last Update:    17/02/2023
Description:    Zabbix Alert (Token, Channel, Severity, Subject, Message) ->
                Bash Script to pass arguments to python ->
                Python Script to post data to Zoho Cliq via API

"""

import json
import sys
from datetime import datetime

import requests


def main():
    argument_check()

    # Bot details
    sender_name = "Zabbix"
    sender_image_url = 'https://assets.zabbix.com/img/favicon.ico'

    # Message Theme
    theme = 'modern-inline'

    unique_channel_name = 'zabbix'

    # Zabbix Script Parameters
    # Zabbix Administration -> Media types -> Create media type
    # https://www.zabbix.com/documentation/current/en/manual/config/notifications/media/script
    # https://www.zabbix.com/documentation/current/en/manual/appendix/macros/supported_by_location

    cliq_webhook_token = sys.argv[1]  # Cliq Authentication - https://cliq.zoho.com.au/integrations/webhook-tokens
    unique_channel_name = sys.argv[2]
    severity_number = sys.argv[3]  # {EVENT.NSEVERITY}
    severity = get_severity(severity_number)
    raw_subject = sys.argv[4]  # {ALERT.SUBJECT}
    subject = set_subject(raw_subject, severity)  # Alert Title
    message = sys.argv[5]  # {ALERT.MESSAGE} / Alert Details

    content = generate_alert_message(sender_name, sender_image_url, subject, message, theme)
    send_alert(cliq_webhook_token, unique_channel_name, content)


def argument_check():
    if len(sys.argv) != 5:
        log_file('/var/log/cliq-alerts.txt',
                 'Error: Invalid argument length, ensure script parameters are properly set in Zabbix.')
        exit(1)


def set_subject(subject, severity):
    if severity != '':
        return '[0] {1}'.format(severity, subject)
    else:
        return subject


def get_severity(severity_number):
    if severity_number == 0:
        return ''  # Not classified
    elif severity_number == 1:
        return 'Information'
    elif severity_number == 2:
        return 'Warning'
    elif severity_number == 3:
        return 'Average'
    elif severity_number == 4:
        return 'High'
    elif severity_number == 5:
        return 'Disaster'


def generate_alert_message(sender, image_url, title, alert_content, theme, broadcast='True'):
    # https://cliq.zoho.com/messagebuilder
    return json.dumps({
        "text": alert_content,
        "broadcast": broadcast,  # Broadcast - send message to all the bot subscribers.
        "bot": {
            "name": sender,
            "image": image_url
        },
        "card": {
            "title": title,
            "theme": theme
        }
    })


def log_file(file_name, content):
    timestamp = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    with open(file_name, 'a+', encoding='utf-8') as log:
        log.write('[{0}] {1}'.format(timestamp, content))


def send_alert(token, channel, content):
    # https://www.zoho.com/cliq/help/restapi/v2/#Post_Message_Channel
    url = 'https://cliq.zoho.com.au/api/v2/channelsbyname/{0}/message?zapikey={1}'.format(channel, token)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, headers=headers, data=content)

    # https://www.zoho.com/cliq/help/restapi/v2/#Errors
    if not response.ok:
        log_file('/var/log/cliq-alerts.txt',
                 'Response: ({0}) {1} | Alert: {2}\n'.format(response.status_code, response.text.rstrip(), content))


if __name__ == '__main__':
    main()
