# from https://docs.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-common-schema-definitions

import json
from types import SimpleNamespace

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

def map_alert_to_channel(alert, channel_definition, rules=default_rules):
    channel_names = [channel.name for channel in channel_definition.channels]
    for rule in rules:
        channel_proposal = rule(alert)
        if channel_proposal in channel_names:
            return channel_proposal
    raise Exception("No channel found for alert {}".format(alert))
