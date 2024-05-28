import requests
import json
import time
import logging

class NewRelicHandler(logging.Handler):
    """
    Custom logging handler to send logs to New Relic.
    """
    def __init__(self, api_key, url='https://log-api.newrelic.com/log/v1'):
        super().__init__()
        self.api_key = api_key
        self.url = url

    def emit(self, record):
        log_entry = self.format(record)
        timestamp = int(time.time())
        payload = [
            {
                "common": {
                    "attributes": {
                        "logtype": record.log_type,
                        "service": "paper_trading_app",
                        "hostname": record.name,
                        "api_key": record.api_key
                    }
                },
                "logs": [
                    {
                        "timestamp": timestamp,
                        "message": log_entry
                    }
                ]
            }
        ]
        headers = {
            'Content-Type': 'application/json',
            'Api-Key': self.api_key,
            'Accept': '*/*'
        }
        try:
            response = requests.post(self.url, headers=headers, data=json.dumps(payload))
            if response.status_code != 202:
                self.handleError(record)
        except Exception:
            self.handleError(record)
