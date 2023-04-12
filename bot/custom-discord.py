#!/usr/bin/env python3
# Copyright (C) 2015, Wazuh Inc.
# March 13, 2018.
#
# This program is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation.

import json
import sys
import time
import os

try:
    import requests
    from requests.auth import HTTPBasicAuth
except Exception as e:
    print("No module 'requests' found. Install: pip install requests")
    sys.exit(1)

# ossec.conf configuration:
#  <integration>
#      <name>slack</name>
#      <hook_url>https://hooks.slack.com/services/XXXXXXXXXXXXXX</hook_url>
#      <alert_format>json</alert_format>
#  </integration>

# Global vars

debug_enabled = True
pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
json_alert = {}
now = time.strftime("%a %b %d %H:%M:%S %Z %Y")

# Set paths
log_file = '{0}/logs/integrations.log'.format(pwd)


def main(args):
    debug("# Starting")

    # Read args
    alert_file_location = args[1]
    webhook = args[3]

    debug("# Webhook")
    debug(webhook)

    debug("# File location")
    debug(alert_file_location)

    # Load alert. Parse JSON object.
    with open(alert_file_location) as alert_file:
        json_alert = json.load(alert_file)
    debug("# Processing alert")
    debug(json_alert)

    debug("# Generating message")
    msg = generate_msg(json_alert)
    debug(msg)

    debug("# Sending message")
    send_msg(msg, webhook)


def debug(msg):
    if debug_enabled:
        msg = "{0}: {1}\n".format(now, msg)
        print(msg)
        f = open(log_file, "a")
        f.write(msg)
        f.close()


def generate_msg(alert):
	#save the rule level
    level = alert['rule']['level']
    #compare rules level to set colors of the alert
    if (level <= 4):
    	#green
        color = "3731970"
    elif (level >= 5 and level <= 12):
        #yellow
        color = "15919874"
    else:
        #red
        color = "15870466"

    if 'agentless' in alert:
        agent_ = 'agentless'
    else:
        agent_ = alert['agent']['name']
    #data that the webhook will receive and use to display the alert in discord chat
    payload = json.dumps({
      "embeds": [
        {
          "title": "Wazuh Alert - Rule {}".format(alert['rule']['id']),
          "color": "{}".format(color),
          "description": "{}".format(alert['rule']['description']),
          "fields": [
            {
              "name": "Agent",
              "value": "{}".format(agent_),
              "inline": True
            },
            {
              "name": "Location",
              "value": "{}".format(alert['location']),
              "inline": True
            },
            {
            "name": "Rule Level",
            "value": "{}".format(alert['rule']['level']),
            "inline": True
            }
          ]
        }
      ]
    })

    return payload


def send_msg(msg, url):
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    res = requests.post(url, data=msg, headers=headers)
    debug(res)


if __name__ == "__main__":
    try:
        # Read arguments
        bad_arguments = False
        if len(sys.argv) >= 4:
            msg = '{0} {1} {2} {3} {4}'.format(
                now,
                sys.argv[1],
                sys.argv[2],
                sys.argv[3],
                sys.argv[4] if len(sys.argv) > 4 else '',
            )
            debug_enabled = (len(sys.argv) > 4 and sys.argv[4] == 'debug')
        else:
            msg = '{0} Wrong arguments'.format(now)
            bad_arguments = True

        # Logging the call
        f = open(log_file, 'a')
        f.write(msg + '\n')
        f.close()

        if bad_arguments:
            debug("# Exiting: Bad arguments.")
            sys.exit(1)

        # Main function
        main(sys.argv)

    except Exception as e:
        debug(str(e))
        raise
