"""Quick connectivity + capability check for the Ryder AI Assistant.

Usage:
    python manage.py test_ai                     # ping the model (verifies the key)
    python manage.py test_ai "How does investing work?"   # full chat reply
"""
import os
from django.core.management.base import BaseCommand
from core.models import ChatConfig


class Command(BaseCommand):
    help = "Verify the DeepSeek API key is valid and the assistant responds."

    def add_arguments(self, parser):
        parser.add_argument('message', nargs='?', default=None,
                            help="Optional message to send through the model.")

    def handle(self, *args, **opts):
        cfg = ChatConfig.get_active()
        if not cfg:
            self.stdout.write(self.style.ERROR("No enabled ChatConfig found. Create/enable one in admin."))
            return
        key = (cfg.api_key or os.environ.get("DEEPSEEK_API_KEY", "")).strip()
        self.stdout.write(f"Provider : {cfg.provider}")
        self.stdout.write(f"Base URL : {cfg.base_url}")
        self.stdout.write(f"Model    : {cfg.model_name}")
        self.stdout.write(f"Key set  : {'yes' if key else 'NO — add it in admin'}")
        if not key:
            self.stdout.write(self.style.ERROR("No API key — add it in Admin → AI Assistant Config."))
            return

        try:
            from openai import OpenAI
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"openai SDK not importable: {e}"))
            return

        client = OpenAI(api_key=key, base_url=cfg.base_url or "https://api.deepseek.com")
        message = opts['message'] or "Reply with exactly: Ryder assistant online."
        self.stdout.write(self.style.WARNING(f"\nSending: {message!r} ...\n"))
        try:
            resp = client.chat.completions.create(
                model=cfg.model_name or "deepseek-chat",
                messages=[{"role": "user", "content": message}],
                temperature=0.2,
                timeout=40,
            )
            reply = resp.choices[0].message.content
            usage = getattr(resp, "usage", None)
            self.stdout.write(self.style.SUCCESS("✅ CONNECTED — model replied:\n"))
            self.stdout.write(reply or "(empty)")
            if usage:
                self.stdout.write(self.style.HTTP_INFO(f"\ntokens: prompt={usage.prompt_tokens} completion={usage.completion_tokens}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ FAILED: {type(e).__name__}: {str(e)[:300]}"))
            self.stdout.write(self.style.WARNING(
                "\nCommon causes: wrong/expired key, wrong model_name for this provider, "
                "or base_url mismatch. Check Admin → AI Assistant Config."))
