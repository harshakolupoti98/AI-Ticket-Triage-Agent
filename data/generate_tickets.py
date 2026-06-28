import pandas as pd
import random

NUM_TICKETS = 120

TEMPLATES = {
    "Authentication Issue": [
        "User cannot log in after resetting password.",
        "Invalid session token prevents login.",
        "MFA code not received.",
        "Login page refreshes after sign in.",
        "Password reset link expired.",
    ],
    "Account Access": [
        "Account locked after failed attempts.",
        "User cannot access profile.",
        "Role assignment missing after onboarding.",
        "Account disabled unexpectedly.",
        "Shared account inaccessible.",
    ],
    "Performance Issue": [
        "Dashboard loads very slowly.",
        "Reports take too long to generate.",
        "Application freezes during peak hours.",
        "Search response is delayed.",
        "High CPU usage causes lag.",
    ],
    "Application Bug": [
        "Save button throws unknown error.",
        "App crashes when opening settings.",
        "Export feature fails.",
        "Search returns incorrect results.",
        "File upload ends with exception.",
    ],
    "Notification Issue": [
        "Email alerts not received.",
        "Push notifications stopped working.",
        "SMS OTP delayed.",
        "Reminder emails missing.",
        "Approval notifications fail.",
    ],
    "Data Issue": [
        "Report totals are incorrect.",
        "Customer records missing.",
        "Duplicate entries created.",
        "Recent updates not visible.",
        "Dashboard shows stale data.",
    ],
    "Integration Issue": [
        "CRM sync failed.",
        "ERP integration timeout.",
        "Payment gateway authentication failed.",
        "Webhook not triggering.",
        "API returns 500 error.",
    ],
    "UI Issue": [
        "Button not clickable.",
        "Layout broken on mobile.",
        "Text overlaps on dashboard.",
        "Dark mode icons invisible.",
        "Dropdown not opening.",
    ],
    "Permission Issue": [
        "Manager cannot approve requests.",
        "Admin page access denied.",
        "User cannot edit records.",
        "Role permissions missing.",
        "Access denied after promotion.",
    ],
    "Security Issue": [
        "Suspicious login detected.",
        "Possible phishing email reported.",
        "Unknown device accessed account.",
        "Unexpected password change.",
        "Security alert triggered.",
    ],
}


def generate_ticket():
    category = random.choice(list(TEMPLATES.keys()))
    ticket = random.choice(TEMPLATES[category])
    return ticket, category

rows = []

for i in range(1, NUM_TICKETS + 1):
    ticket, category = generate_ticket()
    rows.append({
        "ticket_id": i,
        "ticket": ticket,
        "expected_category": category
    })

random.shuffle(rows)

for i, row in enumerate(rows, start=1):
    row["ticket_id"] = i

df = pd.DataFrame(rows)
df.to_csv("data/tickets.csv", index=False)

print(f"{NUM_TICKETS} tickets created successfully.")
