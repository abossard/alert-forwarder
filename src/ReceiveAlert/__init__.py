import logging
from ReceiveAlert.alert_forwarder import handle_request_body, parse_channel_definition

import azure.functions as func

defaultChannelDefinitions = parse_channel_definition("""{
  "channels": [
    {"name": "Critical", "webhook": "https://hooks.slack.com/services/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"},
    {"name": "Warning", "webhook": "https://hooks.slack.com/services/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"},
    {"name": "Information", "webhook": "https://hooks.slack.com/services/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"}
  ]
}""")

def main(req: func.HttpRequest) -> func.HttpResponse:
  try:
    logging.info('Python HTTP trigger function processed a request.')
    req_body = req.get_body().decode('utf-8')
    logging.info(f'Received request with body: {req_body}')
    result = handle_request_body(req_body, defaultChannelDefinitions)
    logging.info(f'Result: {result}')
    return func.HttpResponse(
            f"Sents {len(result)} messages",
            status_code=200
    )
  except Exception as e:
    logging.error(f'Error: {e}')
    return func.HttpResponse(f"Error: {e}", status_code=500)
