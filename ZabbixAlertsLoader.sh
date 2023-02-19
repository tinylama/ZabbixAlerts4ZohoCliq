#!/bin/bash

# Store in AlertScriptsPath (/usr/local/share/zabbix/alertscripts)
# https://www.zabbix.com/documentation/current/en/manual/appendix/config/zabbix_server

./ZabbixAlertSender.py "$1" "$2" "$3" "$4" "$5"


# Zabbix Administration -> Media types -> Create media type

# Zabbix Parameters
# cliq_webhook_token = Argument 1 i.e. "1000.123345..." - https://cliq.zoho.com.au/integrations/webhook-tokens
# unique_channel_name = Argument 2 i.e "Zabbix"
# severity_number = Argument 3 is {EVENT.NSEVERITY}
# subject = Argument 4 is {ALERT.SUBJECT}
# message = Argument 5 is {ALERT.MESSAGE} / Alert Details
