import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/send_email', methods=['POST'])
def send_email():
    try:

        # data = request.form.to_dict()
        data = request.get_json()
        print("received data", data)
        name = data['name']
        sender_email = data['email']  # User's email from the form
        subject = data['subject']
        message = data['message']


        # # Your form data (replace with actual form data)
        form_data = {
            "value1": name,
            "value2": sender_email,
            "value3": subject + " "+ message
            # ... other form fields ...
        }
        #events: form_submitted and message_received
        event_name = "message_received"  # Replace with the event name you set in IFTTT
        webhooks_key = "kBdefkwd04QKirqRnkC5PHin2n3cYzmbk8enGWjCpWC"  # Replace with your Webhooks service key
        
        webhook_url =f"https://maker.ifttt.com/trigger/{event_name}/with/key/kBdefkwd04QKirqRnkC5PHin2n3cYzmbk8enGWjCpWC"
        # webhook_url = f"https://maker.ifttt.com/trigger/{event_name}/json/with/key/{webhooks_key}"
        # webhook_url = "https://maker.ifttt.com/trigger/{event}/json/with/key/kBdefkwd04QKirqRnkC5PHin2n3cYzmbk8enGWjCpWC"
        headers = {
            "Content-Type": "application/json"
        }
 
    
        print("Triggering the webhook...")
        response = requests.post(webhook_url, json=form_data, headers=headers)
        
        # response = requests.post(webhook_url, json=form_data)
    
        if response.status_code == 200:
            print ("Webhook triggered successfully")
            return ("form submitted successfully")
        else:
            return ("Webhook failed")

   
        
  
    except Exception as e:
        return ("An error occured:", str(e))
        # return jsonify({'An error occurred': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

        # message = Mail(
        #     from_email=sender_email,
        #     to_emails='makaraisabel@gmail.com',  # Your email
        #     subject=subject,
        #     plain_text_content=message)

    #     sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    #     sg.send(message)

    #     return jsonify({'message': 'Email sent successfully'})
 