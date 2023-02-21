# Contains the script to constantly comb the SmsAlert table and send alerts when there is a change based on user preferences

# Needs a scheduler
# Needs to connect to the SmsAlert model

# pseudo code

# import scheduler lib
# import SmsAlert model

# define a function to look through the SmsAlert table

# filter for only those users that are opted into sms alerts
# for each of those users, query the locationIQ API to get coordinates
# use those coordinates to get sensor data for that location
# evaluation the AQI of that area


import os
import requests
from .models import SmsAlert
from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
account_sid = os.environ.get("TWILIO_ACCOUNT_SID", "")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "")
twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
location_iq_api_key = "pk.9cf87dc8f1dbe00e1926e39226ed2608" #os.environ.get("LOCATION_IQ_API_KEY")

all_sms_alerts = SmsAlert.objects.all()

@scheduler.scheduled_job('interval', hours=1)
def run_script():
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
    def query_location_iq_api(location):

        url = "https://us1.locationiq.com/v1/search"

        data = {
            'key': location_iq_api_key,
            'q': location,
            'format': 'json'
        }

        response = requests.get(url, params=data)
        print(response.text)
        return response.text
        

    # Query PurpleAir API and get sensor data
    def query_purple_air_api(lat, long):
        # Pass parameters
        # Return latest PM2.5 numbers
        pass

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


    try:
        for alert in all_sms_alerts:
            location = alert.location
            coordinates = query_location_iq_api(location)
            latest_pm_25 = query_purple_air_api(coordinates[0], coordinates[1])
            aqi_level = get_aqi_level(latest_pm_25)

            if aqi_level == alert.previous_air_quality_threshold_alert:
                continue
            else:
                send_alert(alert, aqi_level)
    
    except Exception as e:
        print(e)
scheduler.start()

if __name__ == "__main__":
    print(location_iq_api_key)
    response = query_location_iq_api("Seattle")
    print(response)
