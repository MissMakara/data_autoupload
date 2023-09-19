import requests

def submit_form_to_webhook(form_data):
    webhook_url = "https://maker.ifttt.com/trigger/{event}/json/with/key/kBdefkwd04QKirqRnkC5PHin2n3cYzmbk8enGWjCpWC"
    response = requests.post(webhook_url, json=form_data)
    
    if response.status_code == 200:
        print("Webhook triggered successfully")
    else:
        print("Webhook failed")

# Your form data (replace with actual form data)
form_data = {
    "name": "John Doe",
    "email": "john@example.com",
    # ... other form fields ...
}

submit_form_to_webhook(form_data)