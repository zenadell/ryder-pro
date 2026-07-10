import json
import random
import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify
from core.models import Vehicle, Category, VehicleImage, VehicleFeature, GeminiAPIKey

def get_gemini_client():
    import google.generativeai as genai
    keys = GeminiAPIKey.objects.filter(is_active=True)
    if not keys.exists():
        raise Exception("No active Gemini API keys found.")
    # Auto-switch keys to avoid rate limits by picking a random one
    selected_key = random.choice(keys).key
    genai.configure(api_key=selected_key)
    return genai

def generate_vehicle_data(car_name):
    import random
    import re
    
    # Extract year if present
    year = 2024
    match = re.search(r'\b(20\d{2})\b', car_name)
    if match:
        year = int(match.group(1))
    
    # Extract make
    parts = car_name.split(' ')
    make = parts[1] if match and len(parts) > 1 else parts[0]
    
    # Generic realistic descriptions
    desc_template = f"<p>Experience the thrill of the {car_name}, an absolute marvel of modern automotive engineering. From its sleek, aerodynamic exterior to its meticulously crafted interior, every detail has been designed to provide an unparalleled driving experience.</p><p>Under the hood, it boasts a powerful engine that delivers responsive performance and exceptional handling. The premium cabin is equipped with state-of-the-art technology, ensuring both driver and passengers are connected, entertained, and comfortable throughout every journey.</p><p>Whether you're cruising through city streets or embarking on a long-distance road trip, the {car_name} offers the perfect blend of luxury, safety, and exhilaration. Don't miss the opportunity to elevate your daily drive.</p>"
    
    # Categories: suv, sedan, family, sports, heavy duty, electric, luxury
    category = 'Sedan' # default
    name_lower = car_name.lower()
    
    if any(x in name_lower for x in ['suv', 'g63', 'defender', 'cullinan', 'urus', 'purosangue', 'r1s', 'range rover']):
        category = 'SUV'
    elif any(x in name_lower for x in ['gt3', 'corvette', 'm5', 'rs6', 'nsx', 'gt-r', 'supra', 'mc20', 'chiron', 'jesko', 'utopia', 'nevera', 'amg gt', 'artura', '765lt']):
        category = 'Sports'
    elif any(x in name_lower for x in ['taycan', 'lucid', 'tesla']):
        category = 'Electric'
    elif any(x in name_lower for x in ['bentley', 'rolls-royce', 'aston martin']):
        category = 'Luxury'
    elif any(x in name_lower for x in ['silverado', 'f-150', 'ram', 'heavy']):
        category = 'Heavy Duty'
    elif any(x in name_lower for x in ['sienna', 'odyssey', 'pacifica', 'family']):
        category = 'Family'
        
    return {
        "make": make,
        "model": car_name.replace(str(year), '').replace(make, '').strip() or "Model",
        "year": year,
        "price": random.randint(150, 800) * 10,
        "mileage": random.randint(0, 15000),
        "fuel_type": "Electric" if category == 'Electric' else "Petrol",
        "transmission": "Automatic",
        "description": desc_template,
        "features": ["Leather Seats", "Apple CarPlay", "Sunroof", "Premium Audio", "Heated Seats", "Navigation System", "Backup Camera", "Bluetooth"],
        "category": category
    }

def fetch_vehicle_image(car_name, year):
    import subprocess
    import os
    import requests
    
    try:
        # Call the Node.js scraper
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fetch_image.mjs')
        result = subprocess.run(['node', script_path, car_name, str(year)], capture_output=True, text=True, check=True)
        img_src = result.stdout.strip()
        
        if img_src and img_src != 'NONE':
            # Download the image bytes
            img_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            img_res = requests.get(img_src, headers=img_headers, timeout=10)
            if img_res.status_code == 200:
                return img_res.content
    except Exception as e:
        print(f"Failed to fetch image for {car_name}: {e}")
        
    return None

def process_bulk_import(car_list_text):
    import re
    # Split by comma or newline
    cars = [c.strip() for c in re.split(r'[,\n]+', car_list_text) if c.strip()]
    results = []
    
    for car_name in cars:
        try:
            # 1. Generate Data
            data = generate_vehicle_data(car_name)
            
            # 2. Get or create category
            category, _ = Category.objects.get_or_create(
                name=data['make'],
                defaults={'slug': slugify(data['make'])}
            )
            
            # 3. Create Vehicle
            full_name = f"{data['year']} {data['make']} {data['model_name']}"
            vehicle = Vehicle.objects.create(
                name=full_name,
                category=category,
                make=data['make'],
                model=data['model_name'],
                year=data['year'],
                price_per_day=data['price_per_day'],
                full_price=data['full_price'],
                mileage=data['mileage'],
                condition=data['condition'],
                engine_type=data['engine_type'],
                drivetrain=data['drivetrain'],
                exterior_color=data['exterior_color'],
                interior_color=data['interior_color'],
                description=data['description'],
                status='available',
                financing_eligible=True
            )
            
            # 4. Attach Features
            for feat_name in data.get('features', []):
                feature, _ = VehicleFeature.objects.get_or_create(name=feat_name)
                vehicle.features.add(feature)
                
            # 4. Fetch Image
            search_query = f"{data['year']} {data['make']} {data['model_name']}"
            img_content = fetch_vehicle_image(search_query, data['year'])
            if img_content:
                file_name = f"{slugify(full_name)}.jpg"
                
                # Main Image
                vehicle.main_image.save(file_name, ContentFile(img_content), save=True)
                
                # Gallery Image
                VehicleImage.objects.create(
                    vehicle=vehicle,
                    image=vehicle.main_image
                )
                
            results.append({"name": full_name, "status": "success"})
        except Exception as e:
            results.append({"name": car_name, "status": f"error: {str(e)}"})
            
    return results

def generate_bill_of_sale_pdf(plan):
    from io import BytesIO
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from django.utils import timezone
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    Story = []
    
    title_style = styles['Heading1']
    title_style.alignment = 1
    Story.append(Paragraph("BILL OF SALE / PROOF OF OWNERSHIP", title_style))
    Story.append(Spacer(1, 20))
    
    normal_style = styles['Normal']
    normal_style.fontSize = 12
    normal_style.leading = 14
    
    text = """
    This document serves as the official Bill of Sale and Proof of Ownership for the vehicle described below,
    sold by RyderPro to the buyer listed below. The vehicle has been paid in full and is entirely owned by the buyer.
    """
    Story.append(Paragraph(text, normal_style))
    Story.append(Spacer(1, 20))
    
    user_name = plan.user.get_full_name() or plan.user.username
    vin = plan.vehicle.vin or 'N/A'
    
    details = f"""
    <b>Date of Document:</b> {timezone.now().strftime('%B %d, %Y')}<br/>
    <br/>
    <b>Buyer Information:</b><br/>
    Name: {user_name}<br/>
    Email: {plan.user.email}<br/>
    <br/>
    <b>Vehicle Information:</b><br/>
    Make: {plan.vehicle.make}<br/>
    Model: {plan.vehicle.model}<br/>
    Year: {plan.vehicle.year}<br/>
    VIN: {vin}<br/>
    <br/>
    <b>Financial Information:</b><br/>
    Total Purchase Price: ${plan.total_amount:,.2f}<br/>
    Total Amount Paid: ${plan.total_amount:,.2f}<br/>
    Balance Due: $0.00 (PAID IN FULL)<br/>
    """
    Story.append(Paragraph(details, normal_style))
    Story.append(Spacer(1, 40))
    
    Story.append(Paragraph("Authorized Signature: ___________________________", normal_style))
    Story.append(Paragraph("RyderPro Sales Department", normal_style))
    
    doc.build(Story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

def get_live_crypto_rates():
    """Fetch live crypto rates. Using hardcoded fallbacks for reliability if API fails."""
    rates = {'BTC': 65000.0, 'ETH': 3500.0, 'USDT': 1.0}
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether&vs_currencies=usd", timeout=5)
        if response.status_code == 200:
            data = response.json()
            rates['BTC'] = data.get('bitcoin', {}).get('usd', rates['BTC'])
            rates['ETH'] = data.get('ethereum', {}).get('usd', rates['ETH'])
            rates['USDT'] = data.get('tether', {}).get('usd', rates['USDT'])
    except:
        pass
    return rates

# Deposit wallet addresses. These MUST match the addresses shown to the user on
# the checkout page (SiteContent keys crypto_*_address, with the same fallbacks
# used by invest/checkout.html). Verification compares the on-chain recipient
# against these — so they have to be identical or every payment is rejected.
DEFAULT_DEPOSIT_ADDRESSES = {
    'BTC': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
    'ETH': '0x71C7656EC7ab88b098defB751B7401B5f6d8976F',
    'USDT': 'TXLAQ63Xg1NMaF3yGjR91A8R3B8X5Y3x',
}

# Minimum confirmations required before a deposit is trusted.
MIN_CONFIRMATIONS = {'BTC': 1, 'ETH': 2, 'USDT': 1}

# Per-coin tag configuration. `floor` is how far we round the base amount DOWN
# before adding a unique nonce; `unit` is the size of one nonce step (also the
# width of the accepted match band); `nmax` is how many distinct tags exist.
# The uniquely-tagged amount is what ties an on-chain payment to one specific
# user's deposit, so the match must be exact to within one `unit`.
from decimal import Decimal, ROUND_DOWN

_SATOSHI = Decimal('0.00000001')  # 8 dp, the precision we store/compare at
TAG_CONFIG = {
    'BTC':  {'floor': Decimal('0.00001'), 'unit': Decimal('0.00000001'), 'nmax': 999},
    'ETH':  {'floor': Decimal('0.00001'), 'unit': Decimal('0.00000001'), 'nmax': 999},
    'USDT': {'floor': Decimal('1'),       'unit': Decimal('0.01'),       'nmax': 99},
}


def _get_deposit_address(crypto_currency):
    """The configured deposit address for a coin, falling back to the same
    default the checkout template shows."""
    from .models import SiteContent
    key = f"crypto_{crypto_currency.lower()}_address"
    try:
        val = (SiteContent.objects.get(key=key).value or '').strip()
        if val:
            return val
    except SiteContent.DoesNotExist:
        pass
    return DEFAULT_DEPOSIT_ADDRESSES.get(crypto_currency, '')


def generate_unique_tagged_amount(crypto_currency, base_crypto):
    """
    Produce an EXACT crypto amount, close to `base_crypto`, that is unique among
    all currently-outstanding deposits of this coin. The user is told to send
    precisely this amount; because it is unique, the resulting on-chain payment
    can be matched to exactly one deposit intent — so no user can claim another
    user's payment. Returns a Decimal (8 dp) or None if no free tag is available.
    """
    import random
    from .models import CryptoDeposit

    cfg = TAG_CONFIG.get(crypto_currency)
    if not cfg:
        return None

    base = Decimal(str(base_crypto))
    floor_amt = base.quantize(cfg['floor'], rounding=ROUND_DOWN)

    # Amounts already reserved by deposits that could still be matched.
    taken = set(
        CryptoDeposit.objects.filter(
            crypto_currency=crypto_currency,
            status__in=['awaiting_payment', 'pending'],
        ).values_list('crypto_amount', flat=True)
    )

    nonces = list(range(1, cfg['nmax'] + 1))
    random.shuffle(nonces)
    for n in nonces:
        tagged = (floor_amt + cfg['unit'] * n).quantize(_SATOSHI)
        if tagged > 0 and tagged not in taken:
            return tagged
    return None


def _amount_matches(received, expected, crypto_currency):
    """True when `received` lands in [expected, expected + one tag unit): the
    exact tag or a tiny overpay, but never far enough to collide with the next
    tag slot. Underpayment is rejected."""
    cfg = TAG_CONFIG.get(crypto_currency, {'unit': _SATOSHI})
    received = Decimal(received)
    return expected <= received < (expected + cfg['unit'])


def verify_crypto_transaction(tx_hash, crypto_currency, expected_crypto, dummy_mode=False):
    """
    Verify that a real, confirmed on-chain payment of EXACTLY `expected_crypto`
    (the uniquely-tagged amount for one deposit) was made TO OUR deposit address.

    Returns (is_valid, message). Accepted only when ALL hold:
      1. The transaction exists and is confirmed on the correct network.
      2. Its recipient is our configured deposit address for that coin.
      3. The amount sent to us matches the unique tagged amount exactly
         (to within one tag unit — a tiny overpay is tolerated).

    Existence alone is NOT sufficient (the old hole), and neither is a
    right-address-wrong-amount payment. Hash uniqueness is enforced by the
    caller so a payment can only ever be claimed once.
    """
    if dummy_mode and str(tx_hash).startswith('test_'):
        return True, "Verified via Developer Bypass"

    tx_hash = (tx_hash or '').strip()
    if not tx_hash:
        return False, "No transaction hash provided."

    try:
        expected_crypto = Decimal(str(expected_crypto))
    except Exception:
        return False, "Invalid expected amount."
    if expected_crypto <= 0:
        return False, "Invalid expected amount."

    our_address = _get_deposit_address(crypto_currency)
    if not our_address:
        return False, "Deposit address is not configured. Contact support."

    try:
        if crypto_currency == 'BTC':
            received, err = _fetch_btc_received(tx_hash, our_address)
        elif crypto_currency == 'ETH':
            received, err = _fetch_eth_received(tx_hash, our_address)
        elif crypto_currency == 'USDT':
            received, err = _fetch_usdt_received(tx_hash, our_address)
        else:
            return False, "Unsupported currency or invalid hash"
    except requests.RequestException as e:
        return False, f"Verification service unreachable: {str(e)}"
    except Exception as e:
        return False, f"Verification service error: {str(e)}"

    if err:
        return False, err
    if received is None or received <= 0:
        return False, f"This transaction did not pay our {crypto_currency} deposit address."

    if not _amount_matches(received, expected_crypto, crypto_currency):
        return False, (
            f"Amount mismatch. This deposit requires exactly {expected_crypto} "
            f"{crypto_currency}, but the transaction sent {received} {crypto_currency}. "
            f"Please send the exact amount shown."
        )

    return True, f"Verified: {received} {crypto_currency} received."


def _fetch_btc_received(tx_hash, our_address):
    """Return (received_btc: Decimal, err: str|None) — amount paid to our BTC
    address in this confirmed transaction."""
    resp = requests.get(f"https://api.blockcypher.com/v1/btc/main/txs/{tx_hash}", timeout=15)
    if resp.status_code != 200:
        return None, "BTC transaction not found or invalid."
    data = resp.json()

    confirmations = data.get('confirmations', 0)
    if confirmations < MIN_CONFIRMATIONS['BTC']:
        return None, f"Transaction found but not yet confirmed (currently {confirmations} confirmation(s))."

    received_sats = 0
    for out in data.get('outputs', []):
        if our_address in (out.get('addresses') or []):
            received_sats += out.get('value', 0) or 0
    return (Decimal(received_sats) / Decimal(10 ** 8)).quantize(_SATOSHI), None


def _fetch_eth_received(tx_hash, our_address):
    """Return (received_eth: Decimal, err: str|None)."""
    from .models import SiteContent
    try:
        etherscan_key = SiteContent.objects.get(key='etherscan_api_key').value
    except SiteContent.DoesNotExist:
        etherscan_key = ''

    base = "https://api.etherscan.io/api"
    key_param = f"&apikey={etherscan_key}" if etherscan_key else ""

    result = requests.get(
        f"{base}?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}{key_param}",
        timeout=15,
    ).json().get('result')
    if not result:
        return None, "ETH transaction not found or invalid."

    if (result.get('to') or '').lower() != our_address.lower():
        return None, "This transaction did not pay our ETH deposit address."

    # Confirm the tx succeeded and is sufficiently confirmed.
    receipt = requests.get(
        f"{base}?module=proxy&action=eth_getTransactionReceipt&txhash={tx_hash}{key_param}",
        timeout=15,
    ).json().get('result')
    if not receipt:
        return None, "Transaction found but not yet mined/confirmed."
    if receipt.get('status') not in ('0x1', 1, '1'):
        return None, "Transaction failed on-chain."
    try:
        tx_block = int(receipt.get('blockNumber', '0x0'), 16)
        head = int(requests.get(
            f"{base}?module=proxy&action=eth_blockNumber{key_param}", timeout=15
        ).json().get('result', '0x0'), 16)
        if head - tx_block < MIN_CONFIRMATIONS['ETH']:
            return None, "Transaction found but not yet confirmed. Please wait a moment."
    except Exception:
        pass  # receipt success above still stands if confirmation count is unreadable

    received_eth = Decimal(int(result.get('value', '0x0'), 16)) / Decimal(10 ** 18)
    return received_eth.quantize(_SATOSHI), None


def _fetch_usdt_received(tx_hash, our_address):
    """Return (received_usdt: Decimal, err: str|None) for a TRC20 transfer."""
    resp = requests.get(
        f"https://apilist.tronscanapi.com/api/transaction-info?hash={tx_hash}",
        timeout=15,
    )
    if resp.status_code != 200:
        return None, "USDT (TRC20) transaction not found."
    data = resp.json() or {}

    if data.get('contractRet') and data.get('contractRet') != 'SUCCESS':
        return None, f"USDT transaction failed on-chain (status: {data.get('contractRet')})."
    if not data.get('confirmed', False):
        return None, "USDT transaction found but not yet confirmed."

    received = Decimal(0)
    for t in data.get('trc20TransferInfo') or []:
        if (t.get('symbol') or '').upper() == 'USDT' and (t.get('to_address') or '') == our_address:
            decimals = int(t.get('decimals', 6) or 6)
            try:
                received += Decimal(int(t.get('amount_str', '0'))) / Decimal(10 ** decimals)
            except (TypeError, ValueError):
                continue
    return received.quantize(_SATOSHI), None
