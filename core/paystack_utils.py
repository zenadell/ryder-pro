import requests
from django.conf import settings

def paystack_charge_card(email, amount_usd, card_dict):
    """
    Initiates a card charge on Paystack using the raw Charge API.
    amount_usd should be a float or decimal. It will be converted to cents.
    Returns: (status_code, payload)
    status_code: 
      - "success" (fully paid)
      - "send_otp" (OTP required)
      - "send_pin" (PIN required)
      - "send_phone" (Phone number required)
      - "send_birthday" (Birthday required)
      - "failed" (error occurred)
    payload: dict containing reference, message, etc.
    """
    url = "https://api.paystack.co/charge"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "email": email,
        "amount": str(int(float(amount_usd) * 100)),
        "card": {
            "cvv": card_dict.get('cvv'),
            "number": card_dict.get('number'),
            "expiry_month": str(card_dict.get('exp_month')).zfill(2),
            "expiry_year": str(card_dict.get('exp_year'))[-2:]
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        res_data = response.json()
        
        if res_data.get('status') is True:
            r_data = res_data.get('data', {})
            status = r_data.get('status')
            if status == 'success':
                return "success", {"reference": r_data.get('reference'), "message": res_data.get('message')}
            elif status in ['send_otp', 'send_pin', 'send_phone', 'send_birthday']:
                return status, {"reference": r_data.get('reference'), "message": res_data.get('message')}
            elif status == 'failed':
                return "failed", {"message": res_data.get('message', 'Payment failed.')}
            else:
                return "failed", {"message": f"Unknown status: {status}"}
        else:
            return "failed", {"message": res_data.get('message', 'Payment request failed.')}
    except Exception as e:
        return "failed", {"message": f"Network or server error: {str(e)}"}

def paystack_submit_otp(reference, otp):
    """
    Submits the OTP for a pending Paystack charge.
    Returns: (is_success, message)
    """
    url = "https://api.paystack.co/charge/submit_otp"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "otp": otp,
        "reference": reference
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        res_data = response.json()
        
        if res_data.get('status') is True:
            r_data = res_data.get('data', {})
            status = r_data.get('status')
            if status == 'success':
                return True, res_data.get('message')
            else:
                return False, res_data.get('message', 'OTP verification did not return success.')
        else:
            return False, res_data.get('message', 'Failed to verify OTP.')
    except Exception as e:
        return False, f"Network or server error: {str(e)}"
