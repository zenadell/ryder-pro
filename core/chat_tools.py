"""
Ryder AI Assistant — tool definitions and a SAFE, user-scoped dispatcher.

Every tool here only ever reads:
  * public site data (vehicles, investment assets, pages), or
  * the CURRENT logged-in user's own records (request.user).

No tool can read admin data, other users' data, secrets, or the AI's own
API key. Account tools refuse when the user is not authenticated.
"""
from decimal import Decimal, InvalidOperation
from django.urls import reverse
from django.db.models import Q

from .models import (
    Vehicle, InvestmentAsset, InvestorWallet, Investment,
    InvestmentTransaction, WithdrawalRequest, WithdrawalWindow,
)


# ---- OpenAI/DeepSeek-style tool schemas -------------------------------------
TOOLS = [
    {"type": "function", "function": {
        "name": "search_site",
        "description": "Search the whole website for vehicles and investment assets matching a query. Use to locate anything the user asks about.",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string", "description": "What to search for, e.g. 'truck', 'Mercedes', 'bike investment'"}
        }, "required": ["query"]},
    }},
    {"type": "function", "function": {
        "name": "list_investment_assets",
        "description": "List active Fleet Share assets (trucks/vans/bikes) with their daily return %, minimum stake, funding progress and a link to buy shares.",
        "parameters": {"type": "object", "properties": {
            "asset_type": {"type": "string", "enum": ["truck", "van", "bike"], "description": "Optional filter"}
        }},
    }},
    {"type": "function", "function": {
        "name": "list_vehicles",
        "description": "List available vehicles for rent or purchase, optionally filtered by a search term.",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string", "description": "Optional search term, e.g. 'SUV', 'Toyota'"}
        }},
    }},
    {"type": "function", "function": {
        "name": "calculate_investment",
        "description": "Calculate projected earnings for an investment. Provide either an asset_slug (uses that asset's real rate) or a daily_percent.",
        "parameters": {"type": "object", "properties": {
            "amount": {"type": "number", "description": "Investment amount in USD"},
            "asset_slug": {"type": "string", "description": "Slug of the asset to use its real daily rate"},
            "daily_percent": {"type": "number", "description": "Daily return percent if no asset given"},
            "months": {"type": "integer", "description": "Contract length in months (default 1)"}
        }, "required": ["amount"]},
    }},
    {"type": "function", "function": {
        "name": "get_my_account",
        "description": "Get the CURRENT logged-in user's Fleet Share summary: available balance, total invested, total earnings/profit, cumulative withdrawal fee due, and their active shares. Use when the user asks about their own profit, balance, credit, or fleet shares.",
        "parameters": {"type": "object", "properties": {}},
    }},
    {"type": "function", "function": {
        "name": "get_my_transactions",
        "description": "Get the current user's recent payment & investment transactions (deposits, investments, earnings, withdrawals, fees) to monitor payment status.",
        "parameters": {"type": "object", "properties": {
            "limit": {"type": "integer", "description": "How many recent transactions (default 10)"}
        }},
    }},
    {"type": "function", "function": {
        "name": "start_investment",
        "description": "Invest for the current user from their FUNDED wallet balance. If they have enough balance, it completes the investment immediately. If not, it returns an Add Funds link (investing only uses the funded balance — it never charges a card here). Validates the minimum and availability.",
        "parameters": {"type": "object", "properties": {
            "asset_slug": {"type": "string"},
            "amount": {"type": "number"},
            "months": {"type": "integer", "description": "Contract length in months (default 1)"}
        }, "required": ["asset_slug", "amount"]},
    }},
    {"type": "function", "function": {
        "name": "get_page_link",
        "description": "Get the URL of a website page so you can link the user to it or tell them to open it.",
        "parameters": {"type": "object", "properties": {
            "page": {"type": "string", "enum": [
                "home", "invest", "add_funds", "vehicles", "dashboard", "trade_in",
                "tracking", "contact", "faq", "jobs", "blog", "about"
            ]}
        }, "required": ["page"]},
    }},
    {"type": "function", "function": {
        "name": "request_human_agent",
        "description": "Escalate this conversation to a human agent. Call ONLY when the user explicitly asks to talk to a real person/human/agent/support staff.",
        "parameters": {"type": "object", "properties": {
            "reason": {"type": "string", "description": "Short reason for the handoff"}
        }},
    }},
]


def _abs(request, name, **kwargs):
    try:
        return request.build_absolute_uri(reverse(name, kwargs=kwargs))
    except Exception:
        return request.build_absolute_uri("/")


def _D(v):
    try:
        return Decimal(str(v))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal("0")


# ---- Tool implementations ----------------------------------------------------
def _search_site(request, query):
    q = (query or "").strip()
    vehicles = Vehicle.objects.filter(status='available').filter(
        Q(name__icontains=q) | Q(make__icontains=q) | Q(model__icontains=q)
    )[:5]
    assets = InvestmentAsset.objects.filter(is_active=True).filter(
        Q(name__icontains=q) | Q(asset_type__icontains=q)
    )[:5]
    return {
        "vehicles": [{"name": str(v), "url": _abs(request, 'car_details', slug=v.slug),
                      "price_per_day": str(v.price_per_day)} for v in vehicles],
        "investment_assets": [{"name": a.name, "type": a.get_asset_type_display(),
                                "daily_return_percent": str(a.daily_return_percent),
                                "min_investment": str(a.min_investment),
                                "url": _abs(request, 'invest_asset_detail', slug=a.slug)} for a in assets],
    }


def _list_investment_assets(request, asset_type=None):
    qs = InvestmentAsset.objects.filter(is_active=True)
    if asset_type in ('truck', 'van', 'bike'):
        qs = qs.filter(asset_type=asset_type)
    return {"assets": [{
        "name": a.name, "type": a.get_asset_type_display(),
        "daily_return_percent": str(a.daily_return_percent),
        "monthly_return_percent": str(a.monthly_return_percent),
        "min_investment": str(a.min_investment),
        "funded_percent": a.funded_percent,
        "sold_out": a.is_sold_out,
        "url": _abs(request, 'invest_asset_detail', slug=a.slug),
    } for a in qs[:12]]}


def _list_vehicles(request, query=None):
    qs = Vehicle.objects.filter(status='available')
    if query:
        qs = qs.filter(Q(name__icontains=query) | Q(make__icontains=query) | Q(model__icontains=query))
    return {"vehicles": [{
        "name": str(v), "price_per_day": str(v.price_per_day),
        "category": v.category.name if v.category else None,
        "url": _abs(request, 'car_details', slug=v.slug),
    } for v in qs[:12]]}


def _calculate_investment(request, amount, asset_slug=None, daily_percent=None, months=1):
    amt = _D(amount)
    months = int(months or 1)
    rate = None
    asset_name = None
    if asset_slug:
        a = InvestmentAsset.objects.filter(slug=asset_slug, is_active=True).first()
        if a:
            rate = a.daily_return_percent
            asset_name = a.name
            if amt < a.min_investment:
                return {"error": f"Minimum investment for {a.name} is ${a.min_investment}."}
    if rate is None:
        rate = _D(daily_percent if daily_percent is not None else 0)
    daily = amt * rate / Decimal('100')
    monthly = daily * 30
    total_earnings = daily * 30 * months
    win = WithdrawalWindow.current() or WithdrawalWindow.objects.filter(is_active=True).order_by('-opens_at').first()
    fee_note = win.fee_display if win else "set by admin"
    return {
        "asset": asset_name, "amount": str(amt), "daily_return_percent": str(rate),
        "earnings_per_day": str(daily.quantize(Decimal('0.01'))),
        "earnings_per_month": str(monthly.quantize(Decimal('0.01'))),
        "contract_months": months,
        "projected_total_earnings": str(total_earnings.quantize(Decimal('0.01'))),
        "withdrawal_fee": fee_note,
    }


def _require_user(request):
    return request.user.is_authenticated


def _get_my_account(request):
    if not _require_user(request):
        return {"error": "The user is not logged in. Politely ask them to log in to view their account, profit and balance."}
    # Freshly accrue earnings so figures are real-time
    try:
        from .views import _accrue_user_investments
        _accrue_user_investments(request.user)
    except Exception:
        pass
    wallet = InvestorWallet.for_user(request.user)
    invs = request.user.investments.select_related('asset').all()
    active = invs.filter(status='active')
    total_invested = sum((i.amount for i in active), Decimal('0'))
    total_accrued = sum((i.accrued_earnings for i in active), Decimal('0'))
    return {
        "available_to_withdraw": str(wallet.balance),
        "total_invested": str(total_invested),
        "total_profit_earned": str(total_accrued),
        "lifetime_earnings": str(wallet.total_earned),
        "cumulative_withdrawal_fee_due": str(wallet.accumulated_fee),
        "active_investments": [{
            "asset": i.asset.name, "amount": str(i.amount),
            "daily_return_percent": str(i.daily_return_percent),
            "earnings_so_far": str(i.accrued_earnings),
            "contract_months": i.contract_months,
            "matures_on": i.end_date.isoformat() if i.end_date else None,
            "status": i.get_status_display(),
        } for i in invs[:10]],
        "dashboard_url": _abs(request, 'dashboard'),
    }


def _get_my_transactions(request, limit=10):
    if not _require_user(request):
        return {"error": "The user is not logged in. Ask them to log in to see their transactions."}
    limit = max(1, min(int(limit or 10), 30))
    txs = request.user.investment_transactions.all()[:limit]
    return {"transactions": [{
        "date": t.created_at.strftime("%Y-%m-%d %H:%M"),
        "type": t.get_tx_type_display(), "amount": str(t.amount),
        "status": t.get_status_display(), "note": t.note,
    } for t in txs]}


def _start_investment(request, asset_slug, amount, months=1):
    if not _require_user(request):
        return {"error": "The user must be logged in to buy fleet shares. Share the login link and ask them to sign in."}
    a = InvestmentAsset.objects.filter(slug=asset_slug, is_active=True).first()
    if not a:
        return {"error": "That investment asset was not found."}
    amt = _D(amount)
    if amt < a.min_investment:
        return {"error": f"Minimum investment for {a.name} is ${a.min_investment}."}
    if a.is_sold_out or amt > a.amount_remaining:
        return {"error": f"{a.name} is fully funded or only ${a.amount_remaining} remains."}
    months = max(1, min(int(months or 1), 24))

    # Investing draws from the funded wallet balance only.
    try:
        from .views import _accrue_user_investments
        _accrue_user_investments(request.user)
    except Exception:
        pass
    wallet = InvestorWallet.for_user(request.user)
    if wallet.balance < amt:
        shortfall = amt - wallet.balance
        return {
            "needs_funding": True, "balance": str(wallet.balance), "shortfall": str(shortfall),
            "add_funds_url": _abs(request, 'invest_deposit') + f"?amount={shortfall}",
            "message": (f"The user has ${wallet.balance} but the investment needs ${amt}. "
                        f"They must add ${shortfall} to their wallet first via the add_funds_url."),
        }

    inv = Investment.objects.create(
        user=request.user, asset=a, amount=amt, contract_months=months,
        daily_return_percent=a.daily_return_percent,
    )
    wallet.balance -= amt
    wallet.save(update_fields=['balance', 'updated_at'])
    a.amount_funded += amt
    a.save(update_fields=['amount_funded'])
    InvestmentTransaction.objects.create(
        user=request.user, investment=inv, tx_type='investment', amount=amt,
        status='completed', note=f"Invested in {a.name} (via assistant)",
    )
    return {
        "ok": True, "asset": a.name, "amount": str(amt), "contract_months": months,
        "new_balance": str(wallet.balance), "dashboard_url": _abs(request, 'dashboard'),
        "message": f"Investment confirmed from the user's wallet balance: ${amt} in {a.name} for {months} month(s). Earnings accrue daily.",
    }


def _get_page_link(request, page):
    page_map = {
        "home": ("home", {}), "invest": ("invest_marketplace", {}),
        "add_funds": ("invest_deposit", {}),
        "vehicles": ("all_cars", {}), "dashboard": ("dashboard", {}),
        "trade_in": ("trade_in", {}), "tracking": ("shipment_tracking", {}),
        "contact": ("contact", {}), "faq": ("faq", {}),
        "jobs": ("jobs_list", {}), "blog": ("blog", {}), "about": ("about", {}),
    }
    name, kw = page_map.get(page, ("home", {}))
    return {"page": page, "url": _abs(request, name, **kw)}


def _request_human_agent(request, conversation, reason=None):
    if conversation:
        conversation.status = 'human_requested'
        conversation.save(update_fields=['status', 'updated_at'])
        
        # Trigger notifications asynchronously or simply inline for now
        from django.core.mail import send_mail
        from django.conf import settings
        from django.contrib.auth.models import User
        from .models import AdminDevice
        import requests
        
        user_ident = request.user.email if request.user.is_authenticated else "A guest user"
        msg = f"{user_ident} has requested a human agent on the live chat.\nReason: {reason or 'Not provided'}"
        
        # 1. Send Email to superusers
        admin_emails = [u.email for u in User.objects.filter(is_superuser=True) if u.email]
        if admin_emails:
            try:
                send_mail(
                    subject="Ryder Pro Live Chat: Agent Requested",
                    message=msg,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@ryderpro.com'),
                    recipient_list=admin_emails,
                    fail_silently=True,
                )
            except Exception:
                pass
                
        # 2. Send Expo Push Notifications
        tokens = list(AdminDevice.objects.values_list('push_token', flat=True))
        if tokens:
            try:
                push_data = []
                for t in tokens:
                    push_data.append({
                        "to": t,
                        "title": "Live Chat Request",
                        "body": msg,
                        "sound": "default"
                    })
                requests.post("https://exp.host/--/api/v2/push/send", json=push_data, timeout=5)
            except Exception:
                pass

    return {"ok": True, "message": "A human agent has been notified and will join this chat shortly."}


# ---- Dispatcher --------------------------------------------------------------
def dispatch_tool(name, args, request, conversation=None):
    """Execute a tool by name with the given args. Always returns a JSON-able dict."""
    args = args or {}
    try:
        if name == "search_site":
            return _search_site(request, args.get("query", ""))
        if name == "list_investment_assets":
            return _list_investment_assets(request, args.get("asset_type"))
        if name == "list_vehicles":
            return _list_vehicles(request, args.get("query"))
        if name == "calculate_investment":
            return _calculate_investment(request, args.get("amount"), args.get("asset_slug"),
                                         args.get("daily_percent"), args.get("months", 1))
        if name == "get_my_account":
            return _get_my_account(request)
        if name == "get_my_transactions":
            return _get_my_transactions(request, args.get("limit", 10))
        if name == "start_investment":
            return _start_investment(request, args.get("asset_slug"), args.get("amount"), args.get("months", 1))
        if name == "get_page_link":
            return _get_page_link(request, args.get("page", "home"))
        if name == "request_human_agent":
            return _request_human_agent(request, conversation, args.get("reason"))
        return {"error": f"Unknown tool: {name}"}
    except Exception as e:
        return {"error": f"Tool failed: {str(e)}"}
