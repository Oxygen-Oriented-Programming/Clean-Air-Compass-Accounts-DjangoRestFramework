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
from .models import SmsAlert

all_sms_alerts = SmsAlert.objects.all()
# do stuff

# def send_alert(self):
    
#     # Get the user's phone number
#     phone_number = self.user.phone_number
    
#     # Construct the message
#     message = f"Air quality in {self.location} is now {self.air_quality_direction.to_lower()} {self.air_quality_threshold}."
    
#     # Send the message using Twilio or another SMS service
#     account_sid = os.environ.get("TWILIO_ACCOUNT_SID", "")
#     auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "")
#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#         body=message,
#         from_= os.environ.get("TWILIO_PHONE_NUMBER", ""),
#         to=phone_number
#     )
#     return message.sid
