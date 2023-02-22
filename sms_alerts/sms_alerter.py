import requests
from textwrap import dedent
from django.conf import settings
from .models import SmsAlert
from twilio.rest import Client

account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
twilio_phone_number = settings.TWILIO_PHONE_NUMBER
all_sms_alerts = SmsAlert.objects.all()

def send_alert(alert, aqi_level):
    print("Preparing Message")
    # Get the user's phone number
    phone_number = alert.phone_number
    
    # Construct the message
    message = dedent(f"""
        Air quality in {alert.location} is now {aqi_level[0]}.
        {aqi_level[1]}
    """)
    
    # Send the message using Twilio or another SMS service

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_= twilio_phone_number ,
        to=phone_number
    )
    print("Message Sent")
    return message.sid

# Query LocationIQ API and get lat/long
def query_fast_api(location):

    url = f"https://dolphin-app-ebj76.ondigitalocean.app/average_pollution/{location.lower()}"

    response = requests.get(url)
    
    return response.json()
    

# Get AQI Level
def get_aqi_level(pm_25):
    if pm_25 <= 12.0:
        return ("Good", "Air quality is satisfactory and poses little or no risk.")
    elif pm_25 >12.0 and pm_25 <= 35.4:
        return ("Moderate", "Sensitive individuals should avoid outdoor activity.")
    elif pm_25 >35.4 and pm_25 <= 55.4:
        return ("Unhealthy for Sensitive Groups", "General public and sensitive individuals in particular are at risk of respiratory problems.")
    elif pm_25 >55.4 and pm_25 <= 150.4:
        return ("Unhealthy", "Increased likelihood of adverse effects to heart and lungs among the general public.")
    elif pm_25 >150.4 and pm_25 <= 250.4:
        return ("Very Unhealthy", "General public will be noticeably affected. Restrict outdoor activities.")
    else:
        return ("Hazardous", "General public at high risk of strong adverse affect to heart and lungs. Avoid outdoor activities.")

def run_script():
    try:
        print('starting run_script')
        for alert in all_sms_alerts:
            print(alert)
            print(alert.previous_air_quality_threshold_alert)
            location = alert.location
            latest_pm_25 = query_fast_api(location)
            aqi_level = get_aqi_level(latest_pm_25)
            print(aqi_level, alert.previous_air_quality_threshold_alert)
            if aqi_level != alert.previous_air_quality_threshold_alert:
                print("Updating AQI in database")
                alert.previous_air_quality_threshold_alert = aqi_level
                alert.save()

                print("sending message")
                send_alert(alert, aqi_level)
                print("message sent")
            print("next alert")
    
    except Exception as e:
        print(e)
