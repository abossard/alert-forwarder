# from https://docs.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-common-schema-definitions

import json
from types import SimpleNamespace
import requests

def parse_json(json_payload):
    return json.loads(json_payload, object_hook=lambda d: SimpleNamespace(**d))


def parse_alert(json_payload):
    return parse_json(json_payload)


def parse_channel_definition(json_payload):
    return parse_json(json_payload)


def default_to(level):
    return lambda alert: level


def extract_channel_override(alert):
    return alert.data.essentials.alertRule.split('-')[-1]


default_rules = [
    extract_channel_override,
    default_to("Warning")
]


def map_alert_to_channels(alert, channel_definition, rules=default_rules):
    channel_names = [channel.name for channel in channel_definition.channels]
    for rule in rules:
        channel_proposal = rule(alert)
        if channel_proposal in channel_names:
            return [channel for channel in channel_definition.channels if channel.name == channel_proposal]
    raise Exception("No channel found for alert {}".format(alert))

# from https://app.slack.com/block-kit-builder/
def create_slack_message(alert):
    return {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{alert.data.essentials.severity}* ({alert.data.essentials.signalType}): {alert.data.essentials.alertRule}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Type:*\nComputer (laptop)"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*When:*\nSubmitted Aut 10"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Last Update:*\nMar 10, 2015 (3 years, 5 months)"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Reason:*\nAll vowel keys aren't working."
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Specs:*\n\"Cheetah Pro 15\" - Fast, really fast\""
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Approve"
                        },
                        "style": "primary",
                        "value": "click_me_123"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Deny"
                        },
                        "style": "danger",
                        "value": "click_me_123"
                    }
                ]
            }
        ]
    }

def send_slack_message(message, webhook):
    return requests.post(webhook, data=json.dumps(message), headers={'Content-Type': 'application/json'})

def handle_request_body(body_json, channel_definition, rules=default_rules):
    alert = parse_alert(body_json)
    channels = map_alert_to_channels(alert, channel_definition, rules)
    message = create_slack_message(alert)
    return [send_slack_message(message, channel.webhook) for channel in channels]

