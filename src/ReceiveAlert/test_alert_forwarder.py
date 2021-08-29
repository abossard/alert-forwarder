# allow discovery and relative pythonpath
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from alert_forwarder import parse_alert,  extract_channel_override, parse_channel_definition, map_alert_to_channels, create_slack_message, send_slack_message, handle_request_body
import unittest

examplePayload = """{
  "schemaId": "azureMonitorCommonAlertSchema",
  "data": {
    "essentials": {
      "alertId": "/subscriptions/<subscription ID>/providers/Microsoft.AlertsManagement/alerts/b9569717-bc32-442f-add5-83a997729330",
      "alertRule": "WCUS-R2-Gen2",
      "severity": "Sev3",
      "signalType": "Metric",
      "monitorCondition": "Resolved",
      "monitoringService": "Platform",
      "alertTargetIDs": [
        "/subscriptions/<subscription ID>/resourcegroups/pipelinealertrg/providers/microsoft.compute/virtualmachines/wcus-r2-gen2"
      ],
      "configurationItems": [
        "wcus-r2-gen2"
      ],
      "originAlertId": "3f2d4487-b0fc-4125-8bd5-7ad17384221e_PipeLineAlertRG_microsoft.insights_metricAlerts_WCUS-R2-Gen2_-117781227",
      "firedDateTime": "2019-03-22T13:58:24.3713213Z",
      "resolvedDateTime": "2019-03-22T14:03:16.2246313Z",
      "description": "",
      "essentialsVersion": "1.0",
      "alertContextVersion": "1.0"
    },
    "alertContext": {
      "properties": null,
      "conditionType": "SingleResourceMultipleMetricCriteria",
      "condition": {
        "windowSize": "PT5M",
        "allOf": [
          {
            "metricName": "Percentage CPU",
            "metricNamespace": "Microsoft.Compute/virtualMachines",
            "operator": "GreaterThan",
            "threshold": "25",
            "timeAggregation": "Average",
            "dimensions": [
              {
                "name": "ResourceId",
                "value": "3efad9dc-3d50-4eac-9c87-8b3fd6f97e4e"
              }
            ],
            "metricValue": 7.727
          }
        ]
      }
    }
  }
}"""


exampleChannelDefinition = """{
  "channels": [
    {"name": "Critical", "webhook": "https://hooks.slack.com/services/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"},
    {"name": "Warning", "webhook": "https://hooks.slack.com/services/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"},
    {"name": "Information", "webhook": "https://hooks.slack.com/services/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"}
  ]
}"""

class TestAlertForwarder(unittest.TestCase):

    def test_can_parse_schema(self):
      result = parse_alert(examplePayload)
      self.assertEqual(result.schemaId, "azureMonitorCommonAlertSchema")

    def test_can_parse_channel_definitions(self):
      result = parse_channel_definition(exampleChannelDefinition)
      self.assertEqual(result.channels[0].name, "Critical")

    def test_channel_override(self):
      alert = parse_alert(examplePayload)
      result = extract_channel_override(alert)
      self.assertEqual(result, "Gen2")

    def test_default_rules(self):
      alert = parse_alert(examplePayload)
      result = map_alert_to_channels(alert, parse_channel_definition(exampleChannelDefinition))
      self.assertEqual(result[0].name, "Warning")
    
    def test_create_slack_message(self):
      alert = parse_alert(examplePayload)
      result = create_slack_message(alert)
      self.assertIn(alert.data.essentials.severity, result["blocks"][0]["text"]["text"])

    def test_send_slack_message(self):
      message = create_slack_message(parse_alert(examplePayload))
      result = send_slack_message(message, "https://hooks.slack.com/services/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")
      self.assertEqual(result.status_code, 200)


    def test_handle_request_body(self):
      result = handle_request_body(examplePayload, parse_channel_definition(exampleChannelDefinition))
      self.assertEqual(result[0].status_code, 200)

if __name__ == '__main__':
    unittest.main()
