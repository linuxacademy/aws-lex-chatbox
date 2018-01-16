import boto3

ses = boto3.client('ses')
sns = boto3.client('sns')

# In sandbox mode, SES requires senders and recipients to have verified emails
VERIFIED_EMAIL = 'your.email@yourprovider.com'

# Phone numbers must included the plus and country code
PHONE_NUMBER = '+1###3334444'

# Option to add verified emails to each alert type
RED_ALERT_EMAILS = [VERIFIED_EMAIL, ]
ORANGE_ALERT_EMAILS = [VERIFIED_EMAIL, ]
YELLOW_ALERT_EMAILS = [VERIFIED_EMAIL, ]

# Option to add phone numbers to each alert type
RED_ALERT_PHONE_NUMBERS = [PHONE_NUMBER, ]
ORANGE_ALERT_PHONE_NUMBERS = [PHONE_NUMBER, ]


def send_email_alerts(to_addresses, alert_level):
    ses.send_email(
        Source=VERIFIED_EMAIL,
        Destination={
            'ToAddresses': to_addresses
        },
        Message={
            'Subject': {
                'Data': alert_level + ' alert!',
            },
            'Body': {
                'Text': {
                    'Data': 'A ' + alert_level + ' alert was reported via Slack'
                }
            }
        }
    )


def send_sms_alerts(numbers, alert_level):
    for number in numbers:
        sns.publish(
            PhoneNumber=number,
            Message=alert_level+' alert triggered from Slack!'
        )


def send_alerts(level):
    print("Runing an alerting playbook of email and (sometimes) text alerts")
    if level.lower() in ['red', 'orange', 'yellow']:
        print('Running the ' + level + ' Alert runbook!')
        if level.lower() == 'red':
            send_email_alerts(RED_ALERT_EMAILS, 'Red')
            send_sms_alerts(RED_ALERT_PHONE_NUMBERS, 'Red')
        if level.lower() == 'orange':
            send_email_alerts(ORANGE_ALERT_EMAILS, 'Orange')
            send_sms_alerts(ORANGE_ALERT_PHONE_NUMBERS, 'Orange')
        if level.lower() == 'yellow':
            send_email_alerts(YELLOW_ALERT_EMAILS, 'Yellow')
    else:
        print('Alert level not recognized - alert aborted')
