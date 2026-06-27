import pandas as pd
import random


tickets = [

    ("Customer cannot login after password reset", "Account Access"),

    ("User forgot password and cannot access account", "Account Access"),

    ("Account locked after multiple failed attempts", "Account Access"),

    ("Payment failed but money was deducted", "Payment Issue"),

    ("Refund has not reached bank account", "Payment Issue"),

    ("Credit card payment is not going through", "Payment Issue"),

    ("Internet connection is very slow", "Network Issue"),

    ("WiFi keeps disconnecting", "Network Issue"),

    ("VPN connection is failing", "Network Issue"),

    ("Application crashes when opening", "Technical Issue"),

    ("System shows unexpected error message", "Technical Issue"),

    ("Software is running very slowly", "Technical Issue"),

    ("Laptop screen is not turning on", "Hardware Issue"),

    ("Keyboard keys stopped working", "Hardware Issue"),

    ("Battery is draining quickly", "Hardware Issue"),

    ("New update broke the application", "Software Bug"),

    ("Feature is not working correctly", "Software Bug"),

    ("Application throws server error", "Software Bug"),

    ("Subscription renewal failed", "Subscription"),

    ("Need to upgrade subscription plan", "Subscription"),

    ("Cannot cancel my subscription", "Subscription"),

    ("Order has not arrived yet", "Delivery Issue"),

    ("Package delivered to wrong address", "Delivery Issue"),

    ("Need tracking information", "Delivery Issue"),

    ("Suspicious login detected", "Security Issue"),

    ("Account activity looks unusual", "Security Issue"),

    ("Need help changing security settings", "Security Issue"),

    ("Need help with product information", "General Support"),

    ("Customer has a general question", "General Support"),

]


data = []


for i in range(200):

    ticket, category = random.choice(tickets)

    data.append({
        "ticket_id": i + 1,
        "ticket": ticket,
        "expected_category": category
    })


df = pd.DataFrame(data)


df.to_csv(
    "data/tickets.csv",
    index=False
)


print("200 tickets created")