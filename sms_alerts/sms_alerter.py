import requests
from django.conf import settings
from .models import SmsAlert
from twilio.rest import Client
# from apscheduler.schedulers.background import BackgroundScheduler

# scheduler = BackgroundScheduler()
account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
twilio_phone_number = settings.TWILIO_PHONE_NUMBER
all_sms_alerts = SmsAlert.objects.all()

def send_alert(alert, aqi_level):
    
    # Get the user's phone number
    phone_number = alert.phone_number
    
    # Construct the message
    message = f"Air quality in {alert.location} is now {aqi_level}."
    
    # Send the message using Twilio or another SMS service

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_= twilio_phone_number ,
        to=phone_number
    )
    return message.sid

# Query LocationIQ API and get lat/long
def query_fast_api(location):

    url = f"https://dolphin-app-ebj76.ondigitalocean.app/average_pollution/{location.lower()}"

    response = requests.get(url)
    
    return response.json()
    

# Get AQI Level
def get_aqi_level(pm_25):
    if pm_25 <= 12.0:
        return "Good"
    elif pm_25 >12.0 and pm_25 <= 35.4:
        return "Moderate"
    elif pm_25 >35.4 and pm_25 <= 55.4:
        return "Unhealthy for Sensitive Groups"
    elif pm_25 >55.4 and pm_25 <= 150.4:
        return "Unhealthy"
    elif pm_25 >150.4 and pm_25 <= 250.4:
        return "Very Unhealthy"
    else:
        return "Hazardous"

def run_script():
    try:
        
        for alert in all_sms_alerts:
            print(alert)
            location = alert.location
            latest_pm_25 = query_fast_api(location)
            aqi_level = get_aqi_level(latest_pm_25)

            if aqi_level == alert.previous_air_quality_threshold_alert:
                continue
            else:
                send_alert(alert, aqi_level)
    
    except Exception as e:
        print(e)
