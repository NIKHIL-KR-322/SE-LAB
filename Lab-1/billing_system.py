"""Subscription billing system (Lab 5, cleaned up after static analysis).

Handles free trials, plan subscriptions, coupons, billing dates, upgrade
proration, payment retries, refunds, card encryption, signed XML webhooks
and HTML invoices.
"""
import calendar
import hashlib
import hmac
import os
import secrets
from datetime import date

import defusedxml.ElementTree as safe_etree
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from mako.template import Template

PLANS = {"basic": 199, "pro": 499, "team": 999}
GST = 0.18
TRIAL_DAYS = 14
MAX_ATTEMPTS = 3
PERIOD_DAYS = 30
COUPON_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

# Secrets come from the environment, never from source code.  A random
# value is generated for the demo when the variables are not set.
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET") or secrets.token_hex(16)
CARD_KEY = (os.environ.get("CARD_KEY") or secrets.token_hex(8)).encode()
# AES-128 needs a 16-byte key; the key above is exactly 16 bytes.

subscriptions = {}
coupons = {
    "WELCOME10": {"percent": 10, "expires": date(2026, 12, 31)},
    "FRIENDS150": {"percent": 150, "expires": date(2027, 1, 31)},
}


def subscribe(user, plan, start):
    """Create a trial subscription for ``user`` and return it."""
    if plan not in PLANS:
        raise ValueError(f"Unknown plan: {plan}")
    subscriptions[user] = {
        "plan": plan,
        "start": start,
        "status": "trial",
        "invoices": [],
    }
    return subscriptions[user]


def is_trial_over(user, today):
    """Return True once the trial period has fully elapsed."""
    return (today - subscriptions[user]["start"]).days >= TRIAL_DAYS


def apply_coupon(amount, code, today):
    """Apply a coupon; the discount is capped at 100% (never negative)."""
    coupon = coupons.get(code)
    if coupon is None:
        return amount
    if today > coupon["expires"]:
        return amount
    percent = min(max(coupon["percent"], 0), 100)
    return amount - amount * percent / 100


def invoice_amount(user, code=None, today=None):
    """Return the GST-inclusive invoice total, rounded to 2 decimals."""
    today = today or date.today()
    plan_price = PLANS[subscriptions[user]["plan"]]
    with_tax = plan_price * (1 + GST)
    return round(apply_coupon(with_tax, code, today), 2)


def next_billing_date(current):
    """Return the same day next month (clamped to the month's last day)."""
    year = current.year + current.month // 12
    month = current.month % 12 + 1
    last_day = calendar.monthrange(year, month)[1]
    return current.replace(year=year, month=month,
                           day=min(current.day, last_day))


def prorate_upgrade(user, new_plan, today, period_end):
    """Charge the price difference for the days left in the period."""
    old = PLANS[subscriptions[user]["plan"]]
    new = PLANS[new_plan]
    days_left = max((period_end - today).days, 0)
    days_in_period = calendar.monthrange(period_end.year,
                                         period_end.month)[1]
    subscriptions[user]["plan"] = new_plan
    return round((new - old) * days_left / days_in_period, 2)


def retry_payment(charge):
    """Call ``charge`` up to MAX_ATTEMPTS times; return attempts used."""
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        attempts += 1
        if charge():
            break
    return attempts


def cancel_refund(user, days_used):
    """Refund the unused part of the billing period."""
    if not 0 <= days_used <= PERIOD_DAYS:
        raise ValueError("days_used must be between 0 and 30")
    price = PLANS[subscriptions[user]["plan"]]
    refund = round(price * (PERIOD_DAYS - days_used) / PERIOD_DAYS, 2)
    print("Refund for", days_used, "days used:", refund)
    return refund


def coupon_code():
    """Generate an unpredictable coupon code."""
    return "SAVE-" + "".join(secrets.choice(COUPON_ALPHABET)
                             for _ in range(6))


def active_users():
    """Return users that have no invoices yet."""
    return {user for user, sub in subscriptions.items()
            if not sub["invoices"]}


def encrypt_card(card_number):
    """Encrypt a card number with AES-GCM and a fresh random nonce."""
    nonce = secrets.token_bytes(12)
    ciphertext = AESGCM(CARD_KEY).encrypt(nonce, card_number.encode(), None)
    return (nonce + ciphertext).hex()


def sign_webhook(body):
    """Return the HMAC-SHA256 signature of a webhook body."""
    return hmac.new(WEBHOOK_SECRET.encode(), body,
                    hashlib.sha256).hexdigest()


def verify_webhook(body, signature):
    """Check a webhook signature using a constant-time comparison."""
    return hmac.compare_digest(sign_webhook(body), signature)


def parse_webhook(xml_bytes):
    """Parse webhook XML safely (defusedxml blocks XXE and entity bombs)."""
    root = safe_etree.fromstring(xml_bytes)
    return {"event": root.findtext("event"), "user": root.findtext("user")}


def render_invoice(user, amount):
    """Render an HTML invoice; all values are HTML-escaped."""
    if amount < 0:
        raise ValueError("amount must not be negative")
    template = Template(  # nosec B702 - default_filters=["h"] escapes input
        "<h1>Invoice for ${user}</h1><p>Total: Rs.${amount}</p>",
        default_filters=["h"],
    )
    return template.render(user=user, amount=amount)


def main():
    """Run a short demo of the billing system."""
    subscribe("asha", "pro", date(2026, 9, 1))
    subscribe("<b onmouseover=alert(1)>ravi</b>", "basic", date(2026, 9, 20))
    print("Trial (14 days from 09-01) over on 09-15?",
          is_trial_over("asha", date(2026, 9, 15)))
    print("Pro invoice with WELCOME10:",
          invoice_amount("asha", "WELCOME10", date(2026, 10, 1)))
    print("Pro invoice with FRIENDS150:",
          invoice_amount("asha", "FRIENDS150", date(2026, 10, 1)))
    print("Coupon on its expiry day:",
          invoice_amount("asha", "WELCOME10", date(2026, 12, 31)))
    print("Next billing after 2026-10-15:",
          next_billing_date(date(2026, 10, 15)))
    print("Next billing after 2026-01-31:",
          next_billing_date(date(2026, 1, 31)))
    print("Upgrade pro->team with 10 days left in Feb:",
          prorate_upgrade("asha", "team", date(2027, 2, 18),
                          date(2027, 2, 28)))
    print("Payment attempts (max 3, always failing):",
          retry_payment(lambda: False))
    print("Refund after using 25 of 30 days:", cancel_refund("asha", 25))
    print("Same card, same ciphertext?",
          encrypt_card("4111111111111111")
          == encrypt_card("4111111111111111"))
    sig = sign_webhook(b"<x/>")
    print("Webhook verified:", verify_webhook(b"<x/>", sig))
    print("Webhook:", parse_webhook(
        b"<hook><event>paid</event><user>asha</user></hook>"))
    print("Invoice HTML:",
          render_invoice("<b onmouseover=alert(1)>ravi</b>", 199))
    print("Coupon:", coupon_code())


if __name__ == "__main__":
    main()
