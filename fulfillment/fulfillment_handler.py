import alerts


def handler(event, context):
    print('fulfillment event:')
    print(event)
    alert_type = event['currentIntent']['slots']['AlertLevel']
    print(alert_type)

    alert_response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": (
                    "Thanks, I have started the configured "
                    "alerting procedures for a {0} Alert."
                ).format(alert_type)
            }
        }
    }
    alerts.send_alerts(alert_type)
    return alert_response
