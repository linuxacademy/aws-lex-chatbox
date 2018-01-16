from messages import detailed_message, alert_help_message


def validate(event,context):
    print('validation event')
    print(event)
    if event['sessionAttributes'] is not None:
        session_attributes = event['sessionAttributes']
    else:
        session_attributes = {}
    slots = event['currentIntent']['slots']
    alert_level = slots['AlertLevel'] or ''
    if alert_level.lower() == 'help':
        print('HELP INVOKED')
        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': event['currentIntent']['name'],
                'slots': slots,
                'slotToElicit': 'AlertLevel',
                'message': {'contentType': 'PlainText', 'content': detailed_message}
            }
        }
    if alert_level.lower() not in ['red', 'orange', 'yellow']:
        print('NOT IN CHOICES')
        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': event['currentIntent']['name'],
                'slots': slots,
                'slotToElicit': 'AlertLevel',
                'message': {'contentType': 'PlainText', 'content': alert_help_message}
            }
        }
    else:
        print('RETURN DELEGATE')
        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Delegate',
                'slots': slots
            }
        }