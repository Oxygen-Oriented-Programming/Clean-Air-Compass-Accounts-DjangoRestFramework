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
        to=f"+1{phone_number}"
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
    levels = {
        (0, 6.0): ("Good Low", "Air quality is deemed acceptable and presents minimal hazard."),
        (6.0, 12.0): ("Good High", "Individuals who are sensitive should refrain from outdoor activities to prevent respiratory symptoms from occurring."),
        (12.0, 23.0): ("Moderate Low", "Sensitive individuals, as well as the general public, face the possibility of encountering respiratory issues and irritation."),
        (23.0, 33.0): ("Moderate High", "The general public is more likely to experience negative impacts and further strain on their heart and lungs."),
        (33.0, 41.0): ("Unhealthy for Sensitive Groups, Low", "The impact on the general public will be significant, and vulnerable individuals should limit their outdoor activities."),
        (41.0, 55.0): ("Unhealthy for Sensitive Groups, High", "The general public is highly susceptible to experiencing severe irritations and negative health impacts and is advised to refrain from engaging in outdoor activities."),
        (55.0, 155.0): ("Unhealthy", "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."),
        (155.0, 250.0): ("Very Unhealthy", "Health warnings of emergency conditions. The entire population is more likely to be affected."),
        (250.5, float('inf')): ("Hazardous", "Health alert: everyone may experience more serious health effects. Avoid outdoor activities.")
    }

    for (lower, upper), (label, message) in levels.items():
        if lower <= pm_25 <= upper:
            return (label, message)

def run_script():
    try:
        
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
