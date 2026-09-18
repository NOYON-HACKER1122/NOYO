import requests
import time
import json
import os
import uuid
import threading
import random
import re
import html
import csv
import io
import pyotp
import copy
import tempfile
import zipfile
import logging
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin, urlparse
from pathlib import Path
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
TOKEN = '8863965439:AAGa2s7NdNw9Ekv_LNihmkRcgwvluk2IQz8'
if not TOKEN:
    try:
        TOKEN = input('Enter Telegram Bot Token (@BotFather): ').strip()
    except (EOFError, KeyboardInterrupt):
        TOKEN = ''
if not TOKEN:
    raise RuntimeError('❌ Bot token not found. Set BOT_TOKEN, create bot_token.txt next to this file, or enter the token when prompted.')
BASE_URL = f'https://api.telegram.org/bot{TOKEN}'
FILE_URL = f'https://api.telegram.org/file/bot{TOKEN}/'
OWNER_ID = 7546719381
BOT_USERNAME = '@Test404404404bot'
DB_FILE = 'bot_data.json'
PEM = {'ok': '<tg-emoji emoji-id="5352694861990501856">✅</tg-emoji>', 'no': '<tg-emoji emoji-id="6267000941547885720">❌</tg-emoji>', 'warn': '<tg-emoji emoji-id="5336944168944047463">⚠️</tg-emoji>', 'admin': '<tg-emoji emoji-id="5353032893096567467">📊</tg-emoji>', 'user': '<tg-emoji emoji-id="5352861489541714456">👤</tg-emoji>', 'file': '<tg-emoji emoji-id="5352721946054268944">📁</tg-emoji>', 'rocket': '<tg-emoji emoji-id="5352597830089347330">🚀</tg-emoji>', 'graph': '<tg-emoji emoji-id="5352877703043258544">📊</tg-emoji>', 'money': '<tg-emoji emoji-id="5348469219761626211">💸</tg-emoji>', 'gift': '<tg-emoji emoji-id="5420396762189831222">🎁</tg-emoji>', 'msg': '<tg-emoji emoji-id="5337302974806922068">💬</tg-emoji>', 'gear': '<tg-emoji emoji-id="5420155432272438703">⚙️</tg-emoji>', 'link': '<tg-emoji emoji-id="5420517437885943844">🔗</tg-emoji>', 'trash': '<tg-emoji emoji-id="5422557736330106570">🗑</tg-emoji>', 'upload': '<tg-emoji emoji-id="5353001161878182134">📤</tg-emoji>', 'world': '<tg-emoji emoji-id="5336972142066047577">🌐</tg-emoji>', 'lock': '<tg-emoji emoji-id="5353022963132174959">🔐</tg-emoji>', 'phone': '<tg-emoji emoji-id="4969841369850840381">📱</tg-emoji>', 'num': '<tg-emoji emoji-id="5352862640592949843">🔢</tg-emoji>', 'pin': '<tg-emoji emoji-id="5352922460897452503">📍</tg-emoji>', 'star': '<tg-emoji emoji-id="5352552689983067014">✨</tg-emoji>', 'hi': '<tg-emoji emoji-id="5353027129250453493">👋</tg-emoji>'}
GLOBAL_BODY_EMOJIS = {'✅': '5352694861990501856', '❌': '5420130255174145507', '⚠️': '5336944168944047463', '🔥': '5337267511261960341', '🌟': '5337102391244263212', '✨': '5352552689983067014', '➖': '5870818207383686839', '➕': '5420323438508155202', '➡️': '6319061296704656261', '🔄': '6264896248659056036', '⌛': '4958503072801228000', '⏳': '6285092198497129798', '🕓': '5336983442125001376', '🔴': '6267237615720731788', '👤': '5352861489541714456', '👥': '4972130076318500235', '👋': '5353027129250453493', '👇': '5406745015365943482', '👨\u200d⚖️': '5334763399299506604', '😒': '5334763399299506604', '😔': '6120863614149596295', '🫂': '5420145051336485498', '1️⃣': '5877664071720898423', '2️⃣': '5877223446731034464', '3️⃣': '5879546817879740639', '4️⃣': '5879844832775507443', '5️⃣': '5879657954453491518', '6️⃣': '5877556203617259178', '7️⃣': '5879611822209765566', '8️⃣': '5879971663159758717', '9️⃣': '5877752470737784316', '🔢': '5352862640592949843', '🆔': '5352862640592949843', '📊': '5353032893096567467', '📈': '5352877703043258544', '📁': '5352721946054268944', '📦': '5352721946054268944', '📂': '5257969839313526622', '📤': '5353001161878182134', '📝': '5192739271886282680', '🧾': '5192739271886282680', '📅': '5352585194295564660', '📋': '6267008582294705964', '💾': '5197269100878907942', '📛': '6325731252066325108', '💬': '5337302974806922068', '🎙': '5355102594886833928', '📢': '5789428375261023681', '📌': '5318986077455795572', '📍': '5352922460897452503', '📞': '5213179235996294999', '🔑': '6282760761399841824', '🔐': '5337255927735163754', '🔗': '5420517437885943844', '⚙️': '5420155432272438703', '🛡': '5190447043545438788', '🚫': '5334807341109908955', '🌐': '6266794310671275367', '🔒': '6282846669335702032', '💸': '5348469219761626211', '🏦': '5348469219761626211', '💰': '4958926882994127612', '💎': '5352838545826420397', '💳': '5190899075968441286', '🎁': '5420396762189831222', '🤝': '5192805934073685937', '🚀': '5352597830089347330', '🍏': '5337132498965010628', '📱': '5337132498965010628', '🌍': '5780471598922337683', '🗑': '5422557736330106570', '🟢': '5192812028632274956', '👀': '5190645917711114179', '🕹': '5193100774988617665', '🧪': '5190781475468915802', '🎨': '5190751148704833975', '💡': '5422439311196834318', '🎯': '5276032951342088188'}
DEFAULT_CUSTOM_MESSAGES = {'start': {'text': '★彡➖➖➖➖➖➖➖➖➖彡★\n  <tg-emoji emoji-id="6264778055454036969">📊</tg-emoji> NUMBER BOT\n★彡➖➖➖➖➖➖➖➖➖彡★\n<tg-emoji emoji-id="5258332798409783582">🚀</tg-emoji> Welcome to Number &amp; OTP Service\n➖➖➖➖➖➖➖➖➖\n<tg-emoji emoji-id="6071001861341580968">✅</tg-emoji> Choose an option below\nto continue using the bot.\n➖➖➖➖➖➖➖➖➖\n<tg-emoji emoji-id="6073231507713954071">💎</tg-emoji> Premium OTP Service.', 'buttons': []}, 'get_number': {'text': f"{PEM['pin']} Select a service:", 'buttons': []}, 'select_country': {'text': f'📌 Select a country for {{service}}:', 'buttons': []}, 'search_number': {'text': f"{PEM['num']} <b>Search Number</b>\n\nEnter a range like <code>26134XXXX</code>, <code>23275XXXX</code>, or a 3-9 digit prefix:", 'buttons': []}, 'traffic': {'text': f"{PEM['graph']} <b>Traffic Overview</b>\n\n{PEM['ok']} Available Numbers: {{avail}}\n{PEM['rocket']} Assigned Numbers: {{assigned}}", 'buttons': []}, 'refer': {'text': f"➖➖➖➖➖➖➖\n« {PEM['gift']} REFER & EARN »\n➖➖➖➖➖➖➖\n{PEM['link']} YOUR LINK:\n<code>{{ref_link}}</code>\n➖➖➖➖➖➖➖\n{PEM['user']} TOTAL REFERS: <b>{{total_ref}}</b>\n➖➖➖➖➖➖➖\n{PEM['money']} PER REFER: <b>{{ref_reward}}৳</b>\n➖➖➖➖➖➖➖", 'buttons': []}, 'withdrawal': {'text': '➖➖➖➖➖➖➖\n《 😒 WITHDRAWAL 》\n➖➖➖➖➖➖➖\n👋 Total Otp: {total_otp}\n➖➖➖➖➖➖➖\n🫂 Total Reffer :{total_ref}\n➖➖➖➖➖➖➖\n📅 BALANCE: {bal}৳\n➖➖➖➖➖➖➖\n🔐 MINIMUM: {min_w}৳\n➖➖➖➖➖➖➖\nSELECT METHOD:', 'buttons': []}, 'balance': {'text': '《 💰 BALANCE 》\n➖➖➖➖➖➖➖\n👋 Total Otp: {total_otp}\n➖➖➖➖➖➖➖\n🫂 Total Reffer :{total_ref}\n➖➖➖➖➖➖➖\n💰 BALANCE: {bal}৳\n➖➖➖➖➖➖➖\n🔐 MINIMUM: {min_w}৳', 'buttons': []}, 'support': {'text': f"{PEM['msg']} Contact us for any help:", 'buttons': []}}
logger.info('Running in Local Mode')
CURRENCY_CODE = 'BDT'
CURRENCY_SYMBOL = '৳'
Taka = CURRENCY_SYMBOL

bot_settings = {'admins': [OWNER_ID], 'panels': [], 'fw_groups': [], 'topics': [], 'otp_link': 'https://t.me/vip3member', 'withdraw_on': True, 'min_withdraw': 30.0, 'otp_reward': 0.1, 'refer_reward': 0.2, 'cooldown': 10, 'num_req': 3, 'num_share': 1, 'support_link': 'https://t.me/NOYON_MASTER_support', 'w_methods': ['bKash', 'Nagad', 'Rocket'], 'w_group': '', 'fj_on': False, 'fj_channels': [], 'nexa_on': False, 'voltx_on': False, 'stex_on': False, 'nexa_keys': [], 'voltx_keys': [], 'stex_keys': [], 'nexa_search_countries': [], 'voltx_search_countries': [], 'stex_search_countries': [],'smsbower_on': False, 'smsbower_api_key': '', 'smsbower_services': {}, 'nexa_services': {}, 'voltx_services': {}, 'stex_services': {}, 'search_countries': [], 'premium_flags': {'1': {'char': '🇺🇸', 'iso': 'US', 'name': 'United States', 'id': '5913463998522592692'}, '880': {'char': '🇧🇩', 'iso': 'BD', 'name': 'Bangladesh', 'id': '5911365056594973179'}, '91': {'char': '🇮🇳', 'iso': 'IN', 'name': 'India', 'id': '5913754823643107921'}, '92': {'char': '🇵🇰', 'iso': 'PK', 'name': 'Pakistan', 'id': '5913705895375672082'}, '44': {'char': '🇬🇧', 'iso': 'GB', 'name': 'United Kingdom', 'id': '5913443365499703513'}}, 'premium_apps': {'FACEBOOK': {'char': '🚫', 'id': '5334807341109908955', 'name': 'Facebook'}, 'WHATSAPP': {'char': '🚫', 'id': '5334759662677957452', 'name': 'WhatsApp'}}, 'custom_messages': DEFAULT_CUSTOM_MESSAGES.copy(), 'sys_emoji_overrides': {}}
_db_save_lock = threading.Lock()
number_batches = {}
used_numbers_list = []
nexa_assigned_numbers = {}
NEXA_BASE_URL = 'https://nexaotpservice.com'
voltx_assigned_numbers = {}
VOLTX_BASE_URL = 'https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api'
stex_assigned_numbers = {}
STEX_BASE_URL = 'https://api.2oo9.cloud/MXS47FLFX0U/tness/@public/api'
smsbower_assigned_numbers = {}   # {activation_id: owner_id}
SMSBOWER_BASE_URL = 'https://smsbower.page/stubs/handler_api.php'
total_uploaded_stats = 0
total_assigned_stats = 0
_stats_lock = threading.Lock()
_data_lock = threading.Lock()
_traffic_lock = threading.Lock()
processed_otps = {}
SEEN_OTPS_FILE = 'seen_otps.json'
_seen_otps_save_lock = threading.Lock()
_nexa_session = requests.Session()
_voltx_session = requests.Session()
_stex_session = requests.Session()
recent_traffic = []
user_banned_cache = {}
_banned_cache_lock = threading.Lock()
otp_received_numbers = set()
_service_warmup_needed = {'nexa': False, 'voltx': False, 'stex': False}
panel_sessions = {}
_OTP_RECV_MAX = 50000

def _fetch_number_via_panels(query, chat_id, force_auto=False):
    """Try all enabled panels in order (Nexa → VoltX → Stex).
    Enforces strict per-panel isolation: if the admin configured ranges/services
    in any panel, only the panel(s) where that prefix was configured may serve it.
    If no panel has any services configured at all, all panels run in free/auto mode.
    Returns (num_str, panel_name) or (None, None)."""

    _nexa_srvs = bot_settings.get("nexa_services", {})
    _voltx_srvs = bot_settings.get("voltx_services", {})
    _stex_srvs  = bot_settings.get("stex_services", {})

    # Are ANY services/ranges configured by the admin across all panels?
    _any_configured = (
        any(rng for c in _nexa_srvs.values()  for rl in c.values() for rng in rl) or
        any(rng for c in _voltx_srvs.values() for rl in c.values() for rng in rl) or
        any(rng for c in _stex_srvs.values()  for rl in c.values() for rng in rl)
    )
    # allow_auto=True only when NO panel has any configuration (pure auto mode)
    allow_auto = force_auto or not _any_configured

    # Try Nexa (only if ON)
    if bot_settings.get("nexa_on", False):
        num, _key = try_nexa_get_number(query, chat_id, allow_auto=allow_auto)
        if num:
            return num, "Nexa"

    # Try VoltX (only if ON)
    if bot_settings.get("voltx_on", False):
        num, _key = try_voltx_get_number(query, chat_id, allow_auto=allow_auto)
        if num:
            return num, "VoltX"

    # Try Stex (only if ON)
    if bot_settings.get("stex_on", False):
        num, _key = try_stex_get_number(query, chat_id, allow_auto=allow_auto)
        if num:
            return num, "Stex"
            
    # Try SMSBower (only if ON)
    if bot_settings.get("smsbower_on", False):
        sb_services = bot_settings.get("smsbower_services", {})
        for svc_code, cnt_id in sb_services.items():
            num, _aid = try_smsbower_get_number(svc_code, cnt_id, chat_id)
            if num:
                return num, "SMSBower"

    return None, None

def _find_assigned_owner(assigned_dict, clean_num):
    """Find owner_id for a number in any assigned_numbers dict. Returns owner_id or None."""
    for n, owner in assigned_dict.items():
        clean_n = str(n).replace("+", "").replace(" ", "").replace("-", "").strip()
        if clean_n == clean_num:
            return owner
        # Fuzzy suffix match — only when lengths differ by ≤3 digits (country-code prefix).
        # Guard prevents false matches between unrelated numbers sharing last 8 digits.
        if (len(clean_n) >= 8 and len(clean_num) >= 8 and
                abs(len(clean_n) - len(clean_num)) <= 3 and
                (clean_n.endswith(clean_num[-8:]) or
                 clean_num.endswith(clean_n[-8:]))):
            return owner
    return None

def _try_mauthapi_get_number(query, chat_id, base_url, keys_setting, services_setting,
                              assigned_dict, poll_fn, getnum_payload_extra=None,
                              extra_num_field=None, allow_auto=True):
    """Shared number allocation helper for VoltX and Stex (same mauthapi platform).
    getnum_payload_extra: extra POST body fields (e.g. {"m":"n","range":""} for VoltX).
    extra_num_field: extra number key to try before 'number' (e.g. 'phone_number'/'national_number')."""
    global total_assigned_stats
    api_keys = bot_settings.get(keys_setting, [])
    if not api_keys:
        return None, None
    ranges_to_try = []
    services_all = bot_settings.get(services_setting, {})
    has_services = any(
        ranges
        for countries in services_all.values()
        for ranges in countries.values()
    )
    for srv, countries in services_all.items():
        for cnt, ranges in countries.items():
            for rng in ranges:
                rng_prefix = rng.replace("X", "").replace("x", "")
                if query.startswith(rng_prefix) or rng_prefix.startswith(query):
                    ranges_to_try.append(rng)
    # If no matching configured range exists, AUTO MODE must still be able to
    # request a number when allow_auto=True.  The previous logic blocked auto
    # allocation whenever *any* service/range existed in this panel.
    if not ranges_to_try:
        if not allow_auto:
            return None, None
        auto_range = query + ("XXX" if len(query) >= 4 else "X" * (7 - len(query)))
        ranges_to_try.append(auto_range)
    for _ in range(bot_settings.get("num_req", 1)):
        for api_key in api_keys:
            for rng in ranges_to_try:
                try:
                    headers = {"mauthapi": api_key, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
                    rid_value = rng.replace("X", "").replace("x", "")
                    payload = {"rid": rid_value}
                    if getnum_payload_extra:
                        payload.update(getnum_payload_extra)
                    _ms = _voltx_session if base_url == VOLTX_BASE_URL else _stex_session
                    res = _ms.post(f"{base_url}/getnum", json=payload, headers=headers, timeout=15)
                    data = res.json()
                    meta = data.get("meta", {})
                    if meta.get("code") == 200 and data.get("data"):
                        num_data = data["data"]
                        num_str = str(
                            num_data.get("no_plus_number") or
                            num_data.get("full_number") or
                            (num_data.get(extra_num_field) if extra_num_field else None) or
                            num_data.get("number") or ""
                        ).replace("+", "").replace(" ", "")
                        if num_str and not num_str.startswith(rid_value[:len(query)]):
                            logger.warning(f"{keys_setting} returned wrong range: {num_str} (expected: {rid_value})")
                            continue
                        if num_str:
                            with _data_lock:
                                assigned_dict[num_str] = chat_id
                            with _stats_lock:
                                total_assigned_stats += 1
                            threading.Thread(target=poll_fn, args=(num_str, chat_id, api_key), daemon=True).start()
                            return num_str, api_key
                except Exception as e:
                    logger.warning(f"{keys_setting} getnum error: {e}")
                    continue
    return None, None



# Removed external OTP providers: Nexa / VoltX / Stex
def try_nexa_get_number(query, chat_id, allow_auto=True):
    """Try to allocate a number from Nexa. Returns (num_str, api_key) or (None, None).
    allow_auto=False → if Nexa has no matching configured range, skip immediately
    (used when at least one panel has services configured by the admin)."""
    global total_assigned_stats

    if not bot_settings.get("nexa_on", False):
        return None, None

    nexa_keys = bot_settings.get("nexa_keys", [])
    if not nexa_keys:
        return None, None

    nexa_srvs = bot_settings.get("nexa_services", {})
    has_nexa_srvs = any(
        rng
        for countries in nexa_srvs.values()
        for ranges in countries.values()
        for rng in ranges
    )
    clean_q = query.replace("X", "").replace("x", "")

    # Range-match check
    nexa_has_match = any(
        rng.replace("X", "").replace("x", "").startswith(clean_q) or
        clean_q.startswith(rng.replace("X", "").replace("x", ""))
        for countries in nexa_srvs.values()
        for ranges in countries.values()
        for rng in ranges
    )

    # In AUTO MODE, a configured panel may still use its API's free/auto
    # range when the requested prefix has no configured match.
    if not nexa_has_match and not allow_auto:
        return None, None

    t_len = 12
    if query.startswith("880"): t_len = 13
    elif query.startswith("1") and len(query) < 12: t_len = 11
    search_range = query + ("X" * (t_len - len(query))) if len(query) < t_len else query

    payloads = [
        {"range": search_range, "format": "normal"},
        {"range": search_range},
        {"prefix": query},
    ]

    for _ in range(bot_settings.get("num_req", 1)):
        for api_key in nexa_keys:
            for payload in payloads:
                try:
                    headers = {"X-API-Key": api_key}
                    res = _nexa_session.post(
                        f"{NEXA_BASE_URL}/api/v1/numbers/get",
                        json=payload, headers=headers, timeout=10
                    )
                    resp = res.json()
                    if resp.get("success") and (resp.get("number") or resp.get("phone_number")):
                        num_str = str(resp.get("number") or resp.get("phone_number", "")).replace("+", "")
                        # FIX: Nexa multiple number_id field names support karo
                        number_id = (resp.get("number_id") or resp.get("id") or
                                     resp.get("sms_id") or resp.get("num_id") or resp.get("phone_id"))
                        if not num_str:
                            continue
                        # ✅ Range validation: reject number that doesn't match the requested prefix
                        if not num_str.startswith(clean_q):
                            logger.warning(f"Nexa returned wrong range: {num_str} (expected: {clean_q})")
                            continue
                        with _data_lock:
                            nexa_assigned_numbers[num_str] = chat_id
                        with _stats_lock:
                            total_assigned_stats += 1
                        if number_id:
                            threading.Thread(
                                target=poll_otp_with_status,
                                args=(number_id, num_str, chat_id, api_key),
                                daemon=True
                            ).start()
                        return num_str, api_key
                    elif not resp.get("success") and resp.get("code") == 401:
                        break  # Bad API key — skip remaining payloads for this key
                except Exception as e:
                    logger.warning(f"Nexa getnum error: {e}")
                    continue
    return None, None
def try_voltx_get_number(query, chat_id, allow_auto=True):
    """Allocate a number from VoltX — thin wrapper around _try_mauthapi_get_number."""
    return _try_mauthapi_get_number(
        query, chat_id, VOLTX_BASE_URL, "voltx_keys", "voltx_services",
        voltx_assigned_numbers, voltx_poll_otp,
        # FIX: "range": "" hata diya — rid pehle se payload mein hai, empty range conflict karta tha
        getnum_payload_extra={"m": "n"},
        extra_num_field="phone_number",
        allow_auto=allow_auto
    )
def try_stex_get_number(query, chat_id, allow_auto=True):
    """Allocate a number from Stex SMS — thin wrapper around _try_mauthapi_get_number."""
    return _try_mauthapi_get_number(
        query, chat_id, STEX_BASE_URL, "stex_keys", "stex_services",
        stex_assigned_numbers, stex_poll_otp,
        extra_num_field="national_number",
        allow_auto=allow_auto
    )
def voltx_poll_otp(num_str, owner_id, api_key):
    return _poll_mauthapi_otp_single('VX', VOLTX_BASE_URL, 'VoltX SMS', num_str, owner_id, api_key)
def stex_poll_otp(num_str, owner_id, api_key):
    return _poll_mauthapi_otp_single('STX', STEX_BASE_URL, 'Stex SMS', num_str, owner_id, api_key)

# ==================== SMSBOWER API FUNCTIONS ====================
def try_smsbower_get_number(service_code, country_id, chat_id):
    """SMSBower থেকে নাম্বার রিকোয়েস্ট করুন।
    রেসপন্সে 'number' এবং 'activationId' আসে।"""
    api_key = bot_settings.get('smsbower_api_key', '').strip()
    if not api_key:
        return None, None
    try:
        params = {
            'api_key': api_key,
            'action': 'getNumber',
            'service': service_code,
            'country': country_id,
            'operator': 'any'
        }
        res = tg_session.get(SMSBOWER_BASE_URL, params=params, timeout=15)
        try:
            data = res.json()
        except Exception:
            logger.warning(f'SMSBower getNumber invalid JSON: {res.text[:150]!r}')
            return None, None

        status = str(data.get('status', '')).upper()
        if status in ('SUCCESS', '1') and (data.get('number') or data.get('phone')):
            num_str = str(data.get('number') or data.get('phone')).replace('+', '').replace(' ', '').strip()
            activation_id = str(data.get('activationId') or data.get('id') or '').strip()
            if num_str and activation_id:
                with _data_lock:
                    smsbower_assigned_numbers[activation_id] = chat_id
                save_local_db()
                threading.Thread(
                    target=smsbower_poll_otp,
                    args=(activation_id, num_str, chat_id, api_key),
                    daemon=True
                ).start()
                return num_str, activation_id

        err_msg = data.get('status') or data.get('error') or 'Unknown'
        logger.warning(f'SMSBower getNumber failed: {err_msg}')
    except Exception as e:
        logger.warning(f'SMSBower getNumber error: {e}')
    return None, None


def smsbower_poll_otp(activation_id, num_str, owner_id, api_key):
    """SMSBower থেকে OTP পোল করুন (প্রতি ১২ সেকেন্ডে, ২৫ মিনিট পর্যন্ত)।"""
    for _ in range(125):
        try:
            params = {
                'api_key': api_key,
                'action': 'getStatus',
                'id': activation_id
            }
            res = tg_session.get(SMSBOWER_BASE_URL, params=params, timeout=10)
            try:
                data = res.json()
            except Exception:
                logger.warning(f'SMSBower getStatus invalid JSON: {res.text[:150]!r}')
                time.sleep(12)
                continue

            status = str(data.get('status', '')).upper()
            if 'STATUS_OK' in status or status == '1':
                sms_block = data.get('sms') or {}
                otp = str(data.get('code') or sms_block.get('code') or '')
                msg_text = str(
                    sms_block.get('text') or
                    data.get('text') or
                    (data.get('sms') if isinstance(data.get('sms'), str) else '') or
                    f'Your code is {otp}'
                )
                if not otp:
                    otp = extract_otp_code(msg_text)
                if otp:
                    unique_id = f'SMSBOWER_{activation_id}'
                    if not _is_processed(unique_id, window=90000):
                        _add_to_processed(unique_id)
                        app_name = detect_service(msg_text) or 'SMSBower'
                        _record_and_deliver_otp(
                            owner_id, num_str, app_name, msg_text, otp,
                            num_str, 'smsbower_poll'
                        )
                        try:
                            tg_session.get(SMSBOWER_BASE_URL, params={
                                'api_key': api_key,
                                'action': 'setStatus',
                                'id': activation_id,
                                'status': '6'
                            }, timeout=10)
                        except Exception:
                            pass
                    return

            elif 'STATUS_CANCEL' in status:
                logger.info(f'SMSBower activation {activation_id} cancelled')
                with _data_lock:
                    smsbower_assigned_numbers.pop(activation_id, None)
                return

        except Exception as e:
            logger.warning(f'SMSBower poll error: {e}')
        time.sleep(12)

    try:
        tg_session.get(SMSBOWER_BASE_URL, params={
            'api_key': api_key,
            'action': 'setStatus',
            'id': activation_id,
            'status': '8'
        }, timeout=10)
        logger.info(f'SMSBower activation {activation_id} timed out and cancelled.')
    except Exception:
        pass
    with _data_lock:
        smsbower_assigned_numbers.pop(activation_id, None)
# ==================== END SMSBOWER API ====================
def fetch_cpt_panel_cdrs(p, session, check_url):
    res = session.get(check_url, timeout=15, allow_redirects=True)
    html_text = res.text
    final_url = res.url.lower()
    last_path = final_url.split('?')[0].rstrip('/').split('/')[-1]
    is_login_page = last_path in ('login', 'signin', 'sign-in', 'log-in', 'auth')
    if not is_login_page:
        soup_check = BeautifulSoup(html_text, 'html.parser')
        login_form = soup_check.find('input', {'type': 'password'})
        login_phrases = ['sign in to your account', 'please sign in', 'please login', 'log in to continue']
        page_lower = html_text.lower()
        has_login_phrase = any((phrase in page_lower for phrase in login_phrases))
        if login_form and has_login_phrase:
            is_login_page = True
    if is_login_page:
        raise Exception('Session expired')
    soup = BeautifulSoup(html_text, 'html.parser')
    s_ajax_source = ''
    for script in soup.find_all('script'):
        script_text = script.string or ''
        match = re.search('sAjaxSource":\\s*"([^"]+)"', script_text)
        if match:
            s_ajax_source = match.group(1)
            break
    results = []
    n_col_name = p.get('num_col_name', 'number').lower()
    m_col_name = p.get('msg_col_name', 'message').lower()
    n_idx = int(p.get('num_col_idx', 2)) - 1 if p.get('num_col_idx') is not None else 1
    m_idx = int(p.get('msg_col_idx', 3)) - 1 if p.get('msg_col_idx') is not None else 2
    _header_tables = soup.find_all('table')
    for _t in _header_tables:
        _rows = _t.find_all('tr')
        if _rows:
            _hn_idx, _hm_idx = _find_header_column_indices(_rows, n_col_name, m_col_name, n_idx, m_idx)
            if (_hn_idx, _hm_idx) != (n_idx, m_idx):
                n_idx, m_idx = (_hn_idx, _hm_idx)
            break
    if s_ajax_source:
        baseUrl = p.get('login_url', '').split('/client')[0].split('/login')[0].strip()
        if not baseUrl.startswith('http'):
            baseUrl = 'http://' + baseUrl
        full_ajax_url = ''
        if s_ajax_source.startswith('http'):
            full_ajax_url = s_ajax_source
        elif s_ajax_source.startswith('/'):
            full_ajax_url = f'{baseUrl}{s_ajax_source}'
        else:
            last_slash_idx = check_url.rfind('/')
            current_dir = check_url[:last_slash_idx]
            full_ajax_url = f'{current_dir}/{s_ajax_source}'
        if 'iDisplayLength' not in full_ajax_url:
            query_params = 'sEcho=1&iColumns=7&iDisplayStart=0&iDisplayLength=20000&sSearch=&iSortingCols=1&iSortCol_0=0&sSortDir_0=desc'
            divider = '&' if '?' in full_ajax_url else '?'
            full_ajax_url += f'{divider}{query_params}'
        ajax_headers = {'Referer': check_url, 'X-Requested-With': 'XMLHttpRequest'}
        ajax_res = session.get(full_ajax_url, headers=ajax_headers, timeout=30)
        data_dict = ajax_res.json()
        rows = data_dict.get('aaData', [])
        try:
            _total_recs = int(data_dict.get('iTotalDisplayRecords') or data_dict.get('iTotalRecords') or 0)
            if _total_recs and len(rows) < _total_recs:
                logger.warning(f"Panel '{p.get('name')}' has {_total_recs} records today but only {len(rows)} fetched — consider raising iDisplayLength further.")
        except (TypeError, ValueError):
            pass
        for row_val in rows:
            if not isinstance(row_val, list):
                continue
            if len(row_val) < max(n_idx, m_idx) + 1:
                continue
            num_val = row_val[n_idx] if 0 <= n_idx < len(row_val) else row_val[1] if len(row_val) > 1 else ''
            msg_val = row_val[m_idx] if 0 <= m_idx < len(row_val) else row_val[2] if len(row_val) > 2 else ''
            datetime_val = ''
            for col in row_val:
                col_str = str(col).strip()
                if re.search('\\d{4}[-/]\\d{2}[-/]\\d{2}', col_str) and re.search('\\d{2}:\\d{2}:\\d{2}', col_str):
                    datetime_val = col_str
                    break
            if not datetime_val:
                date_part = ''
                time_part = ''
                for col in row_val:
                    col_str = str(col).strip()
                    if not date_part:
                        m = re.search('\\d{4}[-/]\\d{2}[-/]\\d{2}', col_str)
                        if m:
                            date_part = m.group()
                    if not time_part:
                        m = re.search('\\d{2}:\\d{2}:\\d{2}', col_str)
                        if m:
                            time_part = m.group()
                datetime_val = f'{date_part} {time_part}'.strip()
            msg_val = re.sub('(?<!\\n)nn(?!\\n)', '\n', str(msg_val))
            clean_num = re.sub('\\D', '', str(num_val))
            if clean_num and 5 <= len(clean_num) <= 18 and (not re.match('^\\d{8}$', clean_num)):
                otp = extract_otp_code(msg_val)
                if otp and len(msg_val) > 4:
                    results.append({'number': clean_num, 'message': msg_val, 'otp': otp, 'item_id': datetime_val})
    else:
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            if not rows:
                continue
            final_n_idx, final_m_idx = _find_header_column_indices(rows, n_col_name, m_col_name, n_idx, m_idx)
            for row in rows:
                cols = row.find_all(['td', 'th'])
                if all((c.name == 'th' for c in cols)):
                    continue
                if len(cols) > max(final_n_idx, final_m_idx):
                    num_text = cols[final_n_idx].get_text(separator=' ', strip=True)
                    msg_text = cols[final_m_idx].get_text(separator=' ', strip=True)
                    datetime_val = ''
                    for col in cols:
                        col_text = col.get_text(separator=' ', strip=True)
                        if re.search('\\d{4}[-/]\\d{2}[-/]\\d{2}', col_text) and re.search('\\d{2}:\\d{2}:\\d{2}', col_text):
                            datetime_val = col_text
                            break
                    if not datetime_val:
                        date_part = ''
                        time_part = ''
                        for col in cols:
                            col_text = col.get_text(separator=' ', strip=True)
                            if not date_part:
                                m = re.search('\\d{4}[-/]\\d{2}[-/]\\d{2}', col_text)
                                if m:
                                    date_part = m.group()
                            if not time_part:
                                m = re.search('\\d{2}:\\d{2}:\\d{2}', col_text)
                                if m:
                                    time_part = m.group()
                        datetime_val = f'{date_part} {time_part}'.strip()
                    clean_num = re.sub('\\D', '', num_text)
                    msg_text = re.sub('(?<!\\n)nn(?!\\n)', '\n', msg_text)
                    if clean_num and 5 <= len(clean_num) <= 18 and (not re.match('^\\d{8}$', clean_num)):
                        otp = extract_otp_code(msg_text)
                        if otp and len(msg_text) > 4:
                            results.append({'number': clean_num, 'message': msg_text, 'otp': otp, 'item_id': datetime_val})
    return (results, html_text)
user_active_sessions = {}
user_otp_delivery_active = {}
_bot_message_registry = {}
_bot_message_registry_lock = threading.Lock()
_reply_keyboard_message_registry = {}
_user_menu_message_registry = {}
_BOT_MESSAGE_TRACK_LIMIT = 100

# One-time fresh VPS reset: old JSON data is removed only on the first startup.
# After that, the marker prevents future bot restarts from deleting new data.
ONE_TIME_RESET_MARKER = '.first_vps_reset_done'

def reset_old_runtime_json_data_once():
    if os.path.exists(ONE_TIME_RESET_MARKER):
        return
    for _file in (DB_FILE, SEEN_OTPS_FILE, 'users_list.json', 'users_db.json', 'withdrawals_db.json', '2fa_saved.json'):
        try:
            if os.path.exists(_file):
                os.remove(_file)
                logger.info(f'Removed old runtime data: {_file}')
        except Exception as _e:
            logger.warning(f'Could not remove {_file}: {_e}')
    try:
        with open(ONE_TIME_RESET_MARKER, 'w', encoding='utf-8') as _marker:
            _marker.write('done')
        logger.info('One-time fresh VPS reset completed.')
    except Exception as _e:
        logger.warning(f'Could not create reset marker: {_e}')

reset_old_runtime_json_data_once()

def load_db():
    global number_batches, used_numbers_list, total_uploaded_stats, total_assigned_stats, recent_traffic, otp_received_numbers, nexa_assigned_numbers, voltx_assigned_numbers, stex_assigned_numbers, smsbower_assigned_numbers
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                raw_content = f.read()
            if not raw_content.strip():
                logger.warning('DB file is empty, starting fresh.')
                return
            data = json.loads(raw_content)
            saved_settings = data.get('bot_settings', {})
            for key, val in saved_settings.items():
                if key == 'custom_messages':
                    for m_key, m_val in val.items():
                        bot_settings['custom_messages'][m_key] = m_val
                else:
                    bot_settings[key] = val
            for m_key, m_val in DEFAULT_CUSTOM_MESSAGES.items():
                if m_key not in bot_settings['custom_messages']:
                    bot_settings['custom_messages'][m_key] = m_val
            number_batches = data.get('number_batches', {})
            for _b in number_batches.values():
                if isinstance(_b, dict):
                    try:
                        _b['rate'] = float(_b.get('rate', 0.0))
                    except (TypeError, ValueError):
                        _b['rate'] = 0.0
            used_numbers_list = data.get('used_numbers_list', [])
            total_uploaded_stats = data.get('total_uploaded_stats', 0)
            total_assigned_stats = data.get('total_assigned_stats', 0)
            recent_traffic = data.get('recent_traffic', [])
            nexa_assigned_numbers = data.get('nexa_assigned_numbers', {})
            voltx_assigned_numbers = data.get('voltx_assigned_numbers', {})
            stex_assigned_numbers = data.get('stex_assigned_numbers', {})
            smsbower_assigned_numbers = data.get('smsbower_assigned_numbers', {})
            otp_received_numbers = set(data.get('otp_received_numbers', []))
            migrated = False
            new_fj = []
            for entry in bot_settings.get('fj_channels', []):
                if isinstance(entry, str):
                    new_fj.append({'chat_id': entry, 'type': 'channel', 'title': entry, 'invite_link': '', 'is_private': False})
                    migrated = True
                else:
                    new_fj.append(entry)
            if migrated:
                bot_settings['fj_channels'] = new_fj
            # Monetary system is bot-side Taka (৳). Preserve existing withdrawal methods
            # and panel/API configuration; normalize legacy dollar-formatted custom messages.
            taka_normalized = False
            cm = bot_settings.get('custom_messages', {})
            for m_key, entry in list(cm.items()):
                if isinstance(entry, dict) and 'text' in entry:
                    txt = str(entry.get('text', ''))
                    if '$' in txt or 'USD' in txt or 'US$' in txt:
                        if m_key in DEFAULT_CUSTOM_MESSAGES:
                            cm[m_key]['text'] = DEFAULT_CUSTOM_MESSAGES[m_key]['text']
                            taka_normalized = True
            if taka_normalized:
                bot_settings['custom_messages'] = cm
                save_local_db()
                logger.info('Normalized legacy dollar-formatted messages to Taka')
            logger.info('Local DB loaded successfully')
        except Exception as e:
            logger.error(f'Error loading local DB: {e}')

def save_local_db():
    with _db_save_lock:
        try:
            local_data = {'bot_settings': copy.deepcopy(bot_settings), 'number_batches': copy.deepcopy(number_batches), 'used_numbers_list': list(used_numbers_list), 'total_uploaded_stats': total_uploaded_stats, 'total_assigned_stats': total_assigned_stats, 'recent_traffic': list(recent_traffic), 'nexa_assigned_numbers': dict(nexa_assigned_numbers), 'voltx_assigned_numbers': dict(voltx_assigned_numbers), 'stex_assigned_numbers': dict(stex_assigned_numbers), 'otp_received_numbers': list(otp_received_numbers) if otp_received_numbers else [], 'smsbower_assigned_numbers': dict(smsbower_assigned_numbers)}
            dir_name = os.path.dirname(os.path.abspath(DB_FILE))
            fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix='.tmp')
            try:
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    json.dump(local_data, f, indent=4)
                os.replace(tmp_path, DB_FILE)
            except Exception as e:
                try:
                    os.unlink(tmp_path)
                except Exception as unlink_err:
                    logger.warning(f'Temp file cleanup error: {unlink_err}')
                raise
        except Exception as e:
            logger.warning(f'DB save error: {e}')
load_db()

# Bangladesh-only monetary system: use Taka (BDT/৳) everywhere.
# Remove legacy India-specific withdrawal methods from saved settings.
try:
    _legacy_india_methods = {'upi', 'paytm', 'phonepe', 'gpay', 'google pay'}
    _saved_methods = bot_settings.get('w_methods', [])
    _bd_methods = [m for m in _saved_methods if str(m).strip().lower() not in _legacy_india_methods]
    bot_settings['w_methods'] = _bd_methods or ['bKash', 'Nagad', 'Rocket']
    _cm = bot_settings.get('custom_messages', {})
    for _m_key, _entry in _cm.items():
        if isinstance(_entry, dict) and 'text' in _entry:
            _txt = str(_entry['text'])
            _txt = _txt.replace('₹', '৳').replace('INR', '৳').replace('Rs.', '৳').replace('Rs ', '৳')
            _entry['text'] = _txt
    bot_settings['custom_messages'] = _cm
except Exception as _e:
    logger.warning(f'Taka currency normalization skipped: {_e}')

# Force the requested Balance layout instead of an older saved custom message.
bot_settings['custom_messages']['balance'] = DEFAULT_CUSTOM_MESSAGES['balance'].copy()
try:
    save_local_db()
except Exception as e:
    logger.warning(f'Balance layout save skipped: {e}')

# ================= AUTOMATIC DAILY BACKUP =================
BACKUP_DIR = 'backups'
BACKUP_INTERVAL_SECONDS = 24 * 60 * 60
BACKUP_KEEP_DAYS = 30
MONTHLY_BACKUP_DIR = os.path.join(BACKUP_DIR, 'monthly')
# Keep one backup from each month permanently.
BACKUP_FILES = [
    'bot_data.json', 'seen_otps.json', 'users_list.json',
    'users_db.json', 'withdrawals_db.json', '2fa_saved.json'
]

def create_automatic_backup():
    """Create one ZIP backup of all current JSON data files."""
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_path = os.path.join(BACKUP_DIR, f'backup_{timestamp}.zip')
        added = 0
        with zipfile.ZipFile(backup_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            for filename in BACKUP_FILES:
                if os.path.isfile(filename):
                    zf.write(filename, arcname=filename)
                    added += 1
        if added == 0:
            try:
                os.remove(backup_path)
            except OSError:
                pass
            logger.info('Automatic backup skipped: no JSON data files found yet.')
            return False
        logger.info(f'Automatic backup created: {backup_path} ({added} files)')
        # Keep daily backups for 30 days.
        cutoff = time.time() - (BACKUP_KEEP_DAYS * 24 * 60 * 60)
        for old in Path(BACKUP_DIR).glob('backup_*.zip'):
            try:
                if old.stat().st_mtime < cutoff:
                    old.unlink()
            except OSError:
                pass

        # Keep one permanent backup per month.
        os.makedirs(MONTHLY_BACKUP_DIR, exist_ok=True)
        month_key = datetime.now().strftime('%Y-%m')
        monthly_path = os.path.join(MONTHLY_BACKUP_DIR, f'monthly_{month_key}.zip')
        if not os.path.exists(monthly_path):
            with zipfile.ZipFile(monthly_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
                for filename in BACKUP_FILES:
                    if os.path.isfile(filename):
                        zf.write(filename, arcname=filename)
            logger.info(f'Permanent monthly backup created: {monthly_path}')
        return True
    except Exception as e:
        logger.error(f'Automatic backup error: {e}')
        return False

def automatic_backup_loop():
    """Backup immediately after startup, then every 24 hours."""
    while True:
        create_automatic_backup()
        time.sleep(BACKUP_INTERVAL_SECONDS)

TFA_DB_FILE = '2fa_saved.json'

def _load_2fa_saved():
    """Load persisted 2FA secrets from disk into user_2fa_saved."""
    global user_2fa_saved
    try:
        if os.path.exists(TFA_DB_FILE):
            with open(TFA_DB_FILE, 'r', encoding='utf-8') as f:
                raw = f.read().strip()
            if raw:
                loaded = json.loads(raw)
                user_2fa_saved = {int(k): v for k, v in loaded.items()} if isinstance(loaded, dict) else {}
    except Exception as e:
        logger.warning(f'2fa_saved load error: {e} — starting fresh')
        user_2fa_saved = {}

def _save_2fa_saved():
    """Atomically persist user_2fa_saved to disk."""
    try:
        snapshot = {str(k): v for k, v in user_2fa_saved.items()}
        dir_name = os.path.dirname(os.path.abspath(TFA_DB_FILE)) or '.'
        with tempfile.NamedTemporaryFile('w', dir=dir_name, delete=False, suffix='.tmp', encoding='utf-8') as tf:
            tmp_path = tf.name
            json.dump(snapshot, tf, ensure_ascii=False)
        os.replace(tmp_path, TFA_DB_FILE)
    except Exception as e:
        logger.warning(f'2fa_saved save error: {e}')
user_states = {}
temp_data = {}
user_cooldowns = {}
pending_withdrawals = {}
user_2fa_saved = {}
_load_2fa_saved()

def _cleanup_stale_sessions():
    """Remove stale entries from in-memory dicts to prevent memory leaks."""
    now = time.time()
    stale_cd = [k for k, v in list(user_cooldowns.items()) if now - v > 600]
    for k in stale_cd:
        user_cooldowns.pop(k, None)
    if len(user_states) > 5000:
        for k in list(user_states.keys())[:2000]:
            user_states.pop(k, None)
    if len(temp_data) > 5000:
        for k in list(temp_data.keys())[:2000]:
            temp_data.pop(k, None)
    if len(pending_withdrawals) > 500:
        old_keys = list(pending_withdrawals.keys())[:-500]
        for k in old_keys:
            pending_withdrawals.pop(k, None)
    if len(user_2fa_saved) > 2000:
        for k in list(user_2fa_saved.keys())[:500]:
            user_2fa_saved.pop(k, None)

def _cleanup_loop():
    """Background thread: memory cleanup har 5 minute mein."""
    while True:
        time.sleep(300)
        try:
            _cleanup_stale_sessions()
        except Exception as e:
            logger.warning(f'_cleanup_stale_sessions error: {e}')

def _show_2fa_list(chat_id, msg_id):
    saved = user_2fa_saved.get(chat_id, [])
    _reset_btn_counter()
    if not saved:
        txt = (
            f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"《 📋 <b>MY 2FA ADDED</b> 》\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"😔 No 2FA codes are saved yet.\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"💡 First, use <b>Generate 2FA Code</b>,\n"
            f"your code will be saved automatically.\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖"
        )
        kb = {"inline_keyboard": [
            [{"text": "Generate 2FA Code", "icon_custom_emoji_id": "5353022963132174959", "callback_data": "gen_2fa", "style": _rs()}],
            [{"text": "Back", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "cancel_2fa", "style": _rs()}]
        ]}
    else:
        txt = (
            f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"《 📋 <b>MY 2FA ADDED</b> 》\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"✅ You have <b>{len(saved)}</b> 2FA code(s) saved.\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"💡 For recovery, any account can be used.\n"
            f"Generate the code or view the Secret Key.\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖"
        )
        list_kb = []
        for i, entry in enumerate(saved):
            list_kb.append([
                {"text": f"{entry['name']}", "icon_custom_emoji_id": "5353022963132174959", "callback_data": f"gen_saved_2fa_{i}", "style": _rs()},
                {"text": "Del", "icon_custom_emoji_id": "5422557736330106570", "callback_data": f"del_2fa_{i}", "style": _rs()}
            ])
        list_kb.append([{"text": "Add New", "icon_custom_emoji_id": "5352552689983067014", "callback_data": "gen_2fa", "style": _rs()}])
        list_kb.append([{"text": "Back", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "cancel_2fa", "style": _rs()}])
        kb = {"inline_keyboard": list_kb}
    edit_message(chat_id, msg_id, render_body_text(txt), reply_markup=kb)

tg_session = requests.Session()
_tg_adapter = requests.adapters.HTTPAdapter(max_retries=2, pool_connections=4, pool_maxsize=20)
tg_session.mount('https://', _tg_adapter)
tg_session.mount('http://', _tg_adapter)

def api_call(method, payload=None):
    url = f'{BASE_URL}/{method}'
    try:
        if payload is None and '?' in method:
            res = tg_session.get(url, timeout=40)
        else:
            res = tg_session.post(url, json=payload, timeout=15)
        try:
            return res.json()
        except ValueError:
            logger.warning(f'Telegram API non-JSON response [{method}]: {res.status_code} {res.text[:100]}')
            return {}
    except requests.exceptions.ConnectionError as e:
        logger.warning(f'Telegram connection error [{method}]: {e}')
        return {}
    except Exception as e:
        logger.warning(f'Telegram API call failed [{method}]: {e}')
        return {}

def _apply_text_overrides(text) -> str:
    """Har outgoing message text mein sys_emoji_overrides apply karo.
    Yeh ensure karta hai ki chahe render_body_text call hua ho ya nahi,
    emoji IDs hamesha latest admin override se replace honge."""
    overrides = bot_settings.get('sys_emoji_overrides', {})
    if not overrides or not text:
        return str(text) if text is not None else ''
    id_map = _build_id_override_map(overrides)
    if not id_map:
        return str(text)

    def _replace_eid(m):
        eid = m.group(1)
        return f'emoji-id="{id_map.get(eid, eid)}"'
    return re.sub('emoji-id="(\\d+)"', _replace_eid, str(text))

def _force_navigation_button_colors(reply_markup):
    """Keep every Back/Close/Cancel navigation button red (danger).
    This is applied at send/edit time so existing and dynamically-built keyboards
    all follow the same rule without changing their callbacks or other buttons.
    """
    if not isinstance(reply_markup, dict):
        return reply_markup
    rm = copy.deepcopy(reply_markup)
    nav_words = {'back', 'back to admin', 'back to menus', 'back to providers', 'back to groups', 'back to list', 'back to system', 'back to balance', 'close', 'cancel', 'cancle', 'cross', 'x', 'cLose'.lower()}

    def patch(btn):
        if not isinstance(btn, dict):
            return
        text = str(btn.get('text', '')).strip().lower()
        if text in nav_words or text.startswith('back') or text in {'✕ close', '❌ close', '❌', '✖ close'}:
            btn['style'] = 'danger'
    for key in ('inline_keyboard', 'keyboard'):
        rows = rm.get(key)
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, list):
                    for btn in row:
                        patch(btn)
    return rm

def send_message(chat_id, text, reply_markup=None, parse_mode='HTML', protect_from_menu_cleanup=False):
    payload = {'chat_id': chat_id, 'text': _apply_text_overrides(text), 'parse_mode': parse_mode, 'disable_web_page_preview': True}
    if reply_markup:
        payload['reply_markup'] = _force_navigation_button_colors(_apply_emoji_overrides(reply_markup))
    resp = api_call('sendMessage', payload)
    if isinstance(chat_id, int) and chat_id > 0 and isinstance(resp, dict) and resp.get('ok'):
        msg_id = resp.get('result', {}).get('message_id')
        if msg_id:
            if not protect_from_menu_cleanup:
                with _bot_message_registry_lock:
                    ids = _bot_message_registry.setdefault(chat_id, [])
                    ids.append(msg_id)
                    if len(ids) > _BOT_MESSAGE_TRACK_LIMIT:
                        del ids[:-_BOT_MESSAGE_TRACK_LIMIT]
            if isinstance(reply_markup, dict) and reply_markup.get('keyboard'):
                _reply_keyboard_message_registry[chat_id] = msg_id
    return resp

def edit_message(chat_id, message_id, text, reply_markup=None, parse_mode='HTML'):
    payload = {'chat_id': chat_id, 'message_id': message_id, 'text': _apply_text_overrides(text), 'parse_mode': parse_mode, 'disable_web_page_preview': True}
    if reply_markup:
        payload['reply_markup'] = _force_navigation_button_colors(_apply_emoji_overrides(reply_markup))
    resp = api_call('editMessageText', payload)
    if not resp or not resp.get('ok'):
        raise RuntimeError(f'editMessageText failed: {resp}')
    return resp

def _paced_edit(chat_id, msg_id, text, target_gap):
    """Edit message with simple 429 retry."""
    t0 = time.monotonic()
    try:
        resp = edit_message(chat_id, msg_id, text, parse_mode='HTML')
    except RuntimeError as e:
        if '429' in str(e):
            time.sleep(1.1)
            try:
                edit_message(chat_id, msg_id, text, parse_mode='HTML')
            except Exception as retry_err:
                logger.warning(f'Retry edit failed: {retry_err}')
        else:
            logger.warning(f'Edit failed: {e}')
    except Exception as e:
        logger.warning(f'Edit failed: {e}')
    elapsed = time.monotonic() - t0
    remaining = target_gap - elapsed
    if remaining > 0:
        time.sleep(remaining)

def send_typing_animation(chat_id, first_name):
    """Simple startup animation requested by the owner.

    The startup message now animates the progress bar and finishes with:
    BOT IS READY
    ▓▓▓▓▓▓▓▓▓▓ 100%
    """
    _PEM_CHECK = '<tg-emoji emoji-id="6266994443262367483">✅</tg-emoji>'
    _FRAMES = [('░░░░░░░░░░', '0%'), ('▓▓▓░░░░░░░', '30%'), ('▓▓▓▓▓▓░░░░', '60%'), ('▓▓▓▓▓▓▓▓▓▓', '100%')]
    resp = send_message(chat_id, render_body_text('<b>BOT IS READY</b>\n░░░░░░░░░░ 0%'), protect_from_menu_cleanup=True)
    if not resp or not resp.get('ok'):
        return None
    msg_id = resp['result']['message_id']
    for bar, pct in _FRAMES[1:]:
        label = f'{_PEM_CHECK} <b>BOT IS READY</b>' if pct == '100%' else '<b>BOT IS READY</b>'
        _paced_edit(chat_id, msg_id, render_body_text(f'{label}\n{bar} {pct}'), target_gap=0.3)
    return msg_id
_previous_start_pair = {}
_previous_reply_keyboard = {}
_previous_reply_keyboard_lock = threading.Lock()

def _remember_reply_keyboard(chat_id, message_id):
    with _previous_reply_keyboard_lock:
        old = _previous_reply_keyboard.get(chat_id)
        _previous_reply_keyboard[chat_id] = message_id
        return old

def _delete_old_reply_keyboard(chat_id, message_id):
    if not message_id:
        return
    try:
        delete_message(chat_id, message_id)
    except Exception:
        pass
_previous_start_pair_lock = threading.Lock()

def _remember_start_pair(chat_id, animation_msg_id, welcome_msg_id):
    """Save the newest completed /start pair and return the previous pair."""
    with _previous_start_pair_lock:
        old = dict(_previous_start_pair.get(chat_id) or {})
        _previous_start_pair[chat_id] = {'animation': animation_msg_id, 'welcome': welcome_msg_id}
        return old

def _delete_old_start_pair(chat_id, pair):
    """Delete the previous /start pair only after the new pair is ready.

    Both stored values are raw Telegram message IDs.
    """
    if not pair:
        return
    old_animation = pair.get('animation')
    if old_animation:
        try:
            delete_message(chat_id, old_animation)
        except Exception:
            pass
    old_welcome = pair.get('welcome')
    if old_welcome:
        try:
            delete_message(chat_id, old_welcome)
        except Exception:
            pass
_active_welcomes = set()
_active_welcomes_lock = threading.Lock()

def _welcome_user(chat_id, first_name, start_user_msg_id=None):
    """Start flow: keep the user /start message visible until animation and Welcome are complete."""
    with _active_welcomes_lock:
        if chat_id in _active_welcomes:
            return
        _active_welcomes.add(chat_id)
    try:
        get_user(chat_id)
        _process_pending_referral(chat_id)
        animation_msg_id = send_typing_animation(chat_id, first_name)
        safe_name = html.escape(str(first_name))
        start_cfg = bot_settings.get('custom_messages', {}).get('start', {})
        start_text = start_cfg.get('text') or DEFAULT_CUSTOM_MESSAGES['start']['text']
        start_text = str(start_text).replace('{name}', safe_name).replace('{first_name}', safe_name)
        welcome_resp = send_message(chat_id, render_body_text(start_text), reply_markup=main_menu(chat_id), protect_from_menu_cleanup=True)
        if not welcome_resp or not welcome_resp.get('ok'):
            return
        welcome_msg_id = welcome_resp['result']['message_id']
        old_pair = _remember_start_pair(chat_id, animation_msg_id, welcome_msg_id)
        if old_pair:
            time.sleep(0.12)
            _delete_old_start_pair(chat_id, old_pair)
    finally:
        with _active_welcomes_lock:
            _active_welcomes.discard(chat_id)

def delete_message(chat_id, message_id):
    return api_call('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})

def cleanup_user_menu_messages(chat_id, current_user_msg_id=None):
    """Stop old active sessions without deleting Reply Keyboard or /start/menu messages.

    Reply Keyboard navigation must not remove the message that introduced the
    keyboard or the user's /start command. Each button tap creates its own
    single bot response, matching the original chat behavior.
    """
    session = user_active_sessions.pop(chat_id, None)
    user_otp_delivery_active[chat_id] = False
    if session:
        for num in session.get('nums', []):
            nexa_assigned_numbers.pop(num, None)
            voltx_assigned_numbers.pop(num, None)
            stex_assigned_numbers.pop(num, None)
        try:
            save_local_db()
        except Exception as e:
            logger.warning(f'Menu cleanup DB save error: {e}')
    keyboard_msg_id = _reply_keyboard_message_registry.get(chat_id)
    with _bot_message_registry_lock:
        ids = list(_bot_message_registry.pop(chat_id, []))
    with _previous_start_pair_lock:
        protected_start_pair = dict(_previous_start_pair.get(chat_id) or {})
    protected_start_ids = {protected_start_pair.get('animation'), protected_start_pair.get('welcome')}
    protected_start_ids.discard(None)
    old_bot_ids = []
    for old_msg_id in ids:
        if keyboard_msg_id and old_msg_id == keyboard_msg_id:
            continue
        if old_msg_id in protected_start_ids:
            continue
        old_bot_ids.append(old_msg_id)
    return

def answer_callback(callback_id, text='', show_alert=False):
    api_call('answerCallbackQuery', {'callback_query_id': callback_id, 'text': text, 'show_alert': show_alert})

def send_document(chat_id, filename, text_content):
    url = f'{BASE_URL}/sendDocument'
    files = {'document': (filename, text_content)}
    data = {'chat_id': chat_id}
    try:
        tg_session.post(url, data=data, files=files, timeout=30)
    except Exception as e:
        logger.warning(f'send_document error: {e}')
all_known_users = set()
_users_set_lock = threading.Lock()

def sync_users_list():
    global all_known_users
    try:
        if os.path.exists('users_list.json'):
            with open('users_list.json', 'r') as f:
                # Normalize every ID to str; old files may contain integer IDs while
                # runtime registration uses strings, which could otherwise cause the
                # same user to receive the startup ONLINE message twice.
                all_known_users = {str(uid) for uid in json.load(f)}
        if not all_known_users and local_users_db:
            all_known_users = set((str(k) for k in local_users_db.keys()))
            with open('users_list.json', 'w') as f:
                json.dump(list(all_known_users), f)
    except Exception as e:
        logger.warning(f'sync_users_list error: {e}')

def _save_users_list():
    try:
        fd, tmp_path = tempfile.mkstemp(dir='.', suffix='.tmp')
        try:
            with os.fdopen(fd, 'w') as f:
                json.dump(list(all_known_users), f)
            os.replace(tmp_path, 'users_list.json')
        except Exception:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
            raise
    except Exception as e:
        logger.warning(f'_save_users_list error: {e}')

def register_user_local(uid):
    uid_str = str(uid)
    with _users_set_lock:
        if uid_str not in all_known_users:
            all_known_users.add(uid_str)
            threading.Thread(target=_save_users_list, daemon=True).start()
USERS_DB_FILE = 'users_db.json'
WITHDRAWALS_DB_FILE = 'withdrawals_db.json'
local_users_db = {}
local_withdrawals_db = {}
_users_db_lock = threading.Lock()

def _load_local_users_db():
    global local_users_db, local_withdrawals_db
    try:
        if os.path.exists(USERS_DB_FILE):
            with open(USERS_DB_FILE, 'r', encoding='utf-8') as f:
                raw = f.read()
            if raw.strip():
                local_users_db = json.loads(raw)
    except Exception as e:
        logger.warning(f'users_db load error: {e} — starting fresh')
        local_users_db = {}
    try:
        if os.path.exists(WITHDRAWALS_DB_FILE):
            with open(WITHDRAWALS_DB_FILE, 'r', encoding='utf-8') as f:
                raw = f.read()
            if raw.strip():
                local_withdrawals_db = json.loads(raw)
    except Exception as e:
        logger.warning(f'withdrawals_db load error: {e} — starting fresh')
        local_withdrawals_db = {}

def _save_local_users_db():
    try:
        with _users_db_lock:
            snapshot = dict(local_users_db)
        dir_name = os.path.dirname(os.path.abspath(USERS_DB_FILE))
        fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix='.tmp')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(snapshot, f, indent=2)
            os.replace(tmp_path, USERS_DB_FILE)
        except Exception:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
            raise
    except Exception as e:
        logger.warning(f'_save_local_users_db error: {e}')
_withdrawals_db_lock = threading.Lock()

def _save_local_withdrawals_db():
    try:
        with _withdrawals_db_lock:
            snapshot = dict(local_withdrawals_db)
        dir_name = os.path.dirname(os.path.abspath(WITHDRAWALS_DB_FILE))
        fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix='.tmp')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(snapshot, f, indent=2)
            os.replace(tmp_path, WITHDRAWALS_DB_FILE)
        except Exception:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
            raise
    except Exception as e:
        logger.warning(f'_save_local_withdrawals_db error: {e}')
_load_local_users_db()
threading.Thread(target=sync_users_list, daemon=True).start()

def _new_user_dict(user_id):
    """Default user record — ek jagah define, teen jagah use. Duplicate hat gaya."""
    return {'user_id': int(user_id), 'balance': 0.0, 'total_refers': 0, 'total_otps': 0, 'banned': False, 'verified': False}

def _get_local_user(user_id):
    uid = str(user_id)
    with _users_db_lock:
        if uid not in local_users_db:
            local_users_db[uid] = _new_user_dict(user_id)
            threading.Thread(target=_save_local_users_db, daemon=True).start()
        return dict(local_users_db[uid])

def _update_local_user(user_id, updates):
    uid = str(user_id)
    with _users_db_lock:
        if uid not in local_users_db:
            local_users_db[uid] = _new_user_dict(user_id)
        local_users_db[uid].update(updates)
    threading.Thread(target=_save_local_users_db, daemon=True).start()

def _increment_local_user(user_id, field, amount):
    uid = str(user_id)
    with _users_db_lock:
        if uid not in local_users_db:
            local_users_db[uid] = _new_user_dict(user_id)
        local_users_db[uid][field] = local_users_db[uid].get(field, 0) + amount
    threading.Thread(target=_save_local_users_db, daemon=True).start()

def _save_local_withdrawal(req_id, data):
    local_withdrawals_db[req_id] = data
    local_withdrawals_db[req_id]['timestamp'] = time.time()
    threading.Thread(target=_save_local_withdrawals_db, daemon=True).start()

def _update_local_withdrawal(req_id, updates):
    if req_id in local_withdrawals_db:
        local_withdrawals_db[req_id].update(updates)
        threading.Thread(target=_save_local_withdrawals_db, daemon=True).start()

def _broadcast_parallel(users, worker, max_workers=25):
    """Send broadcasts concurrently for faster delivery while avoiding excessive API pressure."""
    success = 0
    failed = 0
    lock = threading.Lock()

    def run_one(user_id):
        nonlocal success, failed
        try:
            ok = worker(user_id)
        except Exception:
            ok = False
        with lock:
            if ok:
                success += 1
            else:
                failed += 1

    workers = min(max_workers, max(1, len(users)))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        list(executor.map(run_one, users))
    return success, failed

def broadcast_copymessage(from_chat_id, msg_id):
    users = list(all_known_users)
    def worker(user_id):
        payload = {'chat_id': user_id, 'from_chat_id': from_chat_id, 'message_id': msg_id}
        try:
            res = tg_session.post(f'{BASE_URL}/copyMessage', json=payload, timeout=10).json()
            return bool(res.get('ok'))
        except Exception:
            return False
    success, failed = _broadcast_parallel(users, worker, max_workers=25)
    send_message(from_chat_id, render_body_text(f'📢 <b>Broadcast Completed!</b>\n✅ Success: {success}\n❌ Failed: {failed}\n👥 Total Sent: {len(users)}'))

def broadcast_text_message(txt):
    """Broadcast plain text/HTML concurrently for faster large-user delivery."""
    users = list(all_known_users)
    body = _apply_text_overrides(txt)
    def worker(user_id):
        try:
            res = tg_session.post(f'{BASE_URL}/sendMessage', json={'chat_id': user_id, 'text': body, 'parse_mode': 'HTML', 'disable_web_page_preview': True}, timeout=10).json()
            return bool(res.get('ok'))
        except Exception:
            return False
    success, failed = _broadcast_parallel(users, worker, max_workers=25)
    logger.info(f'Broadcast: {success} sent, {failed} failed')
_STYLES = ['primary', 'success', 'danger']
_tl = threading.local()

def _reset_btn_counter():
    """Reset THIS thread's counter to 0 (primary). Call at start of every keyboard builder."""
    _tl.i = 0

def _get_service_emoji_id(srv, apps_db):
    """Service name (WHATSAPP, TELEGRAM, ...) ke liye premium-emoji id dhundo.
    Nexa/VoltX/Stex teen jagah yeh exact same lookup duplicate tha — ab shared."""
    emoji_id = '5257969839313526622'
    for app_key, app_data in apps_db.items():
        if srv.upper() == app_key or srv.upper() in app_key or app_key in srv.upper():
            if 'id' in app_data:
                emoji_id = app_data['id']
                break
    return emoji_id

def _download_telegram_txt_document(chat_id, doc):
    """Download a text document used by the admin emoji/flag upload tools."""
    if not str(doc.get('file_name', '')).lower().endswith('.txt'):
        send_message(chat_id, render_body_text(f"{PEM['no']} Please upload a .txt file only."))
        return None
    file_id = doc['file_id']
    try:
        file_info = tg_session.get(f'{BASE_URL}/getFile?file_id={file_id}', timeout=15).json()
    except ValueError:
        send_message(chat_id, render_body_text(f"{PEM['no']} Could not download the file. Please try again."))
        return None
    if not file_info.get('ok') or not file_info.get('result', {}).get('file_path'):
        send_message(chat_id, render_body_text(f"{PEM['no']} Could not get the file path from Telegram. Please try again."))
        return None
    file_path = file_info['result']['file_path']
    try:
        return tg_session.get(f'{FILE_URL}{file_path}', timeout=30).text
    except Exception:
        send_message(chat_id, render_body_text(f"{PEM['no']} Could not download the file. Please try again."))
        return None

def _download_telegram_number_document(chat_id, doc):
    """Download an Admin Panel number file and normalize TXT/CSV into number lines."""
    filename = str(doc.get('file_name', '')).strip()
    ext = Path(filename).suffix.lower()
    if ext not in {'.txt', '.csv'}:
        send_message(chat_id, render_body_text(f"{PEM['no']} Unsupported file type. Please upload a .txt or .csv file."))
        return None
    file_id = doc.get('file_id')
    try:
        file_info = tg_session.get(f'{BASE_URL}/getFile?file_id={file_id}', timeout=15).json()
        file_path = file_info.get('result', {}).get('file_path')
        if not file_info.get('ok') or not file_path:
            raise RuntimeError('Telegram did not return a file path')
        response = tg_session.get(f'{FILE_URL}{file_path}', timeout=30)
        response.raise_for_status()
        raw = response.content.decode('utf-8-sig', errors='replace')
    except Exception as e:
        logger.warning(f'Number file download failed: {e}')
        send_message(chat_id, render_body_text(f"{PEM['no']} Could not download the file. Please try again."))
        return None
    if ext == '.txt':
        return raw.splitlines()
    rows = list(csv.reader(io.StringIO(raw)))
    if not rows:
        return []
    aliases = {'number', 'phone', 'phone number', 'mobile', 'mobile number', 'msisdn', 'telephone', 'tel', 'recipient', 'recipient number', 'contact', 'num', 'phone_number', 'mobile_number'}
    header = [str(x).strip().lower().replace('-', ' ').replace('_', ' ') for x in rows[0]]
    candidate_indexes = [i for i, h in enumerate(header) if h in aliases or 'phone' in h or 'mobile' in h or (h == 'msisdn')]
    data_rows = rows[1:] if candidate_indexes else rows
    cells = []
    if candidate_indexes:
        for row in data_rows:
            for i in candidate_indexes:
                if i < len(row):
                    cells.append(row[i])
    else:
        for row in data_rows:
            cells.extend(row)
    numbers = []
    seen = set()
    for cell in cells:
        value = str(cell).strip()
        if not value:
            continue
        cleaned = re.sub('[\\s().-]', '', value)
        if cleaned.startswith('+'):
            digits = '+' + re.sub('\\D', '', cleaned[1:])
        else:
            digits = re.sub('\\D', '', cleaned)
        raw_digits = digits[1:] if digits.startswith('+') else digits
        if not 5 <= len(raw_digits) <= 18:
            continue
        if len(raw_digits) == 8 and re.match('^(19|20)\\d{6}$', raw_digits):
            continue
        if digits not in seen:
            seen.add(digits)
            numbers.append(digits)
    return numbers
_NUMBER_COL_ALIASES = ('number', 'mobile', 'phone', 'msisdn', 'num', 'recipient', 'to')
_MESSAGE_COL_ALIASES = ('message', 'sms', 'text', 'content', 'msg', 'body')

def _find_header_column_indices(rows, n_col_name, m_col_name, default_n_idx, default_m_idx):
    """HTML table ki pehli row (header) mein column-name se number/message column ka
    real index dhundo. Nahi mile to caller ke diye gaye default index use hote hain.
    Do jagah (AJAX-backup path aur Auto Captcha panel path) yeh exact same header-scan
    logic duplicate tha — ab shared.

    FIX: Bahut saare panels column ka header "SMS" likhte hain, "Message" nahi — aur
    number wale column ko "Mobile"/"Phone" bhi likh sakte hain. Pehle sirf exact
    n_col_name/m_col_name (jo panel-config mein set hai, default "number"/"message")
    match hota tha — agar panel ka header text usse alag hota (jaise "SMS"), match
    fail ho jaata aur ghalat column select ho jaata (isi wajah se "Connected, but
    couldn't parse OTP data!" milta tha, jabki panel mein data sahi tha).
    Ab hum configured name ko PEHLE priority dete hain, phir known aliases try karte
    hain — taaki 'SMS' jaisa header bhi 'message' ke barabar detect ho."""
    final_n_idx, final_m_idx = (default_n_idx, default_m_idx)
    if not rows:
        return (final_n_idx, final_m_idx)
    header_cells = rows[0].find_all(['th', 'td'])
    header_texts = [cell.get_text(strip=True).lower() for cell in header_cells]
    n_candidates = [n_col_name] + [a for a in _NUMBER_COL_ALIASES if a != n_col_name]
    m_candidates = [m_col_name] + [a for a in _MESSAGE_COL_ALIASES if a != m_col_name]
    for candidate in n_candidates:
        matched = [i for i, c_text in enumerate(header_texts) if candidate in c_text]
        if matched:
            final_n_idx = matched[0]
            break
    for candidate in m_candidates:
        matched = [i for i, c_text in enumerate(header_texts) if candidate in c_text]
        if matched:
            final_m_idx = matched[0]
            break
    return (final_n_idx, final_m_idx)

def _rs():
    """Return next style (primary→success→danger→...) for THIS thread. Auto-inits if needed."""
    if not hasattr(_tl, 'i'):
        _tl.i = 0
    s = _STYLES[_tl.i % 3]
    _tl.i += 1
    return s

def render_body_text(text):
    if not text:
        return str(text)
    parts = re.split('(<tg-emoji.*?</tg-emoji>)', str(text))
    for i in range(len(parts)):
        if not parts[i].startswith('<tg-emoji'):
            for normal_emj, prem_id in GLOBAL_BODY_EMOJIS.items():
                if normal_emj in parts[i]:
                    parts[i] = parts[i].replace(normal_emj, f'<tg-emoji emoji-id="{prem_id}">{normal_emj}</tg-emoji>')
    return _apply_text_overrides(''.join(parts))

def extract_premium_html(msg):
    text = msg.get('text', msg.get('caption', ''))
    entities = msg.get('entities', msg.get('caption_entities', []))
    if not entities:
        return text
    try:
        b_text = text.encode('utf-16-le')
        c_entities = [e for e in entities if e.get('type') == 'custom_emoji']
        c_entities.sort(key=lambda x: x['offset'], reverse=True)
        for ent in c_entities:
            offset = ent['offset'] * 2
            length = ent['length'] * 2
            eid = ent['custom_emoji_id']
            emoji_char = b_text[offset:offset + length].decode('utf-16-le')
            html_tag = f'<tg-emoji emoji-id="{eid}">{emoji_char}</tg-emoji>'
            replacement = html_tag.encode('utf-16-le')
            b_text = b_text[:offset] + replacement + b_text[offset + length:]
        return b_text.decode('utf-16-le')
    except Exception as e:
        return text
_COUNTRY_CALLING_ISO = {'1': 'US', '1246': 'BB', '1264': 'AI', '1268': 'AG', '1345': 'KY', '1441': 'BM', '1473': 'GD', '1664': 'MS', '1670': 'MP', '1671': 'GU', '1684': 'AS', '1758': 'LC', '1767': 'DM', '1784': 'VC', '1787': 'PR', '1809': 'DO', '1829': 'DO', '1849': 'DO', '1868': 'TT', '1869': 'KN', '1876': 'JM', '1939': 'PR', '20': 'EG', '211': 'SS', '212': 'EH', '213': 'DZ', '216': 'TN', '218': 'LY', '221': 'SN', '222': 'MR', '223': 'ML', '224': 'GN', '226': 'BF', '227': 'NE', '228': 'TG', '229': 'BJ', '230': 'MU', '231': 'LR', '232': 'SL', '233': 'GH', '234': 'NG', '235': 'TD', '236': 'CF', '237': 'CM', '240': 'GQ', '241': 'GA', '244': 'AO', '245': 'GW', '246': 'IO', '248': 'SC', '249': 'SD', '250': 'RW', '251': 'ET', '252': 'SO', '253': 'DJ', '254': 'KE', '256': 'UG', '257': 'BI', '258': 'MZ', '260': 'ZM', '261': 'MG', '262': 'YT', '263': 'ZW', '264': 'NA', '265': 'MW', '266': 'LS', '267': 'BW', '269': 'KM', '27': 'ZA', '291': 'ER', '297': 'AW', '298': 'FO', '299': 'GL', '30': 'GR', '31': 'NL', '32': 'BE', '33': 'FR', '34': 'ES', '350': 'GI', '351': 'PT', '352': 'LU', '353': 'IE', '354': 'IS', '355': 'AL', '356': 'MT', '357': 'CY', '358': 'FI', '359': 'BG', '36': 'HU', '370': 'LT', '371': 'LV', '372': 'EE', '374': 'AM', '375': 'BY', '377': 'MC', '378': 'SM', '380': 'UA', '381': 'RS', '385': 'HR', '386': 'SI', '387': 'BA', '39': 'IT', '40': 'RO', '41': 'CH', '421': 'SK', '423': 'LI', '43': 'AT', '44': 'GB', '45': 'DK', '46': 'SE', '47': 'NO', '4779': 'SJ', '48': 'PL', '49': 'DE', '500': 'GS', '501': 'BZ', '502': 'GT', '503': 'SV', '504': 'HN', '505': 'NI', '506': 'CR', '507': 'PA', '508': 'PM', '509': 'HT', '51': 'PE', '52': 'MX', '53': 'CU', '54': 'AR', '55': 'BR', '56': 'CL', '57': 'CO', '590': 'GP', '592': 'GY', '593': 'EC', '594': 'GF', '595': 'PY', '596': 'MQ', '597': 'SR', '598': 'UY', '60': 'MY', '61': 'AU', '62': 'ID', '63': 'PH', '64': 'NZ', '65': 'SG', '66': 'TH', '672': 'NF', '674': 'NR', '675': 'PG', '676': 'TO', '677': 'SB', '678': 'VU', '679': 'FJ', '680': 'PW', '681': 'WF', '682': 'CK', '683': 'NU', '685': 'WS', '686': 'KI', '687': 'NC', '688': 'TV', '689': 'PF', '690': 'TK', '692': 'MH', '7': 'RU', '76': 'KZ', '77': 'KZ', '81': 'JP', '852': 'HK', '855': 'KH', '856': 'LA', '86': 'CN', '880': 'BD', '91': 'IN', '92': 'PK', '93': 'AF', '94': 'LK', '960': 'MV', '961': 'LB', '962': 'JO', '963': 'SY', '964': 'IQ', '965': 'KW', '966': 'SA', '967': 'YE', '968': 'OM', '971': 'AE', '972': 'IL', '973': 'BH', '974': 'QA', '975': 'BT', '976': 'MN', '977': 'NP', '992': 'TJ', '993': 'TM', '994': 'AZ', '995': 'GE', '996': 'KG', '998': 'UZ'}

def _unicode_flag(iso):
    iso = str(iso or '').upper()
    if len(iso) != 2 or not iso.isalpha():
        return '🌍'
    return ''.join((chr(127462 + ord(ch) - 65) for ch in iso))

def get_flag_info_from_num(num):
    clean = str(num).replace('+', '').replace(' ', '').replace('-', '')

    # Local Bangladeshi mobile numbers (01XXXXXXXXX) do not contain +880.
    # Recognize them here so Test/Panel messages show 🇧🇩 instead of 🌍.
    if re.fullmatch(r'01\d{9}', clean):
        iso = 'BD'
        for code, data in bot_settings.get('premium_flags', {}).items():
            if str(data.get('iso') or '').upper() == iso:
                char = data.get('char') or _unicode_flag(iso)
                eid = data.get('id')
                return (char, iso, eid)
        return (_unicode_flag(iso), iso, None)

    sorted_codes = sorted(bot_settings.get('premium_flags', {}).keys(), key=len, reverse=True)
    for code in sorted_codes:
        if clean.startswith(str(code)):
            data = bot_settings['premium_flags'][code]
            iso = str(data.get('iso') or '').upper()
            if not iso:
                iso = _COUNTRY_CALLING_ISO.get(str(code), '')
            char = data.get('char') or _unicode_flag(iso)
            return (char, iso or '', data.get('id'))
    for code in sorted(_COUNTRY_CALLING_ISO.keys(), key=len, reverse=True):
        if clean.startswith(code):
            iso = _COUNTRY_CALLING_ISO[code]
            return (_unicode_flag(iso), iso, None)
    return ('🌍', '', '5204160805402080246')

def get_flag_and_code(num):
    char, iso, _ = get_flag_info_from_num(num)
    return (char, iso)

def _get_cc_from_iso(iso):
    """Return country-code digits for a given ISO-2 code (e.g. 'MG' → '261'), or None."""
    for code, data in bot_settings.get('premium_flags', {}).items():
        if data.get('iso') == iso:
            return code
    return None

def _get_cc_from_num(num_str):
    """Return country-code digits embedded at the start of num_str, or None."""
    clean = str(num_str).replace('+', '').replace(' ', '')
    sorted_codes = sorted(bot_settings.get('premium_flags', {}).keys(), key=len, reverse=True)
    for code in sorted_codes:
        if clean.startswith(code):
            return code
    return None

def get_flag_info_html(num_or_iso):
    if len(num_or_iso) == 2:
        for code, data in bot_settings.get('premium_flags', {}).items():
            if data.get('iso') == num_or_iso:
                eid = data.get('id')
                char = data.get('char')
                if eid:
                    return f'<tg-emoji emoji-id="{eid}">{char}</tg-emoji>'
                return char
        return '🌍'
    char, _, eid = get_flag_info_from_num(num_or_iso)
    if eid:
        return f'<tg-emoji emoji-id="{eid}">{char}</tg-emoji>'
    return char
_MASK_EMOJI = '<tg-emoji emoji-id="6228781436330054904">⭐</tg-emoji>'
_END_NUMBER_EMOJI = '<tg-emoji emoji-id="4958728373900674046">🔥</tg-emoji>'
_OTP_COPY_EMOJI_ID = '6266995104687330978'
_OTP_BOX_PAD = '\u2003' * 30  # em spaces give the SMS line enough invisible width to visually match the inline button row

def _otp_box_message(first_line_html, lang_line=''):
    """Build OTP forward text with a invisible fixed-width padding so the SMS bubble visually
    matches the width of the inline button row. Padding is invisible to users."""
    return render_body_text(f'<b>{first_line_html}{_OTP_BOX_PAD}</b>{lang_line}')


def mask_number(num, user_id=None):
    clean = num.replace('+', '').replace(' ', '')
    tag = _MASK_EMOJI
    if len(clean) > 6:
        return f'{clean[:3]}✦{tag}✦{clean[-3:]}'
    elif len(clean) > 2:
        return f'{clean[:1]}✦{tag}✦{clean[-1:]}'
    return clean
SERVICE_SMS_KEYWORDS = {'whatsapp': ['whatsapp', 'wa', 'wap', 'w/a', 'whatsapp business', 'wa.me', 'wa code', 'wh', 'واتساب', 'واتساپ', 'واٹس ایپ', 'व्हाट्सएप', 'वाट्सएप', 'वॉट्सऐप', 'व्हाट्सप्प', 'হোয়াটসঅ্যাপ', 'হোটসঅ্যাপ', 'ватсап', 'уотсап', 'вотсап', 'ватс апп', 'వాట్సాప్', 'വാട്\u200cസ്ആപ്പ്', 'வாட்ஸ்அப்', 'ವಾಟ್ಸಾಪ್', 'વોટ્સએપ', 'ਵਟਸਐਪ', 'ହ୍ଵାଟସ୍ ଆପ୍', 'වට්ස්ඇප්', 'วอตส์แอปป์', 'วอทส์แอพ', 'ဝက်စ်အက်ပ်', 'វ៉តសាប់', 'ວອດແອັບ', 'ワッツアップ', '왓츠앱', 'whatsapp的', 'whatsapp验证码', 'וואטסאפ', 'γουάτσαπ', 'ዋትስአፕ', 'ვოთსאფი', 'վոթսափ'], 'facebook': ['facebook', 'fb', 'meta', 'fbook', 'fb code', 'facebook code', 'فيسبوك', 'فيس بوك'], 'instagram': ['instagram', 'insta', 'ig', 'ig code', 'instagram code', 'انستغرام', 'انستقرام'], 'telegram': ['telegram', 'tg', 'tele', 'telegram code', 'tg code', 't.me', 'تيليجرام', 'تليجرام'], 'tiktok': ['tiktok', 'tik tok', 'tikvideo', 'tiktok code', 'tik code', 'تيك توك'], 'snapchat': ['snapchat', 'snap', 'snap code', 'سناب شات'], 'twitter': ['twitter', 'x.com', 'x code', 'twitter code', 'تويتر'], 'discord': ['discord', 'discord code', 'ديسكورد'], 'viber': ['viber', 'viber code', 'فايبر'], 'line': ['line', 'line code', 'line verification', 'لاين'], 'wechat': ['wechat', 'we chat', 'wechat code', 'وي تشات'], 'signal': ['signal', 'signal code', 'سيجنال'], 'linkedin': ['linkedin', 'linked in', 'لينكد إن'], 'imo': ['imo', 'imo code', 'imo verification', 'ايمو'], 'kakaotalk': ['kakao', 'kakaotalk', 'كاكاو'], 'qq': ['qq', 'tencent qq'], 'vk': ['vk', 'vkontakte'], 'google': ['google', 'gmail', 'youtube', 'g-', 'google voice', 'جوجل', 'غوغل'], 'microsoft': ['microsoft', 'ms', 'outlook', 'live.com', 'hotmail'], 'apple': ['apple', 'icloud', 'itunes', 'apple id'], 'yahoo': ['yahoo', 'yahoo code', 'ymail'], 'protonmail': ['proton', 'protonmail'], 'binance': ['binance', 'bnb', 'binances'], 'coinbase': ['coinbase'], 'okx': ['okx', 'okex'], 'kucoin': ['kucoin'], 'bybit': ['bybit'], 'huobi': ['huobi', 'htx'], 'mexc': ['mexc'], 'trustwallet': ['trust wallet', 'trustwallet'], 'paytm': ['paytm', 'paytm code', 'paytm otp'], 'phonepe': ['phonepe', 'phone pe', 'phonepe code'], 'gpay': ['gpay', 'google pay', 'googlepay'], 'upi': ['upi', 'upi code', 'upi otp'], 'paypal': ['paypal', 'pay pal'], 'cashapp': ['cash app', 'cashapp'], 'wise': ['wise', 'transferwise'], 'amazon': ['amazon', 'amzn', 'amazon code'], 'ebay': ['ebay'], 'aliexpress': ['aliexpress', 'ali express'], 'alibaba': ['alibaba'], 'daraz': ['daraz', 'daraz code'], 'foodpanda': ['foodpanda', 'food panda'], 'uber': ['uber', 'uber code', 'uber verification', 'uber eats'], 'pathao': ['pathao', 'pathao ride'], 'netflix': ['netflix', 'netflix code'], 'spotify': ['spotify', 'spotify code'], 'steam': ['steam', 'steam guard'], 'epicgames': ['epic games', 'epicgames'], 'roblox': ['roblox', 'roblox code'], 'riotgames': ['riot', 'riot games', 'valorant', 'league of legends'], 'garena': ['garena', 'free fire', 'freefire'], 'playstation': ['playstation', 'psn'], '1xbet': ['1xbet', '1x bet'], 'melbet': ['melbet', 'melbet code'], 'linebet': ['linebet'], 'bet365': ['bet365'], 'megapari': ['megapari'], 'tinder': ['tinder', 'tinder code'], 'bumble': ['bumble'], 'badoo': ['badoo'], 'gro5me': ['gro5me', 'gro 5 me', 'groSMS', 'gro sms', 'grow5me', 'gro5'], 'textlocal': ['textlocal', 'text local'], 'msg91': ['msg91', 'msg 91'], '2factor': ['2factor', '2 factor'], 'kaleyra': ['kaleyra'], 'valueFirst': ['valuefirst', 'value first'], 'smscountry': ['smscountry', 'sms country'], 'smsjust': ['smsjust', 'sms just'], 'exotel': ['exotel'], 'alertsms': ['alertsms', 'alert sms']}

def _kw_match(kw, text_lower):
    """Keyword ko text mein match karo.
    Short keywords (<=3 pure-alpha chars) ke liye word-boundary (\x08) use karo
    taaki 'wa' 'swap' mein ya 'wh' 'which' mein galat match na ho.
    Special chars wale keywords (w/a, t.me, wa.me, g-) ke liye simple 'in' check."""
    if len(kw) <= 3 and kw.isalpha():
        return bool(re.search('\\b' + re.escape(kw) + '\\b', text_lower))
    return kw in text_lower

def detect_service(text):
    """SMS/OTP message text se service detect karo.
    Word-boundary matching short keywords ke liye — false positives avoid hote hain."""
    text_lower = str(text).lower()
    for service_key, keywords in SERVICE_SMS_KEYWORDS.items():
        for kw in keywords:
            if _kw_match(kw, text_lower):
                return service_key.upper()
    return None
_KNOWN_SERVICE_KEYS = None

def _get_known_service_keys():
    global _KNOWN_SERVICE_KEYS
    if _KNOWN_SERVICE_KEYS is None:
        _KNOWN_SERVICE_KEYS = {k.upper() for k in SERVICE_SMS_KEYWORDS}
    return _KNOWN_SERVICE_KEYS

def get_service_info_html(service_text, msg_text=''):
    s = str(service_text).upper().strip()
    m = str(msg_text).lower().strip()
    apps = bot_settings.get('premium_apps', {})
    known_keys = _get_known_service_keys()
    detected_service = s
    if s not in known_keys and m:
        for service_key, keywords in SERVICE_SMS_KEYWORDS.items():
            for kw in keywords:
                if _kw_match(kw, m):
                    detected_service = service_key.upper()
                    break
            if detected_service != s:
                break
    clean_s = re.sub('[^\\w\\s]', '', detected_service).strip()
    for app_name, data in apps.items():
        if app_name == detected_service or app_name == clean_s or app_name in detected_service or (detected_service in app_name):
            full_name = data.get('name', app_name.title())
            char = data.get('char', '📱')
            eid = data.get('id')
            if eid:
                return (full_name, f'<tg-emoji emoji-id="{eid}">{char}</tg-emoji>')
            return (full_name, char)
    if len(detected_service) > 20:
        return ('Message', '💬')
    return (detected_service.title(), '📱')

def detect_language(text):
    if not text:
        return 'English'
    text_str = str(text)
    if any(('\u0600' <= c <= 'ۿ' for c in text_str)):
        return 'Arabic'
    if any(('ঀ' <= c <= '\u09ff' for c in text_str)):
        return 'Bengali'
    if any(('ऀ' <= c <= 'ॿ' for c in text_str)):
        return 'Hindi'
    if any(('\u0a00' <= c <= '\u0a7f' for c in text_str)):
        return 'Punjabi'
    if any(('\u0a80' <= c <= '૿' for c in text_str)):
        return 'Gujarati'
    if any(('\u0b00' <= c <= '\u0b7f' for c in text_str)):
        return 'Odia'
    if any(('\u0b80' <= c <= '\u0bff' for c in text_str)):
        return 'Tamil'
    if any(('ఀ' <= c <= '౿' for c in text_str)):
        return 'Telugu'
    if any(('ಀ' <= c <= '\u0cff' for c in text_str)):
        return 'Kannada'
    if any(('ഀ' <= c <= 'ൿ' for c in text_str)):
        return 'Malayalam'
    if any(('\u0d80' <= c <= '\u0dff' for c in text_str)):
        return 'Sinhala'
    if any(('\u0e00' <= c <= '\u0e7f' for c in text_str)):
        return 'Thai'
    if any(('\u0e80' <= c <= '\u0eff' for c in text_str)):
        return 'Lao'
    if any(('ༀ' <= c <= '\u0fff' for c in text_str)):
        return 'Tibetan'
    if any(('က' <= c <= '႟' for c in text_str)):
        return 'Burmese'
    if any(('ሀ' <= c <= '\u137f' for c in text_str)):
        return 'Amharic'
    if any(('ក' <= c <= '\u17ff' for c in text_str)):
        return 'Khmer'
    if any(('Ⴀ' <= c <= 'ჿ' for c in text_str)):
        return 'Georgian'
    if any(('\u0530' <= c <= '֏' for c in text_str)):
        return 'Armenian'
    if any(('\u0590' <= c <= '\u05ff' for c in text_str)):
        return 'Hebrew'
    if any(('Ͱ' <= c <= 'Ͽ' for c in text_str)):
        return 'Greek'
    if any(('Ѐ' <= c <= 'ӿ' for c in text_str)):
        return 'Russian'
    if any(('一' <= c <= '鿿' for c in text_str)):
        return 'Chinese'
    if any(('\u3040' <= c <= 'ゟ' or '゠' <= c <= 'ヿ' for c in text_str)):
        return 'Japanese'
    if any(('가' <= c <= '\ud7af' for c in text_str)):
        return 'Korean'
    text_lower = text_str.lower()
    if any((w in text_lower for w in ['kode verifikasi', 'jangan bagikan', 'rahasia'])):
        return 'Indonesian'
    if any((w in text_lower for w in ['kod pengesahan', 'jangan kongsi'])):
        return 'Malay'
    if any((w in text_lower for w in ['mã của bạn', 'không chia sẻ', 'mã xác minh'])):
        return 'Vietnamese'
    if any((w in text_lower for w in ['ang iyong code', 'huwag ibahagi'])):
        return 'Filipino'
    if any((w in text_lower for w in ['código', 'tu código', 'verificación', 'no compartas'])):
        return 'Spanish'
    if any((w in text_lower for w in ['seu código', 'código de verificação', 'não compartilhe'])):
        return 'Portuguese'
    if any((w in text_lower for w in ['code secret', 'ne partagez pas', 'votre code'])):
        return 'French'
    if any((w in text_lower for w in ['dein code', 'bestätigungscode', 'nicht teilen'])):
        return 'German'
    if any((w in text_lower for w in ['il tuo codice', 'codice di verifica', 'non condividere'])):
        return 'Italian'
    if any((w in text_lower for w in ['twój kod', 'nie udostępniaj', 'kod weryfikacyjny'])):
        return 'Polish'
    if any((w in text_lower for w in ['doğrulama kodu', 'paylaşmayın', 'onay kodu'])):
        return 'Turkish'
    if any((w in text_lower for w in ['jouw code', 'verificatiecode', 'niet delen'])):
        return 'Dutch'
    if any((w in text_lower for w in ['din kod', 'verifieringskod', 'dela inte'])):
        return 'Swedish'
    if any((w in text_lower for w in ['bekræftelseskode', 'del ikke'])):
        return 'Danish'
    if any((w in text_lower for w in ['bekreftelseskode', 'ikke del'])):
        return 'Norwegian'
    if any((w in text_lower for w in ['vahvistuskoodi', 'älä jaa'])):
        return 'Finnish'
    if any((w in text_lower for w in ['váš kód', 'ověřovací kód', 'nesdílejte'])):
        return 'Czech'
    if any((w in text_lower for w in ['overovací kód', 'nezdieľajte'])):
        return 'Slovak'
    if any((w in text_lower for w in ['ellenőrző kód', 'ne oszd meg'])):
        return 'Hungarian'
    if any((w in text_lower for w in ['codul tău', 'codul de verificare', 'nu partaja'])):
        return 'Romanian'
    if any((w in text_lower for w in ['kontrolni kod', 'kod za potvrdu', 'ne delite'])):
        return 'Croatian'
    if any((w in text_lower for w in ['код за потвърждение', 'не споделяйте'])):
        return 'Bulgarian'
    if any((w in text_lower for w in ['ваш код', 'код підтвердження'])):
        return 'Ukrainian'
    if any((w in text_lower for w in ['msimbo wako', 'usishiriki'])):
        return 'Swahili'
    if any((w in text_lower for w in ['verifikasiekode', 'moenie deel nie'])):
        return 'Afrikaans'
    return 'English'

def parse_chat_id(text):
    text = text.strip()
    if text.startswith('-100') or (text.startswith('-') and text[1:].isdigit()):
        return text
    if 't.me/' in text:
        parts = [p for p in text.split('/') if p]
        username = parts[-1] if parts else ''
        if username and (not username.startswith('+')):
            return '@' + username if not username.startswith('@') else username
    if text.startswith('@'):
        return text
    return '@' + text

def is_admin(user_id):
    return user_id in bot_settings['admins'] or user_id == OWNER_ID

def _get_fj_chat_id(entry):
    if isinstance(entry, dict):
        return entry.get('chat_id', '')
    return entry

def _get_fj_info(entry):
    if isinstance(entry, dict):
        return entry
    return {'chat_id': entry, 'type': 'channel', 'title': str(entry), 'invite_link': '', 'is_private': False}

def auto_detect_chat(chat_id_raw):
    res = api_call('getChat', {'chat_id': chat_id_raw})
    if not res.get('ok'):
        return None
    chat = res['result']
    chat_type = chat.get('type', '')
    title = chat.get('title', str(chat_id_raw))
    username = chat.get('username', '')
    is_private = not bool(username)
    if chat_type in ['supergroup', 'group']:
        detected_type = 'group'
    else:
        detected_type = 'channel'
    invite_link = ''
    if is_private:
        link_res = api_call('exportChatInviteLink', {'chat_id': chat_id_raw})
        if link_res.get('ok'):
            invite_link = link_res['result']
    else:
        invite_link = f'https://t.me/{username}'
    return {'chat_id': str(chat.get('id', chat_id_raw)), 'type': detected_type, 'title': title, 'invite_link': invite_link, 'is_private': is_private}

def check_force_join(user_id):
    if not bot_settings['fj_on'] or not bot_settings['fj_channels']:
        return True
    if is_admin(user_id):
        return True
    for entry in bot_settings['fj_channels']:
        ch = _get_fj_chat_id(entry)
        res = api_call('getChatMember', {'chat_id': ch, 'user_id': user_id})
        if res.get('ok') and res.get('result', {}).get('status', 'left') not in ['left', 'kicked']:
            continue
        else:
            return False
    return True

def send_force_join_msg(chat_id):
    _reset_btn_counter()
    kb = []
    for entry in bot_settings['fj_channels']:
        info = _get_fj_info(entry)
        ch_type = info.get('type', 'channel')
        title = info.get('title', '')
        invite_link = info.get('invite_link', '')
        ch_id = info.get('chat_id', '')
        if invite_link:
            url = invite_link
        elif str(ch_id).startswith('@'):
            url = f"https://t.me/{ch_id.replace('@', '')}"
        else:
            url = f'https://t.me/{ch_id}'
        type_label = 'Channel' if ch_type == 'channel' else 'Group'
        btn_text = f'Join {type_label}: {title}' if title else f'Join {type_label}'
        kb.append([{'text': btn_text, 'icon_custom_emoji_id': '5789428375261023681', 'url': url, 'style': _rs()}])
    kb.append([{'text': 'Check Joined', 'icon_custom_emoji_id': '5352694861990501856', 'callback_data': 'check_fj', 'style': _rs()}])
    send_message(chat_id, render_body_text(f"{PEM['warn']} <b>Please join our channels/groups to use the bot!</b>"), reply_markup={'inline_keyboard': kb})

def is_user_banned(user_id):
    if is_admin(user_id):
        return False
    with _banned_cache_lock:
        cached = user_banned_cache.get(user_id)
    if cached and time.time() - cached['time'] < 60:
        return cached['banned']
    local_u = _get_local_user(user_id)
    banned = local_u.get('banned', False)
    with _banned_cache_lock:
        if len(user_banned_cache) > 2000:
            oldest = sorted(user_banned_cache, key=lambda k: user_banned_cache[k]['time'])[:500]
            for k in oldest:
                user_banned_cache.pop(k, None)
        user_banned_cache[user_id] = {'banned': banned, 'time': time.time()}
    return banned

def extract_otp_code(text):
    clean_text = re.sub('[\\u200B-\\u200D\\uFEFF]', '', str(text))
    multi_part = re.search('(\\d{3}[-\\s]+\\d{3})|(\\d{2}[-\\s]+\\d{2}[-\\s]+\\d{2})', clean_text)
    if multi_part:
        return multi_part.group(0).replace(' ', '')
    otp_keywords = ['code', 'is', 'otp', 'pin', 'verification', 'auth', 'رمز', 'your code']
    keywords_pattern = '|'.join(otp_keywords)
    keyword_match = re.search(f'(?:{keywords_pattern})\\s*(?:is|:|-|=)?\\s*([a-z0-9]{{4,10}})', clean_text, re.I)
    if keyword_match and keyword_match.group(1).isdigit():
        return keyword_match.group(1)
    keyword_match_rev = re.search(f'([a-z0-9]{{4,10}})\\s*(?:is your|is the|code)', clean_text, re.I)
    if keyword_match_rev and keyword_match_rev.group(1).isdigit():
        return keyword_match_rev.group(1)
    g_match = re.search('G-(\\d{6})', clean_text, re.IGNORECASE)
    if g_match:
        return g_match.group(1)
    digit_matches = re.findall('(?<!\\d)\\d{4,8}(?!\\d)', clean_text)
    if digit_matches:
        six_digit = [d for d in digit_matches if len(d) == 6]
        if six_digit:
            return six_digit[0]
        non_year = [d for d in digit_matches if not (len(d) == 4 and 1990 <= int(d) <= 2099)]
        return non_year[0] if non_year else digit_matches[0]
    return None

def parse_panel_response(response_text, p_config=None, max_results=None):
    results = []
    p_type = p_config.get('type', 'API Panel') if p_config else 'API Panel'
    n_col_name = p_config.get('num_col_name', 'number').lower() if p_config else 'number'
    m_col_name = p_config.get('msg_col_name', 'message').lower() if p_config else 'message'

    def _safe_col_idx(val, default):
        try:
            return max(0, int(val) - 1)
        except (TypeError, ValueError):
            return default
    n_idx = _safe_col_idx(p_config.get('num_col_idx'), 1) if p_config else 1
    m_idx = _safe_col_idx(p_config.get('msg_col_idx'), 2) if p_config else 2
    if p_type == 'Auto Captcha Panel':
        try:
            soup = BeautifulSoup(response_text, 'html.parser')
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                if not rows:
                    continue
                final_n_idx, final_m_idx = _find_header_column_indices(rows, n_col_name, m_col_name, n_idx, m_idx)
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    if all((c.name == 'th' for c in cols)):
                        continue
                    if len(cols) > max(final_n_idx, final_m_idx):
                        num_text = cols[final_n_idx].get_text(separator=' ', strip=True)
                        msg_text = cols[final_m_idx].get_text(separator=' ', strip=True)
                        clean_num = re.sub('\\D', '', num_text)
                        if clean_num and 5 <= len(clean_num) <= 18:
                            otp = extract_otp_code(msg_text)
                            if otp and len(msg_text) > 4:
                                results.append({'number': clean_num, 'message': msg_text, 'otp': otp, 'item_id': ''})
        except Exception as e:
            logger.warning(f'parse_panel HTML table error: {e}')
    else:
        try:
            data = json.loads(response_text)
            temp_results = []

            def process_item(item):
                pot_nums_list = []
                pot_msg = None
                explicit_otp = ''
                item_id = ''
                values = []
                if isinstance(item, dict):
                    lower_keys = {str(k).lower(): v for k, v in item.items()}
                    for k in ['number', 'num', 'phone', 'msisdn', 'sender']:
                        if k in lower_keys:
                            clean_val = re.sub('\\D', '', str(lower_keys[k]))
                            if 5 <= len(clean_val) <= 18:
                                if clean_val not in pot_nums_list:
                                    pot_nums_list.append(clean_val)
                    for k in ['message', 'msg', 'sms', 'content', 'text', 'message_text', 'sms_text', 'full_message']:
                        if k in lower_keys:
                            val = str(lower_keys[k])
                            if len(val) > 4:
                                pot_msg = val
                                break
                    for k in ['otp_code', 'otp', 'code', 'pin']:
                        if k in lower_keys and str(lower_keys[k] or '').strip().isdigit():
                            explicit_otp = str(lower_keys[k]).strip()
                            break
                    item_id = ''
                    for k in ['id', 'sms_id', 'msg_id', 'message_id', 'record_id', 'row_id', 'cdr_id']:
                        if k in lower_keys and lower_keys[k] is not None:
                            item_id = str(lower_keys[k]).strip()
                            break
                    values = list(item.values())
                elif isinstance(item, list):
                    if len(item) > max(n_idx, m_idx):
                        raw_n = item[n_idx]
                        raw_m = item[m_idx]
                        cn = re.sub('\\D', '', str(raw_n))
                        if 5 <= len(cn) <= 18:
                            pot_nums_list.append(cn)
                        m_clean = re.sub('(?<!\\n)nn(?!\\n)', '\n', str(raw_m))
                        if len(m_clean) > 2:
                            pot_msg = m_clean
                        for col in item:
                            col_str = str(col).strip()
                            if re.match('^\\d{4}[-/]\\d{2}[-/]\\d{2}(\\s+\\d{2}:\\d{2}(:\\d{2})?)?$', col_str):
                                item_id = col_str
                                break
                    values = item
                for v in values:
                    if isinstance(v, (dict, list)) or v is None:
                        continue
                    v_str = str(v).strip()
                    clean_v = re.sub('\\D', '', v_str)
                    if 7 <= len(clean_v) <= 18 and (not re.search('[a-zA-Z]', v_str)):
                        is_date = re.search('\\d{4}[-/]\\d{2}[-/]\\d{2}', v_str) or re.search('\\d{2}:\\d{2}:\\d{2}', v_str) or re.match('^\\d{8}$', clean_v) or ('.' in v_str)
                        if not is_date and (not re.search('\\d{4}[-/]\\d{1,2}[-/]\\d{1,2}\\s+\\d{1,2}:\\d{2}', v_str)):
                            if clean_v not in pot_nums_list:
                                pot_nums_list.append(clean_v)
                    if len(v_str) > 4 and (not v_str.isdigit()):
                        _is_datetime_str = bool(re.match('^\\d{4}[-/]\\d{2}[-/]\\d{2}(\\s+\\d{2}:\\d{2}(:\\d{2})?)?$', v_str) or re.match('^\\d{2}:\\d{2}:\\d{2}$', v_str))
                        if _is_datetime_str:
                            if not item_id:
                                item_id = v_str
                            continue
                        v_str_clean = re.sub('(?<!\\n)nn(?!\\n)', '\n', v_str)
                        has_otp = bool(extract_otp_code(v_str_clean))
                        if has_otp:
                            if pot_msg is None or len(v_str_clean) > len(pot_msg):
                                pot_msg = v_str_clean
                        elif pot_msg is None and len(v_str_clean) > 10:
                            pot_msg = v_str_clean
                pot_num = None
                if pot_nums_list:
                    matched_user_num = None
                    for n in pot_nums_list:
                        if n in nexa_assigned_numbers or any((n in str(key) for key in nexa_assigned_numbers.keys())):
                            matched_user_num = n
                            break
                    if matched_user_num:
                        pot_num = matched_user_num
                    else:
                        valid_nums = [n for n in pot_nums_list if not (len(n) == 8 and re.match('^\\d{8}$', n))]
                        if valid_nums:
                            pot_num = max(valid_nums, key=len)
                        elif pot_nums_list:
                            pot_num = pot_nums_list[0]
                if pot_num and (pot_msg or explicit_otp):
                    otp = explicit_otp if explicit_otp else extract_otp_code(pot_msg)
                    if otp:
                        temp_results.append({'number': pot_num, 'message': pot_msg or '', 'otp': otp, 'item_id': item_id})

            def traverse_json(node, depth=0):
                if depth > 10:
                    return
                if max_results and len(temp_results) >= max_results:
                    return
                if isinstance(node, list):
                    if len(node) > 0 and (not isinstance(node[0], (dict, list))):
                        process_item(node)
                    else:
                        for child in node:
                            if max_results and len(temp_results) >= max_results:
                                break
                            if isinstance(child, (dict, list)):
                                traverse_json(child, depth + 1)
                elif isinstance(node, dict):
                    prev_len = len(temp_results)
                    process_item(node)
                    if len(temp_results) == prev_len:
                        for val in node.values():
                            if max_results and len(temp_results) >= max_results:
                                break
                            if isinstance(val, (dict, list)):
                                traverse_json(val, depth + 1)
            traverse_json(data)
            seen = set()
            for r in temp_results:
                uid = f"{r['number']}_{r['otp']}_{r.get('item_id', '')}"
                if uid not in seen:
                    seen.add(uid)
                    results.append(r)
        except Exception as e:
            logger.warning(f'parse_panel_response error: {e}')
    return results

def _attempt_spa_json_login(login_url, initial_res, username, password, session, idx):
    """Returns (True, None) on success, (False, reason) on failure."""
    parsed = urlparse(login_url)
    same_origin = f'{parsed.scheme}://{parsed.netloc}'
    api_bases = []
    csp = initial_res.headers.get('Content-Security-Policy', '') or initial_res.headers.get('content-security-policy', '')
    if csp:
        m = re.search('connect-src([^;]+)', csp, re.I)
        if m:
            for tok in m.group(1).split():
                if tok.startswith('http'):
                    api_bases.append(tok.strip().rstrip('/'))
    if same_origin not in api_bases:
        api_bases.append(same_origin)
    login_paths = ['/api/user/login', '/api/auth/login', '/user/login', '/auth/login', '/api/login', '/login']
    payload_variants = [{'identifier': username, 'password': password}, {'username': username, 'password': password}, {'email': username, 'password': password}]
    last_reason = 'No login form found'
    for base in api_bases:
        for path in login_paths:
            url = base.rstrip('/') + path
            for payload in payload_variants:
                try:
                    res = session.post(url, json=payload, timeout=12)
                except Exception:
                    continue
                if res.status_code not in (200, 201):
                    continue
                try:
                    body = res.json()
                except Exception:
                    continue
                token = None
                for path_getter in (lambda b: b.get('data', {}).get('doc', {}).get('token'), lambda b: b.get('data', {}).get('token'), lambda b: b.get('doc', {}).get('token'), lambda b: b.get('token')):
                    try:
                        token = path_getter(body)
                    except Exception:
                        token = None
                    if token:
                        break
                success_flag = body.get('success') is True or str(body.get('status', '')).lower() == 'success'
                if token or success_flag:
                    if token:
                        session.headers.update({'Authorization': f'Bearer {token}'})
                    panel_sessions[idx] = session
                    return (True, {'token': token, 'api_base': base})
                msg = body.get('data', {}).get('message') if isinstance(body.get('data'), dict) else body.get('message')
                if msg:
                    last_reason = str(msg)[:60]
    return (False, last_reason)

def attempt_auto_login(p, idx):
    """Login to HTML Auto Captcha panels while preserving the returned session/cookies.
    Success is detected from the real post-login response, not only from a hard-coded
    /client redirect, so panels with slightly different dashboard/CDR routes work too.
    """
    login_url = p.get('login_url', '').strip()
    if not login_url.startswith('http'):
        login_url = 'http://' + login_url
    login_keywords = ['/login', '/signin', '/auth', '/sign-in', '/log-in', '.php', '.asp', '.html', '.htm', '.jsp']
    url_lower = login_url.lower()
    has_login_path = any(kw in url_lower for kw in login_keywords)
    if not has_login_path:
        login_url = f"{login_url.rstrip('/')}/login"

    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=2)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    })

    def _looks_like_login_page(response):
        """Return True only when the response still clearly looks like the login page."""
        try:
            page_url = (response.url or '').lower()
            soup_ = BeautifulSoup(response.text or '', 'html.parser')
            has_password = bool(soup_.find('input', {'type': 'password'}))
            forms_ = soup_.find_all('form')
            login_form = False
            for f in forms_:
                txt = f.get_text(' ', strip=True).lower()
                action_ = (f.get('action') or '').lower()
                if has_password and ('login' in txt or 'login' in action_ or 'signin' in action_ or 'auth' in action_):
                    login_form = True
                    break
            return ('/login' in page_url or '/signin' in page_url or '/auth' in page_url) and (has_password or login_form)
        except Exception:
            return False

    def _mark_success():
        panel_sessions[idx] = session
        p['login_status'] = '✅ Active & Fetching'
        p['retry_wait'] = 90
        return True

    try:
        res = session.get(login_url, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        all_text = res.text

        captcha_match = re.search(r'(\d+\s*[\+\-\*]\s*\d+)\s*[=\?:]', all_text)
        if not captcha_match:
            captcha_match = re.search(r'what is\s*(\d+\s*[\+\-\*]\s*\d+)', all_text, re.I)
        if not captcha_match:
            for el in soup.find_all(['label', 'div', 'span', 'p', 'strong']):
                txt = el.get_text(separator=' ', strip=True)
                if any(op in txt for op in ['+', '-', '*']):
                    m = re.search(r'(\d+\s*[\+\-\*]\s*\d+)', txt)
                    if m:
                        captcha_match = m
                        break

        captcha_found = captcha_match is not None
        captcha_text = captcha_match.group(1) if captcha_match else ''
        answer = ''
        if captcha_found:
            m2 = re.search(r'(\d+)\s*([\+\-\*])\s*(\d+)', captcha_text)
            if m2:
                a, op, b = int(m2.group(1)), m2.group(2), int(m2.group(3))
                if op == '+':
                    answer = str(a + b)
                elif op == '-':
                    answer = str(a - b)
                elif op == '*':
                    answer = str(a * b)

        form = soup.find('form')
        if not form:
            ok, info = _attempt_spa_json_login(login_url, res, p.get('username', ''), p.get('password', ''), session, idx)
            if ok:
                p['login_status'] = '✅ Active & Fetching'
                p['retry_wait'] = 90
                if isinstance(info, dict):
                    if info.get('token'):
                        p['auth_token'] = info['token']
                    if info.get('api_base'):
                        p['api_base'] = info['api_base']
                return True
            reason = info if isinstance(info, str) else 'No login form found'
            p['login_status'] = f'❌ Login Failed ({reason[:40]})'
            p['retry_wait'] = 90
            return False

        action = form.get('action')
        post_url = urljoin(login_url, action) if action else login_url
        form_data = {}
        for hidden in form.find_all('input', type='hidden'):
            name = hidden.get('name')
            if name:
                form_data[name] = hidden.get('value') or ''

        def _attr_matches(value, pattern):
            if isinstance(value, (list, tuple)):
                value = ' '.join(str(v) for v in value)
            return bool(value and re.search(pattern, str(value), re.I))

        user_input = form.find('input', {'name': lambda value: _attr_matches(value, r'user|email|id')}) \
            or form.find('input', {'type': 'text', 'placeholder': lambda value: _attr_matches(value, r'user|email')}) \
            or form.find('input', {'type': 'text'})
        pass_input = form.find('input', {'name': lambda value: _attr_matches(value, r'pass')}) \
            or form.find('input', {'type': 'password'})
        captcha_input = form.find('input', {'placeholder': lambda value: _attr_matches(value, r'answer|ans|code|verification|value|captcha')}) \
            or form.find('input', {'name': lambda value: _attr_matches(value, r'ans|captcha|ver|code|answer')})

        user_field = user_input.get('name') if user_input else 'username'
        pass_field = pass_input.get('name') if pass_input else 'password'
        captcha_field = captcha_input.get('name') if captcha_input else 'answer'
        form_data[user_field] = p.get('username', '')
        form_data[pass_field] = p.get('password', '')
        if captcha_found and captcha_field and answer:
            form_data[captcha_field] = answer

        method = (form.get('method') or 'post').strip().lower()
        request_headers = {'Referer': login_url, 'Origin': f'{urlparse(login_url).scheme}://{urlparse(login_url).netloc}'}
        if method == 'get':
            login_req = session.get(post_url, params=form_data, allow_redirects=False, timeout=15, headers=request_headers)
        else:
            login_req = session.post(post_url, data=form_data, allow_redirects=False, timeout=15, headers=request_headers)

        location = (login_req.headers.get('Location') or '').strip()
        candidate_responses = []
        if location:
            redirect_url = urljoin(post_url, location)
            try:
                candidate_responses.append(session.get(redirect_url, allow_redirects=True, timeout=12))
            except Exception:
                pass
        else:
            candidate_responses.append(login_req)

        # A successful login can redirect to /client/... or any other authenticated dashboard route.
        for candidate in candidate_responses:
            final_url = (candidate.url or '').lower()
            if candidate.status_code == 200 and not _looks_like_login_page(candidate):
                if '/client/' in final_url or '/dashboard' in final_url or 'smscdr' in final_url or 'sms cdr' in (candidate.text or '').lower():
                    return _mark_success()

        err_response = candidate_responses[-1] if candidate_responses else login_req
        err_text = err_response.text or ''
        err_soup = BeautifulSoup(err_text, 'html.parser')
        error_el = err_soup.find('font') or err_soup.find('div', class_='error') or err_soup.find('span', class_='error')
        error_msg = error_el.get_text(' ', strip=True) if error_el else ''
        error_lower = error_msg.lower()

        if 'session invalid' in error_lower or 'try after' in error_lower:
            wait_seconds = 120
            m_wait = re.search(r'try after\s*(\d+)\s*(minute|min|second|sec)', error_msg, re.I)
            if m_wait:
                n = int(m_wait.group(1))
                unit = m_wait.group(2).lower()
                wait_seconds = n * 60 if 'min' in unit else n
                wait_seconds += 15
            p['login_status'] = f'❌ Panel Locked ({error_msg[:80]})'
            p['retry_wait'] = wait_seconds
            p['last_login_attempt'] = time.time()
            return False
        if 'captcha' in error_lower:
            p['login_status'] = '❌ Captcha Failed (Retrying...)'
            p['retry_wait'] = 90
            return False
        if 'invalid' in error_lower or 'password' in error_lower or 'username' in error_lower:
            p['login_status'] = '❌ Wrong Username/Password'
            p['retry_wait'] = 90
            return False

        # Final session verification. Try the configured message URL first, then both
        # common MSI CDR routes. This fixes panels where the real page is /client/SMSCDR
        # instead of /client/SMSCDRStats.
        msg_link = p.get('msg_link', '').strip()
        if msg_link and not msg_link.startswith('http'):
            msg_link = 'http://' + msg_link
        parsed_login = urlparse(login_url)
        base = f'{parsed_login.scheme}://{parsed_login.netloc}{parsed_login.path.rsplit("/", 1)[0]}'
        check_urls = []
        if msg_link:
            check_urls.append(msg_link)
        check_urls.extend([
            f'{base}/client/SMSCDR',
            f'{base}/client/SMSCDRStats',
        ])

        seen_urls = set()
        for check_url in check_urls:
            if not check_url or check_url in seen_urls:
                continue
            seen_urls.add(check_url)
            try:
                check_res = session.get(check_url, allow_redirects=True, timeout=12)
                if check_res.status_code == 200 and not _looks_like_login_page(check_res):
                    body_lower = (check_res.text or '').lower()
                    final_url = (check_res.url or '').lower()
                    if '/client/' in final_url or 'sms cdr' in body_lower or 'smscdr' in final_url:
                        return _mark_success()
            except Exception:
                continue

        # Do not report a correct math answer as the cause of failure.
        reason = error_msg[:60] if error_msg else 'Authenticated session not detected after login'
        p['login_status'] = f'❌ Login Failed ({reason})'
        p['retry_wait'] = 90
        return False
    except Exception as e:
        p['login_status'] = f'❌ Error: {str(e)[:60]}'
        p['retry_wait'] = 90
        return False

def _build_api_urls(p):
    """Build the list of URLs + headers to try for an API Panel from its config.
    Extracted to avoid duplicate code between panel_monitor_thread and test_p_conn_."""
    full_url = p.get('full_api_url', '').strip()
    url = p.get('api_url', '').strip()
    token = p.get('token', '').strip()
    token_header = p.get('token_header', '').strip()
    urls_to_try = []
    if full_url:
        urls_to_try.append(full_url)
    elif token_header and token:
        urls_to_try.append(url)
    elif '{token}' in url or '{key}' in url:
        urls_to_try.append(url.replace('{token}', token).replace('{key}', token))
    elif 'token=' in url or 'key=' in url:
        urls_to_try.append(url)
    else:
        urls_to_try.append(url)
        if token:
            sep = '&' if '?' in url else '?'
            urls_to_try.append(f'{url}{sep}token={token}')
            urls_to_try.append(f'{url}{sep}key={token}&start=0')
            urls_to_try.append(f'{url}{sep}key={token}')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    if token_header and token:
        headers[token_header] = token
    return (urls_to_try, headers)

def _find_otp_owners(clean_num):
    """Find all bot users who own this phone number.
    Extracted to avoid duplicate code between panel_monitor_thread and global_sms_listener.
    Returns: list of chat_ids (may be multiple if num_share > 1)."""
    owners = []
    for uid, session_data in list(user_active_sessions.items()):
        for act_num in session_data.get('nums', []):
            act_clean = str(act_num).replace('+', '').replace(' ', '').replace('-', '').strip()
            if act_clean == clean_num or (len(act_clean) >= 8 and len(clean_num) >= 8 and (abs(len(act_clean) - len(clean_num)) <= 3) and (act_clean.endswith(clean_num[-8:]) or clean_num.endswith(act_clean[-8:]))):
                owners.append(uid)
                break
    if not owners:
        for b_id, b_data in number_batches.items():
            for n_obj in b_data.get('numbers', []):
                stored_clean = str(n_obj.get('num', '')).replace('+', '').replace(' ', '').replace('-', '').strip()
                if stored_clean == clean_num or (len(stored_clean) >= 8 and len(clean_num) >= 8 and (abs(len(stored_clean) - len(clean_num)) <= 3) and (stored_clean.endswith(clean_num[-8:]) or clean_num.endswith(stored_clean[-8:]))):
                    for used_uid in n_obj.get('used_by', []):
                        if not user_otp_delivery_active.get(used_uid, True):
                            continue
                        if used_uid not in owners:
                            owners.append(used_uid)
                    if owners:
                        break
            if owners:
                break
    if not owners:
        for nexa_n, n_owner in nexa_assigned_numbers.items():
            clean_nexa = str(nexa_n).replace('+', '').replace(' ', '').replace('-', '').strip()
            if clean_nexa == clean_num or (len(clean_nexa) >= 8 and len(clean_num) >= 8 and (abs(len(clean_nexa) - len(clean_num)) <= 3) and (clean_nexa.endswith(clean_num[-8:]) or clean_num.endswith(clean_nexa[-8:]))):
                owners.append(n_owner)
    if not owners:
        vx_owner = _find_assigned_owner(voltx_assigned_numbers, clean_num)
        if vx_owner:
            owners.append(vx_owner)
    if not owners:
        sx_owner = _find_assigned_owner(stex_assigned_numbers, clean_num)
        
        if sx_owner:
            owners.append(sx_owner)
    if not owners:
        with _data_lock:
            for aid, aowner in smsbower_assigned_numbers.items():
                if aowner == clean_num or str(aid) == clean_num:
                    owners.append(aowner)
    return list(set(owners))
_RATE_LIMIT_PHRASES = ['too many times', 'too many requests', 'rate limit', 'try again in', 'slow down', '429', 'access denied', "you've accessed"]

def _is_rate_limited_response(text):
    """Check karo agar API rate-limit HTML/text page return kar raha hai."""
    if not text:
        return False
    lower = text.lower()
    return any((phrase in lower for phrase in _RATE_LIMIT_PHRASES))
_owner_alert_last_sent = {}

def _notify_owner_panel_issue(alert_key, message, cooldown=3600):
    """Owner ko panel ki about a specific problem once (cooldown ke andar dobara nahi) batao.
    Isse silent failures (jaise 'the panel is returning data but OTPs cannot be parsed/delivered')
    ab OWNER ko turant dikhengi, warna pehle yeh sirf log file mein chhup jaati thi."""
    now = time.time()
    last = _owner_alert_last_sent.get(alert_key, 0)
    if now - last < cooldown:
        return
    _owner_alert_last_sent[alert_key] = now
    try:
        send_message(OWNER_ID, render_body_text(f'⚠️ <b>Panel Alert</b>\n{message}'))
    except Exception as e:
        logger.warning(f'Owner panel-alert send failed: {e}')

def _fetch_api_panel_data(idx, p):
    """Ek API panel se data fetch karo. Returns parsed list ya [] on failure."""
    now = time.time()
    rate_limit_until = p.get('rate_limit_until', 0)
    if now < rate_limit_until:
        wait_left = int(rate_limit_until - now)
        logger.info(f'Panel {idx} rate-limited — skipping for {wait_left}s more')
        return []
    urls_to_try, headers = _build_api_urls(p)
    for try_url in urls_to_try:
        try:
            res = tg_session.get(try_url, headers=headers, timeout=8)
            if res.status_code == 429 or _is_rate_limited_response(res.text):
                backoff = 10
                p['rate_limit_until'] = now + backoff
                logger.warning(f'Panel {idx} rate-limited by API — backing off {backoff}s. Response: {res.text[:120]!r}')
                return []
            parsed_data = parse_panel_response(res.text, p)
            if parsed_data:
                full_url = p.get('full_api_url', '')
                token = p.get('token', '').strip()
                url = p.get('api_url', '').strip()
                if not full_url and try_url != url and token and (not p.get('token_header', '')):
                    p['api_url'] = try_url.replace(token, '{token}')
                    save_local_db()
                p.pop('rate_limit_until', None)
                p['_zero_yield_streak'] = 0
                return parsed_data
            else:
                _has_body = bool(res.text and res.text.strip() and (res.text.strip() not in ('[]', '{}', 'null')))
                if _has_body:
                    p['_zero_yield_streak'] = p.get('_zero_yield_streak', 0) + 1
                    if p['_zero_yield_streak'] >= 5:
                        # Silent panel parse warning: keep monitoring, do not send automatic alert messages.
                        logger.warning(f"Panel {idx} returned data but no OTP/number could be parsed for 5+ checks.")
        except Exception as e:
            logger.warning(f'Panel URL probe error: {e}')
            continue
    return []

def _fetch_json_api_panel_data(p, sess):
    """SPA/JSON-API panels (jaise Teleroutex) ke liye data fetch — HTML table
    scrape karne ki jagah seedha panel ki live JSON API se records lete hain."""
    api_base = p.get('api_base', '').rstrip('/')
    if not api_base:
        return ([], '')
    data_path = p.get('api_data_path', '/api/message-data-record')
    if 'sample' in data_path.lower():
        data_path = '/api/message-data-record'
    if not data_path.startswith('/'):
        data_path = '/' + data_path
    panel_username = p.get('username', '').strip().lower()
    url = f'{api_base}{data_path}?pageSize=50&page=1&sortBy=createdAt_descending'
    res = sess.get(url, timeout=15)
    if res.status_code == 401:
        raise Exception('Session expired')
    try:
        body = res.json()
    except Exception:
        return ([], res.text)
    docs = (body.get('data') or {}).get('docs', [])
    if not isinstance(docs, list):
        return ([], res.text)
    results = []
    # Incremental panel cursor: the panel API returns a rolling history, but the
    # bot must only hand NEW records to the OTP processor.  Keep the record IDs
    # per panel so an old history page can never be re-delivered after a poll,
    # restart, or a changed internal OTP id.
    seen_records = p.setdefault('_seen_panel_records', {})
    seen_cutoff = time.time() - 26 * 60 * 60
    if seen_records:
        for _k, _ts in list(seen_records.items()):
            try:
                if float(_ts) < seen_cutoff:
                    del seen_records[_k]
            except Exception:
                del seen_records[_k]
    changed_seen = False
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        cause = str(doc.get('cause', 'Success')).strip()
        if cause.lower() not in ('success', ''):
            continue
        if panel_username:
            client_info = doc.get('client') or {}
            if isinstance(client_info, dict):
                rec_user = str(client_info.get('username', '')).strip().lower()
                if rec_user and rec_user != panel_username:
                    continue
        num_val = doc.get('number', '')
        msg_val = doc.get('message', '')
        clean_num = re.sub('\\D', '', str(num_val))
        if not (clean_num and 5 <= len(clean_num) <= 18 and (not re.match('^\\d{8}$', clean_num))):
            continue
        msg_clean = re.sub('(?<!\\n)nn(?!\\n)', '\n', str(msg_val))
        otp = extract_otp_code(msg_clean)
        if otp and len(msg_clean) > 4:
            item_id = str(doc.get('createdAt') or doc.get('_id') or doc.get('id') or '').strip()
            # Prefer the panel's immutable record id/timestamp.  If the API has
            # no id, use a stable fingerprint of the actual SMS record.
            if item_id:
                record_key = item_id
            else:
                record_key = 'NOID_' + re.sub(r'\s+', ' ', f'{clean_num}|{otp}|{msg_clean}'.strip().lower())[:700]
            if record_key in seen_records:
                # This is history already seen by this panel. Do not return it
                # to _process_panel_otps at all.
                continue
            seen_records[record_key] = time.time()
            changed_seen = True
            results.append({'number': clean_num, 'message': msg_clean, 'otp': otp, 'item_id': item_id})
    if changed_seen:
        # Persist the cursor so restarting the bot does not make the panel's old
        # history look new again.
        save_local_db()
    return (results, res.text)

def _fetch_captcha_panel_data(idx, p):
    """Ek Auto Captcha panel se data fetch karo. Returns list, ya None agar skip karna ho."""
    now = time.time()
    if now - p.get('last_fetch_time', 0) < 10:
        return None
    sess = panel_sessions.get(idx)
    if not sess:
        retry_wait = p.get('retry_wait', 90)
        if retry_wait > 1800:
            retry_wait = 1800
            p['retry_wait'] = 1800
        if now - p.get('last_login_attempt', 0) < retry_wait:
            return None
        p['last_login_attempt'] = now
        success = attempt_auto_login(p, idx)
        save_local_db()
        if not success:
            p['last_fetch_time'] = now
            p['_login_fail_streak'] = p.get('_login_fail_streak', 0) + 1
            if p['_login_fail_streak'] >= 3:
                _notify_owner_panel_issue(f'cpt_login_fail_{idx}', f"<b>{p.get('name', 'Auto Captcha Panel')}</b> is repeatedly failing to log in.\nStatus: {p.get('login_status', 'Unknown')}\nThat is why OTPs are not being sent to the OTP group from this panel — Please check the Username, Password, and Login URL.")
            return None
        p['_login_fail_streak'] = 0
        sess = panel_sessions.get(idx)
    try:
        if p.get('api_base'):
            parsed_data, res_text = _fetch_json_api_panel_data(p, sess)
        else:
            msg_link = p.get('msg_link', '').strip()
            if not msg_link.startswith('http') and msg_link != '':
                msg_link = 'http://' + msg_link
            if not msg_link:
                login_url = p.get('login_url', '').strip()
                if not login_url.startswith('http'):
                    login_url = 'http://' + login_url
                base = login_url
                for _seg in ['/login', '/signin', '/auth', '/sign-in', '/log-in']:
                    if _seg in base.lower():
                        base = base[:base.lower().index(_seg)]
                        break
                msg_link = f'{base}/client/SMSCDRStats'
            parsed_data, res_text = fetch_cpt_panel_cdrs(p, sess, msg_link)
        p['login_status'] = '✅ Active & Fetching'
        p['last_fetch_time'] = time.time()
        if parsed_data:
            p['_zero_yield_streak'] = 0
        elif res_text and res_text.strip():
            if p.get('api_base'):
                p['_zero_yield_streak'] = 0
            else:
                p['_zero_yield_streak'] = p.get('_zero_yield_streak', 0) + 1
                if p['_zero_yield_streak'] >= 5:
                    # Silent panel parse warning: keep monitoring, do not send automatic alert messages.
                    logger.warning(f"Panel {idx} page loaded but no OTP/number could be parsed for 5+ checks.")
        return parsed_data
    except Exception as e:
        p['login_status'] = '❌ Session Expired (Retrying...)'
        if idx in panel_sessions:
            del panel_sessions[idx]
        p['last_fetch_time'] = time.time()
        save_local_db()
        return None

def _process_panel_otps(idx, p, parsed_data):
    """Panel se mila parsed_data process karo aur OTPs deliver karo."""
    panel_needs_warmup = p.get('needs_warmup', True)
    limit = p.get('records', 0)
    if p.get('type') != 'Auto Captcha Panel' and limit > 0:
        parsed_data = parsed_data[:limit]
    for item in parsed_data:
        try:
            num = item['number']
            otp = item['otp']
            msg_text = item['message']
            item_id = item.get('item_id', '')
            panel_key = p.get('name', str(idx))
            if item_id:
                if _is_stale_otp(item_id):
                    _add_to_processed(f'PANEL_{panel_key}_{item_id}')
                    continue
                unique_id = f'PANEL_{panel_key}_{item_id}'
                dedup_window = 90000
            else:
                unique_id = f'{num}_{otp}'
                dedup_window = 10
            clean_api_num = str(num).replace('+', '').replace(' ', '').replace('-', '').strip()
            # First-level cross-provider dedup prevents the same historical panel SMS
            # from being forwarded again under a new panel-specific item ID.
            detected_app = detect_service(msg_text)
            if not _claim_global_otp(clean_api_num, otp, msg_text, detected_app or p.get('name', 'Panel')):
                logger.info(f'Skipping duplicate OTP across sources: {clean_api_num} / {otp}')
                continue
            owners = _find_otp_owners(clean_api_num)
            warmup_num_otp_key = f'WARMUP_{num}_{otp}'
            if panel_needs_warmup:
                if item_id:
                    _add_to_processed(unique_id)
                _add_to_processed(warmup_num_otp_key)
                continue
            if not item_id and _is_processed(warmup_num_otp_key, window=90000):
                continue
            if _is_processed(unique_id, window=dedup_window):
                continue
            _add_to_processed(unique_id)
            if not item_id:
                _add_to_processed(warmup_num_otp_key)
            char, iso = get_flag_and_code(num)
            app_name_for_display = detect_service(msg_text) or p.get('name', 'Panel')
            app_full_name, prem_app_html = get_service_info_html(app_name_for_display, msg_text)
            current_time = time.time()
            display_num = f'+{num}' if not str(num).startswith('+') else str(num)
            lang = detect_language(msg_text)
            _prune_traffic(current_time)
            with _traffic_lock:
                recent_traffic.append({'service': app_full_name, 'iso': iso, 'flag': char, 'number': num, 'time': current_time})
            save_local_db()
            first_owner = owners[0] if owners else None
            masked = mask_number(display_num, user_id=first_owner)
            _g_clean = str(display_num).replace('+', '').replace(' ', '')
            _g_masked = f'{_g_clean[:4]}{_MASK_EMOJI}{_g_clean[-4:]}{_END_NUMBER_EMOJI}' if len(_g_clean) >= 8 else mask_number(display_num)
            iso_text = f' #{iso}' if iso else ''
            lang_text = str(lang or '').strip()
            lang_line = f'\n💬 {html.escape(lang_text)}' if lang_text and lang_text.lower() not in ('unknown','none','n/a') else ''
            group_msg = _otp_box_message(f'{get_flag_info_html(display_num)}{iso_text} {prem_app_html} {_g_masked}', lang_line)
            fw_groups = bot_settings.get('fw_groups', [])
            if not fw_groups:
                _notify_owner_panel_issue('no_fw_groups', 'OTP is being received and parsed, but no <b>OTP Group</b> is configured so it is not being forwarded anywhere.\nAdd a group in Admin Panel → OTP Groups.')
            _sent_group_ids = set()
            for fw in fw_groups:
                try:
                    _fw_chat_key = str(fw.get('chat_id', '')).strip()
                    # The same OTP Group can accidentally exist more than once in
                    # settings; send only once per destination chat.
                    if _fw_chat_key and _fw_chat_key in _sent_group_ids:
                        logger.info(f'Skipping duplicate OTP Group destination: {_fw_chat_key}')
                        continue
                    if _fw_chat_key:
                        _sent_group_ids.add(_fw_chat_key)
                    _reset_btn_counter()
                    kb = [[{'text': f'{otp}', 'icon_custom_emoji_id': _OTP_COPY_EMOJI_ID, 'copy_text': {'text': otp}, 'style': _rs()}]]
                    _fw_btns = []
                    for btn in fw.get('buttons', []):
                        if str(btn.get('text', '')).strip().lower() == 'full message':
                            continue
                        _fw_btns.append(_make_fw_btn(btn, kb))
                    for _i in range(0, len(_fw_btns), 2):
                        kb.append(_fw_btns[_i:_i + 2])
                    res_fw = send_message(fw['chat_id'], group_msg, reply_markup={'inline_keyboard': kb})
                    if not (res_fw and res_fw.get('ok')):
                        logger.warning(f"Panel group send failed ({fw.get('chat_id')}): {res_fw}")
                        _notify_owner_panel_issue(f"fw_send_fail_{fw.get('chat_id')}", f"Message delivery to OTP Group (<code>{fw.get('chat_id')}</code>) is failing.\nReason: {res_fw}\nVerify that the Group ID is correct and that the bot is an admin/member in the group.")
                except Exception as e:
                    logger.warning(f"Panel group delivery error ({fw.get('chat_id')}): {e}")
            for owner_id in owners:
                try:
                    country_full_name = _country_full_name_from_iso(iso)
                    clean_number = str(display_num).replace('+', '').replace(' ', '').strip()
                    service_name_for_inbox = detect_service(msg_text) or app_full_name
                    service_full_name, service_icon_html = get_service_info_html(service_name_for_inbox, msg_text)
                    inbox_msg = render_body_text(f'<b>{get_flag_info_html(clean_number)} {html.escape(country_full_name)} {service_icon_html} {html.escape(service_full_name)}</b>\n➖➖➖➖➖➖➖➖➖➖\n📞 <b>NUMBER:</b> <code>{clean_number}</code>')
                    _reset_btn_counter()
                    inbox_kb = [[{'text': f'OTP {otp}', 'icon_custom_emoji_id': _OTP_COPY_EMOJI_ID, 'copy_text': {'text': str(otp)}, 'style': _rs()}]]
                    reward = _get_effective_otp_reward(owner_id, clean_number)
                    if reward > 0:
                        update_balance(owner_id, reward)
                        inbox_kb.append([{'text': f'Added {reward:g}৳', 'icon_custom_emoji_id': '5420396762189831222', 'callback_data': 'ignore', 'style': _rs()}])
                    send_message(owner_id, inbox_msg, reply_markup={'inline_keyboard': inbox_kb}, protect_from_menu_cleanup=True)
                    _increment_local_user(owner_id, 'total_otps', 1)
                except Exception as e:
                    logger.warning(f'Panel user delivery error ({owner_id}): {e}')
            try:
                with _data_lock:
                    otp_received_numbers.add(clean_api_num)
            except Exception as e:
                logger.warning(f'panel_monitor otp_received error: {e}')
        except Exception as e:
            logger.warning(f'_process_panel_otps item error: {e}')
    if panel_needs_warmup:
        p['needs_warmup'] = False
        save_local_db()
        logger.info(f'Panel warmup done — old OTPs skipped.')

def _eagerly_warmup_panel(idx, p):
    """Jab panel ON hota hai tab TURANT ek fetch karo aur sare existing OTPs mark karo.
    panel_monitor_thread se race condition eliminate — panel ON hone ke 0.5s baad chalta hai.
    Agar fetch fail ho, needs_warmup=True rahta hai — panel_monitor_thread pehle iteration
    mein warmup kar lega (backup protection)."""
    try:
        time.sleep(0.10)
        if not p.get('needs_warmup', True):
            logger.info(f'Eager warmup skipped — monitor already warmed up.')
            return
        if p.get('type') == 'Auto Captcha Panel':
            data = _fetch_captcha_panel_data(idx, p)
        elif p.get('api_url') or p.get('full_api_url'):
            data = _fetch_api_panel_data(idx, p)
        else:
            data = None
        if data:
            _process_panel_otps(idx, p, data)
            logger.info(f'Eager warmup done for panel: {len(data)} OTPs pre-marked.')
    except Exception as e:
        logger.warning(f"Eager warmup error for panel '{p.get('name')}': {e}")

def panel_monitor_thread():
    """Saare panels ko PARALLEL threads mein poll karo — ek slow panel doosre ko block na kare.
    Delivery delay: ~1-2 seconds (was up to minutes when panels ran sequentially).
    Har panel apna warmup khud karta hai (needs_warmup flag) — global first_run nahi."""
    for p in bot_settings.get('panels', []):
        p['last_fetch_time'] = 0
        p['needs_warmup'] = True

    def _fetch_one(args):
        """Single panel fetch — ThreadPoolExecutor mein parallel run hota hai."""
        idx, p = args
        p_type = p.get('type', 'API Panel')
        if p_type == 'Auto Captcha Panel':
            data = _fetch_captcha_panel_data(idx, p)
        elif p.get('api_url') or p.get('full_api_url'):
            if time.time() - p.get('last_fetch_time', 0) < 5:
                return (idx, p, None)
            p['last_fetch_time'] = time.time()
            data = _fetch_api_panel_data(idx, p)
        else:
            return (idx, p, None)
        return (idx, p, data)
    with ThreadPoolExecutor(max_workers=30) as executor:
        while True:
            try:
                active = [(idx, p) for idx, p in enumerate(bot_settings.get('panels', [])) if p.get('status') == 'ON']
                if active:
                    futures = {executor.submit(_fetch_one, args): args for args in active}
                    for future in list(futures.keys()):
                        try:
                            idx, p, parsed_data = future.result(timeout=8)
                            if parsed_data:
                                _process_panel_otps(idx, p, parsed_data)
                        except Exception as e:
                            logger.warning(f'panel_monitor fetch/process error: {e}')
            except Exception as e:
                logger.warning(f'panel_monitor_thread error: {e}')
            _save_processed_otps()
            if not hasattr(_cleanup_stale_sessions, '_last') or time.time() - _cleanup_stale_sessions._last > 300:
                _cleanup_stale_sessions()
                _cleanup_stale_sessions._last = time.time()
            time.sleep(1)
user_cache = {}

def get_user(user_id):
    uid = int(user_id) if str(user_id).lstrip('-').isdigit() else user_id
    if uid in user_cache:
        return user_cache[uid]
    data = _get_local_user(uid)
    if len(user_cache) > 1000:
        for k in list(user_cache.keys())[:200]:
            user_cache.pop(k, None)
    user_cache[uid] = data
    return data

def update_balance(user_id, amount):
    _increment_local_user(user_id, 'balance', float(amount))
    user_cache.pop(user_id, None)
    user_cache.pop(str(user_id), None)

def _parse_btn_from_text(text, entities):
    """Parse 'BtnText - https://url' with optional custom_emoji from entities or emoji ID prefix.
    Formats supported:
      Button Text - https://link.com
      6228781436330054904 Button Text - https://link.com   (numeric emoji ID prefix)
      [premium emoji] Button Text - https://link.com       (actual premium emoji in message)
    """
    if '-' not in text:
        return None
    parts = text.split('-', 1)
    btn_text = parts[0].strip()
    btn_url = parts[1].strip()
    emoji_id = None
    emoji_char = ''
    id_match = re.match('^(\\d{15,20})\\s+(.*)', btn_text)
    if id_match:
        emoji_id = id_match.group(1)
        btn_text = id_match.group(2).strip()
    else:
        for ent in entities:
            if ent.get('type') == 'custom_emoji':
                emoji_id = ent.get('custom_emoji_id')
                offset = ent.get('offset', 0)
                length = ent.get('length', 0)
                b_text = text.encode('utf-16-le')
                emoji_char = b_text[offset * 2:(offset + length) * 2].decode('utf-16-le')
                break
        if emoji_char:
            btn_text = btn_text.replace(emoji_char, '').strip()
    btn_data = {'text': btn_text, 'url': btn_url, 'style': _rs()}
    if emoji_id:
        btn_data['icon_custom_emoji_id'] = emoji_id
    return btn_data

def _build_2fa_code_txt(entry_name, code, remaining_time):
    """2FA result layout requested by the user, using premium custom emojis."""
    return (
        "<tg-emoji emoji-id=\"6231229503264267384\">🔐</tg-emoji> <b>2FA CODE</b>\n"
        "➖➖➖➖➖➖➖\n"
        f"<tg-emoji emoji-id=\"6046412391887935443\">🔢</tg-emoji> <code>{code}</code>\n"
        "➖➖➖➖➖➖➖\n"
        f"<tg-emoji emoji-id=\"5807903945883917416\">⏳</tg-emoji> <b>Expires in:</b> {remaining_time}s"
    )


def _build_2fa_refresh_txt(code, remaining_time):
    """Short loading state shown briefly when Refresh is tapped."""
    return (
        "<tg-emoji emoji-id=\"6231229503264267384\">🔐</tg-emoji> <b>2FA CODE</b>\n"
        "➖➖➖➖➖➖➖\n"
        "<tg-emoji emoji-id=\"6046412391887935443\">🔢</tg-emoji> <code>••••••</code>\n"
        "➖➖➖➖➖➖➖\n"
        "<tg-emoji emoji-id=\"5807903945883917416\">⏳</tg-emoji> <b>Refreshing...</b>"
    )


def _build_2fa_code_kb(code, secret):
    """Tap-to-copy code plus Refresh and Back."""
    _reset_btn_counter()
    return [
        [{"text": "Refresh", "icon_custom_emoji_id": "5420155432272438703", "callback_data": f"ref_2fa_{secret}", "style": _rs()}],
        [{"text": "Back", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "cancel_2fa", "style": _rs()}],
    ]


def _show_2fa_menu(chat_id, msg_id=None):
    """Show the requested 2FA input screen and arm the next key message."""
    txt = (
        "<tg-emoji emoji-id=\"6231229503264267384\">🔐</tg-emoji> <b>2FA ONLINE</b>\n"
        "➖➖➖➖➖➖➖➖➖\n"
        "<tg-emoji emoji-id=\"4958900559139570572\">🔑</tg-emoji> <b>Enter Your 2FA Key:</b>"
    )
    _reset_btn_counter()
    kb = [[{"text": "Close", "icon_custom_emoji_id": "5420130255174145507", "callback_data": "close_msg", "style": _rs()}]]

    user_states[chat_id] = "wait_for_2fa_key"
    if msg_id:
        temp_data[chat_id] = {"msg_id": msg_id, "2fa_name": "My 2FA"}
        edit_message(chat_id, msg_id, render_body_text(txt), reply_markup={"inline_keyboard": kb})
    else:
        resp = send_message(chat_id, render_body_text(txt), reply_markup={"inline_keyboard": kb})
        sent_id = ((resp or {}).get("result") or {}).get("message_id") if isinstance(resp, dict) else None
        if sent_id:
            temp_data[chat_id] = {"msg_id": sent_id, "2fa_name": "My 2FA"}


def _show_2fa_key_input(chat_id, msg_id):
    txt = (
        "<tg-emoji emoji-id=\"6231229503264267384\">🔐</tg-emoji> <b>2FA ONLINE</b>\n"
        "➖➖➖➖➖➖➖➖➖\n"
        "<tg-emoji emoji-id=\"4958900559139570572\">🔑</tg-emoji> <b>Enter Your 2FA Key:</b>"
    )
    _reset_btn_counter()
    kb = {"inline_keyboard":[[{"text":"Close","icon_custom_emoji_id":"5420130255174145507","callback_data":"close_msg","style":_rs()}]]}
    edit_message(chat_id, msg_id, render_body_text(txt), reply_markup=kb)


def get_cancel_kb():
    _reset_btn_counter()
    return {'inline_keyboard': [[{'text': 'Close', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': 'close_msg', 'style': _rs()}]]}

def main_menu(user_id):
    _reset_btn_counter()
    kb = [[{'text': 'GET NUMBER', 'icon_custom_emoji_id': '5337132498965010628', 'style': 'success'}], [{'text': 'LIVE TRAFFIC', 'icon_custom_emoji_id': '5353032893096567467', 'style': 'primary'}, {'text': 'DEPOSIT', 'icon_custom_emoji_id': '5348469219761626211', 'style': 'primary'}], [{'text': 'BALANCE', 'icon_custom_emoji_id': '5190576863226933563', 'style': 'success'}, {'text': 'SUPPORT', 'icon_custom_emoji_id': '5420145051336485498', 'style': 'success'}]]

    if is_admin(user_id):
        kb.append([{'text': 'Admin Panel', 'icon_custom_emoji_id': '5420155432272438703', 'style': 'danger'}])
    return {'keyboard': kb, 'resize_keyboard': True}

def get_admin_text():
    users_count = len(all_known_users)
    total_files = len(number_batches)
    available_nums = sum((len(b['numbers']) for b in number_batches.values()))
    txt = f"\n{PEM['admin']} <b>ADMIN CONTROL PANEL</b> {PEM['admin']}\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n{PEM['graph']} <b>DATABASE OVERVIEW</b>\n— — — — — — — — — —\n{PEM['user']} Users      » {users_count}\n{PEM['file']} Files      » {total_files}\n{PEM['num']} Numbers    » {total_uploaded_stats}\n{PEM['ok']} Assigned   » {total_assigned_stats}\n{PEM['rocket']} Available  » {available_nums}\n\n{PEM['graph']} <b>STOCK LEVEL</b>\n— — — — — — — — — —\n[██████░░░░░░░░░] {available_nums} free\n"
    return render_body_text(txt)

def admin_panel_keyboard():
    _reset_btn_counter()
    return {'inline_keyboard': [
        [
            {'text': 'LEADER BOARD SYSTEM', 'icon_custom_emoji_id': '5353032893096567467', 'callback_data': 'lb_main', 'style': _rs()},
            {'text': 'Upload Number', 'icon_custom_emoji_id': '5353001161878182134', 'callback_data': 'upload_num', 'style': _rs()}
        ],
        [
            {'text': 'Delete files', 'icon_custom_emoji_id': '5422557736330106570', 'callback_data': 'delete_files', 'style': _rs()},
            {'text': 'Broadcast', 'icon_custom_emoji_id': '5789428375261023681', 'callback_data': 'broadcast_msg', 'style': _rs()}
        ],
        [
            {'text': 'System', 'icon_custom_emoji_id': '5420155432272438703', 'callback_data': 'system_settings', 'style': _rs()},
            {'text': 'Used (OTP Received)', 'icon_custom_emoji_id': '5352694861990501856', 'callback_data': 'show_used', 'style': _rs()}
        ],
        [
            {'text': 'Unused (No OTP)', 'icon_custom_emoji_id': '5352597830089347330', 'callback_data': 'show_unused', 'style': _rs()},
            {'text': 'Close', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': 'close_msg', 'style': _rs()}
        ]
    ]}

def system_settings_keyboard():
    _reset_btn_counter()
    return {'inline_keyboard': [
        [
            {'text': 'AUTO MODE', 'icon_custom_emoji_id': '6318566568011764192', 'callback_data': 'auto_mode', 'style': _rs()},
            {'text': 'Test', 'icon_custom_emoji_id': '5190781475468915802', 'callback_data': 'test_message_flow', 'style': _rs()}
        ],
        [
            {'text': 'Force Join System', 'icon_custom_emoji_id': '5420517437885943844', 'callback_data': 'manage_fj', 'style': _rs()},
            {'text': 'Admin Management', 'icon_custom_emoji_id': '5420145051336485498', 'callback_data': 'manage_admins', 'style': _rs()}
        ],
        [
            {'text': 'OTP Group', 'icon_custom_emoji_id': '5190447043545438788', 'callback_data': 'manage_otp_groups', 'style': _rs()},
            {'text': 'User Management', 'icon_custom_emoji_id': '5193063022226086560', 'callback_data': 'user_management', 'style': _rs()}
        ],
        [
            {'text': 'Panel MANAGEMENT', 'icon_custom_emoji_id': '5336879280578138635', 'callback_data': 'manage_panels', 'style': _rs()},
            {'text': 'BOT Control', 'icon_custom_emoji_id': '5193100774988617665', 'callback_data': 'abhi_control', 'style': _rs()}
        ],
        [
            {'text': 'Premium Emoji', 'icon_custom_emoji_id': '5352552689983067014', 'callback_data': 'manage_emojis', 'style': _rs()},
            {'text': 'Menu Design', 'icon_custom_emoji_id': '5190751148704833975', 'callback_data': 'menu_design_list', 'style': _rs()}
        ],
        [
            {'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'back_to_admin', 'style': _rs()}
        ]
    ]}
_SYS_BTN_EMOJIS = [('Back', '5267490665117275176'), ('Add New', '5352552689983067014'), ('Check Joined', '5352694861990501856'), ('Close', '5420130255174145507'), ('GET NUMBER', '5337132498965010628'), ('LIVE TRAFFIC', '5353032893096567467'), ('BALANCE', '5190576863226933563'), ('2FA ONLINE', '5337255927735163754'), ('REFER & EARN', '5420396762189831222'), ('WITHDRAWAL', '5352585194295564660'), ('SUPPORT', '5420145051336485498'), ('Admin Panel', '5420155432272438703'), ('LEADER BOARD SYSTEM', '5353032893096567467'), ('Upload Number', '5353001161878182134'), ('Delete files', '5422557736330106570'), ('Broadcast', '5789428375261023681'), ('System', '5420155432272438703'), ('Used (OTP Received)', '5352694861990501856'), ('Unused (No OTP)', '5352597830089347330'), ('Force Join System', '5420517437885943844'), ('Admin Management', '5420145051336485498'), ('OTP Group', '5190447043545438788'), ('User Management', '5193063022226086560'), ('Panel MANAGEMENT', '5336879280578138635'), ('BOT Control', '5193100774988617665'), ('Premium Emoji', '5352552689983067014'), ('Menu Design', '5190751148704833975'), ('All System Emoji', '5352552689983067014'), ('Download System Emoji', '5257969839313526622'), ('Manage Balance', '5190576863226933563'), ('Ban/Unban User', '5334807341109908955'), ('User Profile', '5352861489541714456'), ('Edit /start Menu', '5395444784611480792'), ('Edit GET NUMBER', '5337132498965010628'), ('Edit Select Country', '5336972142066047577'), ('Edit TRAFFIC', '5353032893096567467'), ('Edit Refer', '5420396762189831222'), ('Edit WITHDRAWAL', '5352585194295564660'), ('Edit SUPPORT', '5420145051336485498'), ('Reset Defaults', '5192812028632274956'), ('Back to Menus', '5267490665117275176'), ('All Uploading System', '5353001161878182134'), ('All Deleting System', '5422557736330106570'), ('All Downloading System', '5257969839313526622'), ('Upload Flags (TXT)', '5353001161878182134'), ('Download Flags', '5257969839313526622'), ('Upload Services (TXT)', '5353001161878182134'), ('Download Services', '5257969839313526622'), ('Delete All Flags', '5422557736330106570'), ('Delete All Services', '5422557736330106570'), ('Add Channel / Group', '5420323438508155202'), ('Add Admin', '5420323438508155202'), ('Edit OTP Button Link', '5420517437885943844'), ('Add Forward Group', '5420323438508155202'), ('W. METHODS', '5190899075968441286'), ('BACK', '5267490665117275176'), ('Add Method', '5420323438508155202'), ('Add New Provider', '5420323438508155202'), ('Back to Providers', '5267490665117275176'), ('Refresh', '5420155432272438703'), ('Add Country Code', '5420323438508155202'), ('Try Again', '5420323438508155202'), ('CLOSE', '5420130255174145507'), ('Contact Support', '5337302974806922068'), ('Remove country code', '6206108815075579644'), ('Add country code', '6206375377925839184'), ('Change Number', '6264896248659056036'), ('Change Number', '6264896248659056036'), ('Download TXT', '5257969839313526622'), ('Top Referrers', '5420145051336485498'), ('Top OTP Receivers', '5353001161878182134'), ('Withdrawal History', '5348469219761626211'), ('Back to Admin', '5267490665117275176'), ('Add New Service', '5420323438508155202'), ('Back to System', '5267490665117275176'), ('Full Message', '5303138782004924588'), ('Test Connection', '5276032951342088188'), ('Delete Provider', '5336944168944047463'), ('COOLDOWN', '5337172996211648018'), ('NUM/SHARE', '5352862640592949843'), ('MIN WITHDRAW', '5352877703043258544'), ('Add Country', '5420323438508155202'), ('Add Inline Button', '5420323438508155202'), ('Add Range', '5420323438508155202'), ('APPROVE', '5352694861990501856'), ('Cancel', '5420130255174145507'), ('Click to copy', '5353022963132174959'), ('COPY LINK', '5192739271886282680'), ('Del', '5422557736330106570'), ('Delete Entire Country', '5422557736330106570'), ('Delete Entire Group', '5422557736330106570'), ('Delete Service', '5422557736330106570'), ('Edit Body (Text)', '5395444784611480792'), ('Edit Inline Buttons', '5420155432272438703'), ('Full API (URL+Token)', '5420517437885943844'), ('Group Not Found', '5420130255174145507'), ('How to Use', '6282760761399841824'), ('Next', '6264699552041801361'), ('Panel Not Found', '5420130255174145507'), ('REJECT', '5420130255174145507'), ('Replace', '5395444784611480792'), ('Set API URL', '5420517437885943844'), ('Set Token', '5353022963132174959'), ('Group: (Forward Group)', '5193063022226086560'), ('Owner: (Admin)', '5353032893096567467')]
_SYS_MSG_EMOJIS = [('PEM:ok', '5352694861990501856', '✅', 'PEM["ok"] — success messages'), ('PEM:no', '6267000941547885720', '❌', 'PEM["no"] — error messages'), ('PEM:warn', '5336944168944047463', '⚠️', 'PEM["warn"] — warning messages'), ('PEM:admin', '5353032893096567467', '📊', 'PEM["admin"] — admin panel header'), ('PEM:user', '5352861489541714456', '👤', 'PEM["user"] — user profile'), ('PEM:file', '5352721946054268944', '📁', 'PEM["file"] — file references'), ('PEM:rocket', '5352597830089347330', '🚀', 'PEM["rocket"] — unused numbers'), ('PEM:graph', '5352877703043258544', '📊', 'PEM["graph"] — stats/graph'), ('PEM:money', '5348469219761626211', '💸', 'PEM["money"] — balance/money'), ('PEM:gift', '5420396762189831222', '🎁', 'PEM["gift"] — referral rewards'), ('PEM:msg', '5337302974806922068', '💬', 'PEM["msg"] — message/support'), ('PEM:gear', '5420155432272438703', '⚙️', 'PEM["gear"] — system settings header'), ('PEM:link', '5420517437885943844', '🔗', 'PEM["link"] — force join links'), ('PEM:trash', '5422557736330106570', '🗑', 'PEM["trash"] — delete actions'), ('PEM:upload', '5353001161878182134', '📤', 'PEM["upload"] — upload prompts'), ('PEM:world', '5336972142066047577', '🌐', 'PEM["world"] — country select'), ('PEM:lock', '5353022963132174959', '🔐', 'PEM["lock"] — 2FA/security'), ('PEM:num', '5352862640592949843', '🔢', 'PEM["num"] — search number prompt'), ('PEM:pin', '5352922460897452503', '📍', 'PEM["pin"] — select service prompt'), ('PEM:star', '5352552689983067014', '✨', 'PEM["star"] — emoji management header'), ('PEM:hi', '5353027129250453493', '👋', 'PEM["hi"] — welcome/main menu'), ('GBE:✅', '5352694861990501856', '✅', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:❌', '5420130255174145507', '❌', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:⚠️', '5336944168944047463', '⚠️', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🔥', '5337267511261960341', '🔥', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🌟', '5337102391244263212', '🌟', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:✨', '5352552689983067014', '✨', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:➖', '5870818207383686839', '➖', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:➕', '5420323438508155202', '➕', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:➡️', '6319061296704656261', '➡️', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🔄', '6264896248659056036', '🔄', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:⌛', '4958503072801228000', '⌛', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:⏳', '6285092198497129798', '⏳', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🕓', '5336983442125001376', '🕓', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🔴', '6267237615720731788', '🔴', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:👤', '5352861489541714456', '👤', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:👥', '4972130076318500235', '👥', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:👋', '5353027129250453493', '👋', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:👇', '5406745015365943482', '👇', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:😒', '5334763399299506604', '😒', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:😔', '6120863614149596295', '😔', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🫂', '5420145051336485498', '🫂', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:1️⃣', '5877664071720898423', '1️⃣', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:2️⃣', '5877223446731034464', '2️⃣', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:3️⃣', '5879546817879740639', '3️⃣', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:4️⃣', '5879844832775507443', '4️⃣', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:5️⃣', '5879657954453491518', '5️⃣', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:6️⃣', '5877556203617259178', '6️⃣', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:7️⃣', '5879611822209765566', '7️⃣', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:8️⃣', '5879971663159758717', '8️⃣', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:9️⃣', '5877752470737784316', '9️⃣', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🔢', '5352862640592949843', '🔢', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:📊', '5353032893096567467', '📊', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:📈', '5352877703043258544', '📈', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:📁', '5352721946054268944', '📁', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:📂', '5257969839313526622', '📂', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:📤', '5353001161878182134', '📤', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:📝', '5192739271886282680', '📝', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:📅', '5352585194295564660', '📅', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:📋', '6267008582294705964', '📋', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:💾', '5197269100878907942', '💾', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:📛', '6325731252066325108', '📛', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:💬', '5337302974806922068', '💬', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🎙', '5355102594886833928', '🎙', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:📢', '5789428375261023681', '📢', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:📌', '5318986077455795572', '📌', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:📍', '5352922460897452503', '📍', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🔑', '6282760761399841824', '🔑', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🔐', '5337255927735163754', '🔐', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🔗', '5420517437885943844', '🔗', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:⚙️', '5420155432272438703', '⚙️', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🛡', '5190447043545438788', '🛡', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🚫', '5334807341109908955', '🚫', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🌐', '6266794310671275367', '🌐', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🔒', '6282846669335702032', '🔒', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:💸', '5348469219761626211', '💸', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:💰', '4958926882994127612', '💰', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:💎', '5352838545826420397', '💎', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:💳', '5190899075968441286', '💳', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🎁', '5420396762189831222', '🎁', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🤝', '5192805934073685937', '🤝', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🚀', '5352597830089347330', '🚀', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🍏', '5337132498965010628', '🍏', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🌍', '5780471598922337683', '🌍', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🗑', '5422557736330106570', '🗑', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🟢', '5192812028632274956', '🟢', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:👀', '5190645917711114179', '👀', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🕹', '5193100774988617665', '🕹', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🧪', '5190781475468915802', '🧪', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🎨', '5190751148704833975', '🎨', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:💡', '5422439311196834318', '💡', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('GBE:🎯', '5276032951342088188', '🎯', 'GLOBAL_BODY_EMOJIS — rendered in all body text'), ('HC:start_📊', '6264778055454036969', '📊', '/start text — NUMBER BOT header icon'), ('HC:start_🚀', '5258332798409783582', '🚀', '/start text — Welcome rocket'), ('HC:start_✅', '6071001861341580968', '✅', '/start text — Choose option below'), ('HC:start_💎', '6073231507713954071', '💎', '/start text — Premium OTP Service'), ('HC:otp_✅', '6266994443262367483', '✅', 'OTP flow — check (received)'), ('HC:otp_▶2', '6264896248659056036', '▶', 'OTP result — separator arrow'), ('HC:mask_⭐', '6228781436330054904', '⭐', '_MASK_EMOJI — number masking star'), ('HC:2fa_👉', '5416117059207572332', '👉', '2FA guide — pointing finger'), ('HC:am_✅ON', '6266827283135207188', '✅', 'Auto Mode — ON indicator'), ('HC:am_🔴OFF', '6267237615720731788', '🔴', 'Auto Mode — OFF indicator'), ('HC:am_⚡', '6318566568011764192', '⚡', 'Auto Mode — header bolt icon'), ('HC:panel_🔹', '6282760761399841824', '🔹', 'Panel control — Nexa/VoltX/Stex header')]
_EMOJI_CHANGE_LOG: dict = {}

def _build_id_override_map(overrides: dict) -> dict:
    """Convert msg_N overrides to {orig_id: new_id} map for message TEXT replacement.
    btn_N entries are intentionally excluded here — buttons are matched by TEXT
    (see _build_btn_text_override_map) so that changing one button's emoji does NOT
    accidentally change other buttons that share the same emoji ID."""
    id_map = {}
    for key, new_id in overrides.items():
        if key.startswith('msg_'):
            try:
                idx = int(key[4:])
                if 0 <= idx < len(_SYS_MSG_EMOJIS):
                    orig_id = _SYS_MSG_EMOJIS[idx][1]
                    id_map[orig_id] = new_id
            except ValueError:
                id_map[key] = new_id
        elif not key.startswith('btn_'):
            id_map[key] = new_id
    return id_map

def _build_btn_text_override_map(overrides: dict) -> dict:
    """Build a {button_text_lower: new_id} map for button keyboard overrides.
    Matching by button TEXT instead of emoji ID ensures that changing one specific
    button's emoji only affects that button — even when multiple buttons share
    the same original emoji ID (e.g. 'Premium Emoji' aur 'All System Emoji' ka
    same ID hai, lekin dono alag-alag change honge)."""
    text_map = {}
    for key, new_id in overrides.items():
        if key.startswith('btn_'):
            try:
                idx = int(key[4:])
                if 0 <= idx < len(_SYS_BTN_EMOJIS):
                    btn_text = _SYS_BTN_EMOJIS[idx][0]
                    text_map[btn_text.lower().strip()] = new_id
            except ValueError:
                pass
    return text_map

def _build_btn_id_fallback_map(overrides: dict) -> dict:
    """ID-based fallback map for btn_N overrides.

    Kuch buttons ka text runtime pe DYNAMIC hota hai — jaise OTP value,
    'COOLDOWN: 30s', 'Explore WhatsApp Range', 'NUM/SHARE: 5', etc.
    Inka actual button text _SYS_BTN_EMOJIS ke registered label se match
    nahi karta, isliye text_map lookup fail ho jaata hai.

    Yeh fallback un buttons ke liye kaam karta hai:
    — sirf un orig_ids ko include karta hai jinka _SYS_BTN_EMOJIS mein
      exactly ONE entry hai (unique ID) — is se koi ambiguity nahi hoti
      aur ek button ka change kisi aur button ko affect nahi karta.
    — Multiple entries wale shared IDs (e.g. Back, Add New, etc.) EXCLUDE
      kiye jaate hain kyunki unke saare buttons static text hain aur
      text_map se pehle hi handle ho jaate hain."""
    from collections import Counter
    id_count = Counter((orig_id for _, orig_id in _SYS_BTN_EMOJIS))
    id_map = {}
    for key, new_id in overrides.items():
        if key.startswith('btn_'):
            try:
                idx = int(key[4:])
                if 0 <= idx < len(_SYS_BTN_EMOJIS):
                    orig_id = _SYS_BTN_EMOJIS[idx][1]
                    if id_count[orig_id] == 1:
                        id_map[orig_id] = new_id
            except ValueError:
                pass
    return id_map

def _apply_emoji_overrides(reply_markup: dict) -> dict:
    """Replace icon_custom_emoji_id values in ANY keyboard type with admin overrides.
    Handles both InlineKeyboardMarkup ('inline_keyboard') and
    ReplyKeyboardMarkup ('keyboard') so main_menu buttons are also overridden.

    Three-layer lookup — STRICT separation: btn_N overrides ONLY affect buttons,
    msg_N overrides ONLY affect message text (handled in _apply_text_overrides).

    Layer 1 — Text match (btn_N):
        Static-text buttons matched by their exact registered label.
        Changing btn_1 (Back) changes ALL 'Back' buttons but NOTHING else.

    Layer 2 — ID fallback (btn_N, unique-ID only):
        Dynamic-text buttons (OTP code showing actual OTP, 'COOLDOWN: 30s',
        'Explore X Range', etc.) whose runtime text ≠ registered label.
        Only applied when the emoji ID is unique in _SYS_BTN_EMOJIS —
        guarantees one btn_N change never bleeds into another button type.

    Layer 3 — Legacy plain-key (backward compat only, no btn_/msg_ prefix):
        Old overrides saved before the btn_N/msg_N system was introduced."""
    overrides = bot_settings.get('sys_emoji_overrides', {})
    if not overrides:
        return reply_markup
    text_map = _build_btn_text_override_map(overrides)
    id_fallback = _build_btn_id_fallback_map(overrides)
    id_legacy = {k: v for k, v in overrides.items() if not k.startswith('btn_') and (not k.startswith('msg_'))}
    if not text_map and (not id_fallback) and (not id_legacy):
        return reply_markup
    rm = copy.deepcopy(reply_markup)

    def _patch_btn(btn):
        btn_text_lower = btn.get('text', '').lower().strip()
        if btn_text_lower and btn_text_lower in text_map:
            btn['icon_custom_emoji_id'] = text_map[btn_text_lower]
            return
        eid = btn.get('icon_custom_emoji_id')
        if not eid:
            return
        if id_fallback and eid in id_fallback:
            btn['icon_custom_emoji_id'] = id_fallback[eid]
            return
        if id_legacy and eid in id_legacy:
            btn['icon_custom_emoji_id'] = id_legacy[eid]
    for row in rm.get('inline_keyboard', []):
        for btn in row:
            _patch_btn(btn)
    for row in rm.get('keyboard', []):
        for btn in row:
            _patch_btn(btn)
    return rm
_SYS_EMJ_PAGE_SIZE = 5

def _sys_btn_emoji_page_keyboard(page: int) -> dict:
    _reset_btn_counter()
    overrides = bot_settings.get('sys_emoji_overrides', {})
    total = len(_SYS_BTN_EMOJIS)
    pages = max(1, (total + _SYS_EMJ_PAGE_SIZE - 1) // _SYS_EMJ_PAGE_SIZE)
    page = max(0, min(page, pages - 1))
    start = page * _SYS_EMJ_PAGE_SIZE
    items = _SYS_BTN_EMOJIS[start:start + _SYS_EMJ_PAGE_SIZE]
    kb = []
    for idx, (btn_text, orig_id) in enumerate(items):
        global_idx = start + idx
        real_id = overrides.get(f'btn_{global_idx}', orig_id)
        label = f'{btn_text[:30]}'
        kb.append([{'text': label, 'icon_custom_emoji_id': real_id, 'callback_data': 'ignore', 'style': _rs()}, {'text': 'Replace', 'icon_custom_emoji_id': '5395444784611480792', 'callback_data': f'rm_btn_emoji_{global_idx}', 'style': _rs()}])
    nav = []
    if page > 0:
        nav.append({'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'btn_emoji_page_{page - 1}', 'style': _rs()})
    if page < pages - 1:
        nav.append({'text': 'Next', 'icon_custom_emoji_id': '6264699552041801361', 'callback_data': f'btn_emoji_page_{page + 1}', 'style': _rs()})
    if nav:
        kb.append(nav)
    kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'all_system_emoji', 'style': _rs()}])
    return {'inline_keyboard': kb}

def _sys_msg_emoji_page_keyboard(page: int) -> dict:
    _reset_btn_counter()
    overrides = bot_settings.get('sys_emoji_overrides', {})
    total = len(_SYS_MSG_EMOJIS)
    pages = max(1, (total + _SYS_EMJ_PAGE_SIZE - 1) // _SYS_EMJ_PAGE_SIZE)
    page = max(0, min(page, pages - 1))
    start = page * _SYS_EMJ_PAGE_SIZE
    items = _SYS_MSG_EMOJIS[start:start + _SYS_EMJ_PAGE_SIZE]
    kb = []
    for idx, (label, orig_id, char, _usage) in enumerate(items):
        global_idx = start + idx
        real_id = overrides.get(f'msg_{global_idx}', orig_id)
        display = _usage
        kb.append([{'text': display[:50], 'icon_custom_emoji_id': real_id, 'callback_data': 'ignore', 'style': _rs()}, {'text': 'Replace', 'icon_custom_emoji_id': '5395444784611480792', 'callback_data': f'rm_msg_emoji_{global_idx}', 'style': _rs()}])
    nav = []
    if page > 0:
        nav.append({'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'msg_emoji_page_{page - 1}', 'style': _rs()})
    if page < pages - 1:
        nav.append({'text': 'Next', 'icon_custom_emoji_id': '6264699552041801361', 'callback_data': f'msg_emoji_page_{page + 1}', 'style': _rs()})
    if nav:
        kb.append(nav)
    kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'all_system_emoji', 'style': _rs()}])
    return {'inline_keyboard': kb}

def _all_system_emoji_keyboard() -> dict:
    _reset_btn_counter()
    return {'inline_keyboard': [[{'text': f'All Button Emoji ({len(_SYS_BTN_EMOJIS)})', 'icon_custom_emoji_id': '5420155432272438703', 'callback_data': 'btn_emoji_page_0', 'style': _rs()}], [{'text': f'All Message Emoji ({len(_SYS_MSG_EMOJIS)})', 'icon_custom_emoji_id': '5337302974806922068', 'callback_data': 'msg_emoji_page_0', 'style': _rs()}], [{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_emojis', 'style': _rs()}]]}

def _generate_sys_emoji_txt() -> bytes:
    overrides = bot_settings.get('sys_emoji_overrides', {})
    lines = []
    lines.append('=' * 80)
    lines.append('  SYSTEM EMOJI EXPORT — All Button & Message Emojis')
    lines.append('=' * 80)
    lines.append('')
    lines.append('  HOW TO USE THIS FILE:')
    lines.append('  ─────────────────────')
    lines.append('  1. This file contains an index number (#) for every emoji.')
    lines.append('  2. In the bot panel:')
    lines.append('       Admin Panel → System → Premium Emoji → All System Emoji')
    lines.append("       → 'select 'All Button Emoji' or 'All Message Emoji'")
    lines.append('  3. Find the row with the matching #.')
    lines.append("  4. tap 'Replace' and send the NEW emoji ID (digits only).")
    lines.append('     Example new ID: 5352552689983067014')
    lines.append('')
    lines.append('  EXAMPLE — Button Emoji change:')
    lines.append('    #0  Generate 2FA Code  →  Current ID: 5353022963132174959')
    lines.append("    To change this icon, tap 'Replace'")
    lines.append('    and send the new ID. Changed? = YES only when an override is set.')
    lines.append('')
    lines.append('  EXAMPLE — Message Emoji change:')
    lines.append('    #0  PEM:ok  ✅  →  Current ID: 5352694861990501856')
    lines.append('    This is used in ✅ success messages (PEM["ok"]).')
    lines.append('    Replacing this ID changes all success check marks.')
    lines.append('')
    lines.append("  NOTE: 'Changed? = YES ◄' means this emoji already has an override.")
    lines.append("        The ID shown in the 'Current ID' column is what the BOT is currently using.")
    lines.append('')
    lines.append('─' * 80)
    lines.append(f'  BUTTON EMOJIS ({len(_SYS_BTN_EMOJIS)} entries)')
    lines.append('  These emojis are icons for inline keyboard buttons.')
    lines.append('─' * 80)
    lines.append(f"  {'#':<5} {'Button Name':<35} {'Current ID':<22} {'Original ID':<22} {'Changed?'}")
    lines.append(f"  {'─' * 78}")
    for idx, (btn_text, orig_id) in enumerate(_SYS_BTN_EMOJIS):
        new_id = overrides.get(f'btn_{idx}', orig_id)
        changed = 'YES ◄' if new_id != orig_id else ''
        cur_id = new_id
        lines.append(f'  {idx:<5} {btn_text:<35} {cur_id:<22} {orig_id:<22} {changed}')
    lines.append('')
    lines.append('─' * 80)
    lines.append(f'  MESSAGE EMOJIS ({len(_SYS_MSG_EMOJIS)} entries — PEM + GLOBAL_BODY + Hardcoded)')
    lines.append('  These emojis are used inside message text, not on buttons.')
    lines.append('─' * 80)
    lines.append(f"  {'#':<5} {'Label':<18} {'Char':<5} {'Current ID':<22} {'Original ID':<22} {'Usage / Example'}")
    lines.append(f"  {'─' * 78}")
    for idx, (label, orig_id, char, usage) in enumerate(_SYS_MSG_EMOJIS):
        new_id = overrides.get(f'msg_{idx}', orig_id)
        changed_tag = ' [CHANGED ◄]' if new_id != orig_id else ''
        cur_id = new_id
        char_display = char[:4] if char else ''
        lines.append(f'  {idx:<5} {label:<18} {char_display:<5} {cur_id:<22} {orig_id:<22} {usage}{changed_tag}')
    lines.append('')
    lines.append('─' * 80)
    lines.append(f'  CHANGE LOG — {len(_EMOJI_CHANGE_LOG)} change(s) this session')
    lines.append('─' * 80)
    if _EMOJI_CHANGE_LOG:
        for key, (new_id, label) in _EMOJI_CHANGE_LOG.items():
            lines.append(f'  [{label}]  key={key}  →  new_id={new_id}')
    else:
        lines.append('  No changes were recorded in this session.')
    lines.append('')
    lines.append('─' * 80)
    lines.append('  Generated by System Emoji Manager — bot_cc_FINAL_v3.py')
    lines.append('─' * 80)
    return '\n'.join(lines).encode('utf-8')

def get_user_management_text():
    total = len(all_known_users)
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    txt = f'➖➖➖➖➖➖➖➖\n《 👋 USER VIEW 》\n➖➖➖➖➖➖➖➖\n📊 LIVE STATISTICS:\n➖➖➖➖➖➖➖➖\n🫂 TOTAL USERS: {total}\n✅ VERIFIED USERS: (Hidden to save DB Cost)\n🚫 BANNED USERS: (Hidden to save DB Cost)\n➖➖➖➖➖➖➖➖\n⌛ UPDATED: {now_str}'
    return render_body_text(txt)

def user_management_keyboard():
    _reset_btn_counter()
    return {'inline_keyboard': [[{'text': 'Manage Balance', 'icon_custom_emoji_id': '5190576863226933563', 'callback_data': 'um_manage_balance', 'style': _rs()}, {'text': 'Ban/Unban User', 'icon_custom_emoji_id': '5334807341109908955', 'callback_data': 'um_ban_unban', 'style': _rs()}], [{'text': 'User Profile', 'icon_custom_emoji_id': '5352861489541714456', 'callback_data': 'um_user_profile', 'style': _rs()}], [{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'system_settings', 'style': _rs()}]]}

def menu_design_list_keyboard():
    _reset_btn_counter()
    return {'inline_keyboard': [
        [
            {'text': 'Edit /start Menu', 'icon_custom_emoji_id': '5395444784611480792', 'callback_data': 'md_edit_start', 'style': _rs()},
            {'text': 'Edit GET NUMBER', 'icon_custom_emoji_id': '5337132498965010628', 'callback_data': 'md_edit_get_number', 'style': _rs()}
        ],
        [
            {'text': 'Edit Select Country', 'icon_custom_emoji_id': '5336972142066047577', 'callback_data': 'md_edit_select_country', 'style': _rs()},
            {'text': 'Edit TRAFFIC', 'icon_custom_emoji_id': '5353032893096567467', 'callback_data': 'md_edit_traffic', 'style': _rs()}
        ],
        [
            {'text': 'Edit Refer', 'icon_custom_emoji_id': '5420396762189831222', 'callback_data': 'md_edit_refer', 'style': _rs()},
            {'text': 'Edit WITHDRAWAL', 'icon_custom_emoji_id': '5352585194295564660', 'callback_data': 'md_edit_withdrawal', 'style': _rs()}
        ],
        [
            {'text': 'Edit SUPPORT', 'icon_custom_emoji_id': '5420145051336485498', 'callback_data': 'md_edit_support', 'style': _rs()},
            {'text': 'Reset Defaults', 'icon_custom_emoji_id': '5192812028632274956', 'callback_data': 'md_reset_defaults', 'style': _rs()}
        ],
        [
            {'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'system_settings', 'style': _rs()}
        ]
    ]}

def menu_edit_options_keyboard(menu_key):
    _reset_btn_counter()
    return {'inline_keyboard': [[{'text': 'Edit Body (Text)', 'icon_custom_emoji_id': '5395444784611480792', 'callback_data': f'md_text_{menu_key}', 'style': _rs()}], [{'text': 'Edit Inline Buttons', 'icon_custom_emoji_id': '5420155432272438703', 'callback_data': f'md_btns_{menu_key}', 'style': _rs()}], [{'text': 'Back to Menus', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'menu_design_list', 'style': _rs()}]]}

def menu_buttons_list_keyboard(menu_key):
    _reset_btn_counter()
    kb = []
    btns = bot_settings['custom_messages'].get(menu_key, {}).get('buttons', [])
    for idx, btn in enumerate(btns):
        kb.append([{'text': f"Del: {btn['text']}", 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'md_delbtn_{menu_key}_{idx}', 'style': _rs()}])
    kb.append([{'text': 'Add Inline Button', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': f'md_addbtn_{menu_key}', 'style': _rs()}])
    kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'md_edit_{menu_key}', 'style': _rs()}])
    return {'inline_keyboard': kb}

def emoji_settings_keyboard():
    _reset_btn_counter()
    return {'inline_keyboard': [[{'text': 'All Uploading System', 'icon_custom_emoji_id': '5353001161878182134', 'callback_data': 'emoji_upload_menu', 'style': _rs()}], [{'text': 'All Deleting System', 'icon_custom_emoji_id': '5422557736330106570', 'callback_data': 'emoji_delete_menu', 'style': _rs()}], [{'text': 'All Downloading System', 'icon_custom_emoji_id': '5257969839313526622', 'callback_data': 'emoji_download_menu', 'style': _rs()}], [{'text': 'All System Emoji', 'icon_custom_emoji_id': '5352552689983067014', 'callback_data': 'all_system_emoji', 'style': _rs()}], [{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'system_settings', 'style': _rs()}]]}

def emoji_upload_keyboard():
    _reset_btn_counter()
    return {'inline_keyboard': [[{'text': 'Upload Flags (TXT)', 'icon_custom_emoji_id': '5353001161878182134', 'callback_data': 'up_flags_txt', 'style': _rs()}], [{'text': 'Upload Services (TXT)', 'icon_custom_emoji_id': '5353001161878182134', 'callback_data': 'up_apps_txt', 'style': _rs()}], [{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_emojis', 'style': _rs()}]]}

def emoji_delete_keyboard():
    _reset_btn_counter()
    return {'inline_keyboard': [[{'text': 'Delete All Flags', 'icon_custom_emoji_id': '5422557736330106570', 'callback_data': 'del_all_flags', 'style': _rs()}], [{'text': 'Delete All Services', 'icon_custom_emoji_id': '5422557736330106570', 'callback_data': 'del_all_apps', 'style': _rs()}], [{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_emojis', 'style': _rs()}]]}

def emoji_download_keyboard():
    _reset_btn_counter()
    return {'inline_keyboard': [[{'text': 'Download Flags', 'icon_custom_emoji_id': '5257969839313526622', 'callback_data': 'dl_flags_txt', 'style': _rs()}], [{'text': 'Download Services', 'icon_custom_emoji_id': '5257969839313526622', 'callback_data': 'dl_apps_txt', 'style': _rs()}], [{'text': 'Download System Emoji', 'icon_custom_emoji_id': '5257969839313526622', 'callback_data': 'dl_system_emoji', 'style': _rs()}], [{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_emojis', 'style': _rs()}]]}

def generate_emoji_txt(mode):
    lines = []
    if mode == 'flags':
        for code, info in bot_settings.get('premium_flags', {}).items():
            char = info.get('char', '')
            iso = info.get('iso', '')
            name = info.get('name', '')
            eid = info.get('id', '')
            if not (char and eid):
                continue
            json_part = json.dumps({'emoji': char, 'id': eid}, ensure_ascii=False)
            lines.append(f'({code}) ({iso}) {name} {char} {json_part}')
    elif mode == 'apps':
        for app_key, info in bot_settings.get('premium_apps', {}).items():
            char = info.get('char', '')
            eid = info.get('id', '')
            name = info.get('name', app_key)
            if not (char and eid):
                continue
            json_part = json.dumps({'emoji': char, 'id': eid}, ensure_ascii=False)
            lines.append(f'{name} {char} {json_part}')
    return '\n'.join(lines)

def fj_settings_keyboard():
    _reset_btn_counter()
    status_text = 'ON' if bot_settings['fj_on'] else 'OFF'
    status_icon = '5352694861990501856' if bot_settings['fj_on'] else '5318840353510408444'
    kb = [[{'text': f'STATUS: {status_text}', 'icon_custom_emoji_id': status_icon, 'callback_data': 'toggle_fj', 'style': _rs()}]]
    for idx, entry in enumerate(bot_settings['fj_channels']):
        info = _get_fj_info(entry)
        ch_type = info.get('type', 'channel')
        title = info.get('title', str(info.get('chat_id', '')))
        is_priv = info.get('is_private', False)
        type_tag = 'Channel' if ch_type == 'channel' else 'Group'
        priv_tag = 'Private' if is_priv else 'Public'
        btn_label = f'{title} [{type_tag} | {priv_tag}]'
        kb.append([{'text': btn_label, 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'del_fj_{idx}', 'style': _rs()}])
    kb.append([{'text': 'Add Channel / Group', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': 'add_fj', 'style': _rs()}])
    kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'system_settings', 'style': _rs()}])
    return {'inline_keyboard': kb}

def admin_settings_keyboard():
    _reset_btn_counter()
    kb = []
    for idx, adm in enumerate(bot_settings['admins']):
        text_btn = f'Owner: {adm}' if adm == OWNER_ID else f'Delete: {adm}'
        icon_id = '5353032893096567467' if adm == OWNER_ID else '5420130255174145507'
        cb_data = 'ignore' if adm == OWNER_ID else f'del_adm_{adm}'
        kb.append([{'text': text_btn, 'icon_custom_emoji_id': icon_id, 'callback_data': cb_data, 'style': _rs()}])
    kb.append([{'text': 'Add Admin', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': 'add_adm', 'style': _rs()}])
    kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'system_settings', 'style': _rs()}])
    return {'inline_keyboard': kb}

def otp_groups_list_keyboard():
    _reset_btn_counter()
    kb = [[{'text': 'Edit OTP Button Link', 'icon_custom_emoji_id': '5420517437885943844', 'callback_data': 'edit_otp_link', 'style': _rs()}]]
    for idx, fg in enumerate(bot_settings['fw_groups']):
        kb.append([{'text': f"Group: {fg['chat_id']}", 'icon_custom_emoji_id': '5193063022226086560', 'callback_data': f'manage_fw_{idx}', 'style': _rs()}])
    kb.append([{'text': 'Add Forward Group', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': 'add_fw', 'style': _rs()}])
    kb.append([{'text': 'Topic Settings', 'icon_custom_emoji_id': '5353032893096567467', 'callback_data': 'topic_settings', 'style': _rs()}])
    kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'system_settings', 'style': _rs()}])
    return {'inline_keyboard': kb}


def topic_settings_keyboard():
    _reset_btn_counter()
    return {'inline_keyboard': [
        [{'text': 'Add Topic', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': 'add_topic', 'style': _rs()}],
        [{'text': 'Topic List', 'icon_custom_emoji_id': '6267008582294705964', 'callback_data': 'topic_list', 'style': _rs()}],
        [{'text': 'Delete Topic', 'icon_custom_emoji_id': '5422557736330106570', 'callback_data': 'delete_topic_menu', 'style': _rs()}],
        [{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_otp_groups', 'style': _rs()}]
    ]}

def _show_topic_settings(chat_id, msg_id):
    edit_message(chat_id, msg_id,
        render_body_text('👩‍💻 <b>TOPIC SETTINGS</b>\n\nManage Topic Auto-Forwarding below:'),
        reply_markup=topic_settings_keyboard())

def _topic_logo_emoji_id(topic):
    """Return the saved topic logo when available, otherwise match the topic to Premium Apps."""
    saved_id = str(topic.get('emoji_id', '') or '').strip()
    if saved_id.isdigit():
        return saved_id
    apps = bot_settings.get('premium_apps', {})
    candidates = [str(topic.get('name', '')).strip(), str(topic.get('keyword', '')).strip()]
    for candidate in candidates:
        key = candidate.upper()
        if not key:
            continue
        info = apps.get(key)
        if isinstance(info, dict) and str(info.get('id', '')).isdigit():
            return str(info['id'])
        for app_key, app_info in apps.items():
            if key == str(app_key).upper() or key in str(app_key).upper() or str(app_key).upper() in key:
                if isinstance(app_info, dict) and str(app_info.get('id', '')).isdigit():
                    return str(app_info['id'])
    # Default premium topic logo when no matching service logo is configured.
    return '5353032893096567467'


def _show_topic_list(chat_id, msg_id, delete_mode=False):
    _reset_btn_counter()
    topics = bot_settings.get('topics', [])
    if not topics:
        kb = {'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176',
                                     'callback_data': 'topic_settings', 'style': _rs()}]]}
        edit_message(chat_id, msg_id, render_body_text('📋 <b>TOPIC LIST</b>\n\nNo topics saved yet.'), reply_markup=kb)
        return

    kb = []
    for idx, topic in enumerate(topics):
        topic_name = str(topic.get('name', 'Topic')).strip() or 'Topic'
        keyword = str(topic.get('keyword', '')).strip()
        if delete_mode:
            kb.append([{'text': f'Delete: {topic_name}', 'icon_custom_emoji_id': '5422557736330106570',
                        'callback_data': f'del_topic_{idx}', 'style': _rs()}])
        else:
            # Each saved topic is shown as its own button with that topic's logo.
            kb.append([{'text': f'{topic_name} | {keyword}', 'icon_custom_emoji_id': _topic_logo_emoji_id(topic),
                        'callback_data': 'ignore', 'style': _rs()}])

    kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176',
                'callback_data': 'topic_settings', 'style': _rs()}])

    title = '🗑️ <b>DELETE TOPIC</b>' if delete_mode else '📋 <b>TOPIC LIST</b>'
    details = []
    for i, topic in enumerate(topics, 1):
        details.append(
            f"{i}. <b>{html.escape(str(topic.get('name', 'Topic')))}</b>\n"
            f"   Keyword: <code>{html.escape(str(topic.get('keyword', '')))}</code>\n"
            f"   Topic ID: <code>{topic.get('topic_id', '')}</code>"
        )
    edit_message(chat_id, msg_id, render_body_text(title + '\n\n' + '\n\n'.join(details)), reply_markup={'inline_keyboard': kb})

def _forward_otp_to_matching_topics(group_msg, otp_code, msg_text):
    """Post matching OTP messages into configured Telegram forum topics."""
    topics = bot_settings.get('topics', [])
    if not topics:
        return
    message_text = str(msg_text or '').lower()
    matched = [t for t in topics if str(t.get('keyword', '')).strip() and str(t.get('keyword', '')).strip().lower() in message_text]
    if not matched:
        return
    for fw in bot_settings.get('fw_groups', []):
        for topic in matched:
            try:
                _reset_btn_counter()
                kb = [[{'text': f'{otp_code}', 'icon_custom_emoji_id': _OTP_COPY_EMOJI_ID,
                       'copy_text': {'text': str(otp_code)}, 'style': _rs()}]]
                fw_btns = []
                for btn in fw.get('buttons', []):
                    if str(btn.get('text', '')).strip().lower() != 'full message':
                        fw_btns.append(_make_fw_btn(btn, kb))
                for i in range(0, len(fw_btns), 2):
                    kb.append(fw_btns[i:i + 2])
                payload = {'chat_id': fw['chat_id'], 'text': _apply_text_overrides(group_msg),
                           'parse_mode': 'HTML', 'disable_web_page_preview': True,
                           'message_thread_id': int(topic['topic_id']),
                           'reply_markup': _force_navigation_button_colors(_apply_emoji_overrides({'inline_keyboard': kb}))}
                resp = api_call('sendMessage', payload)
                if resp and resp.get('ok'):
                    logger.debug(f"OTP topic forwarded to {fw.get('chat_id')} thread {topic.get('topic_id')}")
                else:
                    logger.warning(f"Topic forward failed ({fw.get('chat_id')} / {topic.get('topic_id')}): {resp}")
            except Exception as e:
                logger.warning(f"Topic delivery error ({fw.get('chat_id')} / {topic.get('topic_id')}): {e}")

def auto_mode_keyboard():
    _reset_btn_counter()
    nexa_on  = bot_settings.get("nexa_on", False)
    voltx_on = bot_settings.get("voltx_on", False)
    stex_on  = bot_settings.get("stex_on", False)
    smsbower_on = bot_settings.get("smsbower_on", False)
    # ON  emoji: green indicator  | OFF emoji: red indicator
    ON_EMOJI  = "6237529876690113625"
    OFF_EMOJI = "6267000941547885720"
    return {"inline_keyboard": [
        [{"text": "Nexa Panel Control",  "icon_custom_emoji_id": "6282760761399841824", "callback_data": "nexa_control",  "style": _rs()},
         {"text": "Nexa ON"  if nexa_on  else "Nexa OFF",  "icon_custom_emoji_id": ON_EMOJI if nexa_on  else OFF_EMOJI, "callback_data": "toggle_nexa",  "style": _rs()}],
        [{"text": "VoltX Panel Control", "icon_custom_emoji_id": "6282760761399841824", "callback_data": "voltx_control", "style": _rs()},
         {"text": "VoltX ON" if voltx_on else "VoltX OFF", "icon_custom_emoji_id": ON_EMOJI if voltx_on else OFF_EMOJI, "callback_data": "toggle_voltx", "style": _rs()}],
    [{"text": "Stex Panel Control", "icon_custom_emoji_id": "6282760761399841824", "callback_data": "stex_control", "style": _rs()},
     {"text": "Stex ON"  if stex_on  else "Stex OFF",  "icon_custom_emoji_id": ON_EMOJI if stex_on  else OFF_EMOJI, "callback_data": "toggle_stex",  "style": _rs()}],
    [{"text": "SMSBower Control", "icon_custom_emoji_id": "6282760761399841824", "callback_data": "smsbower_control", "style": _rs()},
     {"text": "SMSBower ON" if smsbower_on else "SMSBower OFF", "icon_custom_emoji_id": ON_EMOJI if smsbower_on else OFF_EMOJI, "callback_data": "toggle_smsbower", "style": _rs()}],
    [{"text": "Back", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "system_settings", "style": _rs()}]
]}

def _panel_control_keyboard(panel_name):
    """Shared API panel control keyboard for Nexa, VoltX, Stex.
    panel_name: display name e.g. 'Nexa', 'VoltX', 'Stex' — lowercase used for callback IDs."""
    p = panel_name.lower()
    _reset_btn_counter()
    return {"inline_keyboard": [
        [{"text": f"Add {panel_name} Key", "icon_custom_emoji_id": "5420323438508155202", "callback_data": f"add_{p}_key", "style": _rs()},
         {"text": "View/Del Keys", "icon_custom_emoji_id": "5422557736330106570", "callback_data": f"view_{p}_keys", "style": _rs()}],
        [{"text": f"Manage {panel_name} Services", "icon_custom_emoji_id": "5192739271886282680", "callback_data": f"manage_{p}_srv", "style": _rs()}],
        [{"text": "Search Country", "icon_custom_emoji_id": "5336972142066047577", "callback_data": f"{p}_search_country", "style": _rs()}],
        [{"text": "Back", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "auto_mode", "style": _rs()}]
    ]}

def specific_fw_group_keyboard(idx):
    _reset_btn_counter()
    if idx < 0 or idx >= len(bot_settings.get('fw_groups', [])):
        return {'inline_keyboard': [[{'text': 'Group Not Found', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': 'manage_otp_groups', 'style': 'danger'}]]}
    group = bot_settings['fw_groups'][idx]
    kb = []
    for b_idx, btn in enumerate(group.get('buttons', [])):
        kb.append([{'text': f"Del: {btn['text']}", 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'del_fwbtn_{idx}_{b_idx}', 'style': _rs()}])
    kb.append([{'text': 'Add Inline Button', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': f'add_fwbtn_{idx}', 'style': _rs()}])
    kb.append([{'text': 'Delete Entire Group', 'icon_custom_emoji_id': '5422557736330106570', 'callback_data': f'del_fw_{idx}', 'style': _rs()}])
    kb.append([{'text': 'Back to Groups', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_otp_groups', 'style': _rs()}])
    return {'inline_keyboard': kb}

def abhi_control_keyboard():
    _reset_btn_counter()
    w_status = 'ON' if bot_settings['withdraw_on'] else 'OFF'
    sup_status = 'ON' if bot_settings.get('support_link') else 'OFF'
    grp_status = 'ON' if bot_settings.get('w_group') else 'OFF'
    return {'inline_keyboard': [[{'text': f'WITHDRAW: {w_status}', 'icon_custom_emoji_id': '5348469219761626211', 'callback_data': 'abhi_toggle_w', 'style': _rs()}], [{'text': f"MIN WITHDRAW: {bot_settings['min_withdraw']}", 'icon_custom_emoji_id': '5352877703043258544', 'callback_data': 'abhi_min_w', 'style': _rs()}, {'text': f"OTP REWARD: {_format_rate(bot_settings.get('otp_reward', 0.0))}৳", 'icon_custom_emoji_id': '5190576863226933563', 'callback_data': 'abhi_otp_r', 'style': _rs()}], [{'text': f"REFER REWARD: {bot_settings['refer_reward']}", 'icon_custom_emoji_id': '5420396762189831222', 'callback_data': 'abhi_ref_r', 'style': _rs()}, {'text': f"COOLDOWN: {bot_settings['cooldown']}s", 'icon_custom_emoji_id': '5337172996211648018', 'callback_data': 'abhi_cool', 'style': _rs()}], [{'text': f"NUM/REQ: {bot_settings['num_req']}", 'icon_custom_emoji_id': '5337132498965010628', 'callback_data': 'abhi_num_req', 'style': _rs()}, {'text': f"NUM/SHARE: {bot_settings['num_share']}", 'icon_custom_emoji_id': '5352862640592949843', 'callback_data': 'abhi_num_share', 'style': _rs()}], [{'text': f'SUPPORT LINK: {sup_status}', 'icon_custom_emoji_id': '5420145051336485498', 'callback_data': 'abhi_sup_link', 'style': _rs()}, {'text': 'W. METHODS', 'icon_custom_emoji_id': '5190899075968441286', 'callback_data': 'manage_w_methods', 'style': _rs()}], [{'text': f'W. GROUP: {grp_status}', 'icon_custom_emoji_id': '5420517437885943844', 'callback_data': 'abhi_w_group', 'style': _rs()}, {'text': 'BACK', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'system_settings', 'style': _rs()}]]}

def w_methods_keyboard():
    _reset_btn_counter()
    kb = []
    for idx, m in enumerate(bot_settings['w_methods']):
        kb.append([{'text': f'Delete: {m}', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'del_wm_{idx}', 'style': _rs()}])
    kb.append([{'text': 'Add Method', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': 'add_wm', 'style': _rs()}])
    kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'abhi_control', 'style': _rs()}])
    return {'inline_keyboard': kb}

def typed_panels_list_keyboard(p_type):
    _reset_btn_counter()
    kb = []
    for idx, p in enumerate(bot_settings['panels']):
        if p.get('type', 'API Panel') != p_type:
            continue
        action_text = f"Turn OFF {p['name']}" if p['status'] == 'ON' else f"Turn ON {p['name']}"
        action_icon = '5318840353510408444' if p['status'] == 'ON' else '5192812028632274956'
        icon_id = '5420155432272438703'
        kb.append([{'text': action_text, 'icon_custom_emoji_id': action_icon, 'callback_data': f'tog_pnl_{idx}', 'style': _rs()}, {'text': f"{p['name']}", 'icon_custom_emoji_id': icon_id, 'callback_data': f'conf_pnl_{idx}', 'style': _rs()}])
    add_cb = 'add_api_panel' if p_type == 'API Panel' else 'add_cpt_panel'
    kb.append([{'text': 'Add New Provider', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': add_cb, 'style': _rs()}])
    kb.append([{'text': 'Delete Provider', 'icon_custom_emoji_id': '5336944168944047463', 'callback_data': f"list_del_{('api' if p_type == 'API Panel' else 'cpt')}", 'style': _rs()}])
    kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_panels', 'style': _rs()}])
    return {'inline_keyboard': kb}

def panel_config_keyboard(idx):
    _reset_btn_counter()
    if idx < 0 or idx >= len(bot_settings.get('panels', [])):
        return {'inline_keyboard': [[{'text': 'Panel Not Found', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': 'manage_panels', 'style': 'danger'}]]}
    p = bot_settings['panels'][idx]
    kb = []
    action_text = 'Turn OFF' if p['status'] == 'ON' else 'Turn ON'
    action_icon = '5318840353510408444' if p['status'] == 'ON' else '5192812028632274956'
    kb.append([{'text': action_text, 'icon_custom_emoji_id': action_icon, 'callback_data': f'tog_pnl_{idx}', 'style': _rs()}])
    if p['type'] != 'Auto Captcha Panel':
        rec_count_text = 'All (Unlimited)' if p.get('records', 0) == 0 else str(p.get('records'))
        kb.append([{'text': 'Set API URL', 'icon_custom_emoji_id': '5420517437885943844', 'callback_data': f'set_p_api_{idx}', 'style': _rs()}])
        kb.append([{'text': 'Set Token', 'icon_custom_emoji_id': '5353022963132174959', 'callback_data': f'set_p_tok_{idx}', 'style': _rs()}])
        token_hdr = p.get('token_header', '')
        hdr_text = f'Token Header: {token_hdr}' if token_hdr else 'Set Token Header (Optional)'
        kb.append([{'text': hdr_text, 'icon_custom_emoji_id': '5353022963132174959', 'callback_data': f'set_p_tokh_{idx}', 'style': _rs()}])
        kb.append([{'text': 'Full API (URL+Token)', 'icon_custom_emoji_id': '5420517437885943844', 'callback_data': f'set_p_fapi_{idx}', 'style': _rs()}])
        kb.append([{'text': f'Set Records Count: {rec_count_text}', 'icon_custom_emoji_id': '5192739271886282680', 'callback_data': f'set_p_rec_{idx}', 'style': _rs()}])
    kb.append([{'text': 'Test Connection', 'icon_custom_emoji_id': '5276032951342088188', 'callback_data': f'test_p_conn_{idx}', 'style': _rs()}])
    back_data = 'manage_api_panels' if p.get('type', 'API Panel') == 'API Panel' else 'manage_cpt_panels'
    kb.append([{'text': 'Back to Providers', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': back_data, 'style': _rs()}])
    return {'inline_keyboard': kb}

def build_traffic_ui():
    """LIVE TRAFFIC — 5-minute live activity + 24-hour Top Countries."""
    current_time = time.time()
    live_cutoff = current_time - 300
    day_cutoff = current_time - TRAFFIC_RETENTION_SECONDS

    with _traffic_lock:
        recent_traffic[:] = [
            t for t in recent_traffic
            if current_time - t.get("time", 0) <= TRAFFIC_RETENTION_SECONDS
        ]
        day_window = [t for t in recent_traffic if t.get("time", 0) >= day_cutoff]
        live_window = [t for t in day_window if t.get("time", 0) >= live_cutoff]

    def country_name(iso):
        iso = str(iso or "XX").upper()
        for _, fdata in bot_settings.get("premium_flags", {}).items():
            if str(fdata.get("iso", "")).upper() == iso:
                return str(fdata.get("name") or iso)
        try:
            obj = pycountry.countries.get(alpha_2=iso)
            if obj:
                return obj.name
        except Exception:
            pass
        return iso

    def country_flag(iso):
        try:
            return get_flag_info_html(iso)
        except Exception:
            return "🌍"

    def group_stats(records):
        groups = {}
        for t in records:
            iso = str(t.get("iso") or "XX").upper()
            service = str(t.get("service") or "").strip()
            key = (iso, service)
            groups[key] = groups.get(key, 0) + 1
        return groups

    live_groups = group_stats(live_window)
    day_groups = group_stats(day_window)
    live_total = sum(live_groups.values())
    day_total = sum(day_groups.values())

    day_countries = Counter()
    for (iso, _service), count in day_groups.items():
        day_countries[iso] += count
    ranked_countries = day_countries.most_common()

    ranked_live = sorted(
        live_groups.items(),
        key=lambda item: (-item[1], item[0][0], item[0][1])
    )

    _traffic_graph = '<tg-emoji emoji-id="5353032893096567467">📊</tg-emoji>'
    _traffic_calendar = '<tg-emoji emoji-id="5352585194295564660">📅</tg-emoji>'
    _traffic_eye = '<tg-emoji emoji-id="5190645917711114179">👁</tg-emoji>'
    _traffic_top = '<tg-emoji emoji-id="5276032951342088188">🏆</tg-emoji>'
    _traffic_world = '<tg-emoji emoji-id="5780471598922337683">🌍</tg-emoji>'

    txt = (
        f"<b>{_traffic_graph} Live Traffic</b>\n\n"
        f"{_traffic_calendar} <b>Live Window:</b> Last 5 minutes\n"
        f"{_traffic_eye} <b>Results Sent:</b> {live_total}\n"
    )

    if ranked_live:
        (iso, service), count = ranked_live[0]
        top_label = country_name(iso) + (f" {service}" if service else "")
        txt += f"{_traffic_top} <b>Top Live:</b> {country_flag(iso)} {top_label} — {count}\n"
    else:
        txt += f"{_traffic_top} <b>Top Live:</b> —\n"

    # Top Countries always uses the rolling 24-hour history.
    txt += (
        f"\n{_traffic_world} <b>Top Countries — Last 24 Hours</b>\n"
        f"{_traffic_calendar} <b>Total Results:</b> {day_total}\n"
    )

    if ranked_countries:
        for idx, (iso, count) in enumerate(ranked_countries[:15], 1):
            pct = (count / day_total * 100.0) if day_total else 0.0
            txt += f"{idx}. {country_flag(iso)} <b>{country_name(iso)}</b> — {count} ({pct:.1f}%)\n"
    else:
        txt += "<i>No OTP results received in the last 24 hours.</i>\n"

    txt = render_body_text(txt)
    _reset_btn_counter()
    kb = [
        [{"text": "Refresh", "icon_custom_emoji_id": "5420155432272438703", "callback_data": "refresh_traffic", "style": "success"}],
        [{"text": "Close", "icon_custom_emoji_id": "5420130255174145507", "callback_data": "close_msg", "style": "danger"}]
    ]
    return txt, {"inline_keyboard": kb}


def _save_processed_otps():
    global _seen_otps_save_lock
    # Defensive initialization: prevents NameError if this function is loaded
    # from a partial/older runtime copy.
    try:
        _seen_otps_save_lock
    except NameError:
        _seen_otps_save_lock = threading.Lock()
    with _seen_otps_save_lock:
        try:
            with _data_lock:
                items = dict(processed_otps)
            cutoff = time.time() - 90000
            items = {k: v for k, v in items.items() if v > cutoff}
            tmp_path = SEEN_OTPS_FILE + '.tmp'
            with open(tmp_path, 'w') as f:
                json.dump(items, f)
            os.replace(tmp_path, SEEN_OTPS_FILE)
        except Exception as e:
            logger.warning(f'OTP save error: {e}')

def _load_processed_otps():
    global processed_otps
    try:
        with open(SEEN_OTPS_FILE, 'r') as f:
            data = json.load(f)
        if isinstance(data, dict):
            cutoff = time.time() - 90000
            new_dict = {k: v for k, v in data.items() if v > cutoff}
        else:
            new_dict = {uid: time.time() - 3600 for uid in data}
        with _data_lock:
            processed_otps = new_dict
        logger.info(f'Loaded {len(new_dict)} previously seen OTP IDs — old OTPs will be skipped.')
    except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
        with _data_lock:
            processed_otps = {}
        if isinstance(e, FileNotFoundError):
            pass
        elif isinstance(e, json.JSONDecodeError):
            logger.warning(f'seen_otps.json parse error: {e} — starting fresh')
        else:
            logger.warning(f'seen_otps.json I/O error: {e} — starting fresh')

def _add_to_processed(unique_id):
    with _data_lock:
        processed_otps[unique_id] = time.time()
        if len(processed_otps) > 20000:
            cutoff = time.time() - 90000
            old_keys = [k for k, v in processed_otps.items() if v < cutoff]
            for k in old_keys:
                del processed_otps[k]
            if len(processed_otps) > 20000:
                sorted_keys = sorted(processed_otps, key=lambda k: processed_otps[k])
                for k in sorted_keys[:10000]:
                    del processed_otps[k]

def _is_processed(unique_id, window=90000):
    """True if unique_id last `window` seconds mein process ho chuka hai (default 25 ghante).
    25h window isliye: panels 24h tak OTP history rakhte hain, toh 25h = 1 ghante ka
    extra safe margin — purane OTPs kabhi dobara deliver nahi honge."""
    with _data_lock:
        ts = processed_otps.get(unique_id)
        if ts is None:
            return False
        return time.time() - ts < window

# Cross-source OTP deduplication. A panel/API can return the same SMS again with a
# different internal ID (or without an ID), and multiple listeners can see the same OTP.
# This canonical key is intentionally independent of provider/panel prefix.
GLOBAL_OTP_DEDUP_WINDOW = 25 * 60 * 60

def _canonical_otp_key(num, otp, msg_text='', app_name=''):
    # IMPORTANT: panel history APIs often return the same SMS later with a new
    # row/message/internal ID and sometimes slightly different message markup.
    # Therefore the duplicate identity MUST NOT depend on panel name, provider,
    # internal ID, service text, or the full SMS body.  The phone number + OTP
    # pair is the stable identity we need for the 25-hour delivery window.
    clean_num = re.sub(r'\D', '', str(num or ''))
    clean_otp = re.sub(r'\s+', '', str(otp or '')).strip().upper()
    return f'GLOBAL_OTP_{clean_num}_{clean_otp}'

def _claim_global_otp(num, otp, msg_text='', app_name=''):
    """Atomically claim an OTP for delivery across ALL providers/listeners.
    Returns False when this exact OTP was already delivered during the 25h window."""
    key = _canonical_otp_key(num, otp, msg_text, app_name)
    with _data_lock:
        ts = processed_otps.get(key)
        now = time.time()
        if ts is not None and now - ts < GLOBAL_OTP_DEDUP_WINDOW:
            return False
        processed_otps[key] = now
    return True
OTP_MAX_AGE_SECONDS = 90000
_DT_FORMATS = ('%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%d-%m-%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%f')

def _parse_item_datetime_epoch(dt_str):
    """item_id mein aya datetime string ko epoch seconds mein convert karta hai.
    Parse nahi ho paya to None return karta hai (age-check us case mein skip ho jata hai —
    hum sirf CONFIRMED purane OTPs ko block karte hain, kabhi false-positive nahi)."""
    if not dt_str:
        return None
    s = str(dt_str).strip()
    for fmt in _DT_FORMATS:
        try:
            return datetime.strptime(s, fmt).timestamp()
        except (ValueError, TypeError):
            continue
    return None

def _is_stale_otp(item_id, max_age=OTP_MAX_AGE_SECONDS):
    """True agar item_id ka apna timestamp bataye ki OTP already max_age se purana hai.
    Panel ke record ki timestamp future mein bhi ho sakti hai (clock drift) — us case
    mein bhi stale nahi maanenge, sirf ATEET (past) mein bahut purana ho to hi block karo."""
    epoch = _parse_item_datetime_epoch(item_id)
    if epoch is None:
        return False
    age = time.time() - epoch
    return age > max_age

def _process_pending_referral(chat_id):
    u_data = _get_local_user(chat_id)
    if u_data.get('referred_by') and (not u_data.get('ref_paid')):
        inviter = u_data['referred_by']
        _update_local_user(chat_id, {'ref_paid': True})
        reward = bot_settings.get('refer_reward', 0.2)
        update_balance(inviter, reward)
        _increment_local_user(inviter, 'total_refers', 1)
        ref_msg = f"{PEM['gift']} <b>New Referral !</b>\n------------------\n🔥 <b>You Received {reward}৳</b>\n------------------\n{PEM['user']} <b>From User ID:</b> <code>{chat_id}</code>"
        send_message(inviter, render_body_text(ref_msg))

def _get_all_numbers_set():
    all_nums = set()
    for b in number_batches.values():
        for n in b['numbers']:
            all_nums.add(n['num'].replace('+', '').strip())
    for n in used_numbers_list:
        all_nums.add(n.replace('+', '').strip())
    return all_nums

def _record_and_deliver_otp(owner_id, num_str, app_name, msg_text, otp, clean_num_key, caller_tag='', _global_claimed=False):
    """Shared helper: record traffic + save DB + deliver OTP to user + mark otp_received.
    Used by poll_otp_with_status, _poll_mauthapi_otp_single, _poll_mauthapi_otps, global_sms_listener."""
    if not _global_claimed and not _claim_global_otp(clean_num_key or num_str, otp, msg_text, app_name):
        logger.info(f'Skipping duplicate OTP in shared delivery helper: {clean_num_key or num_str} / {otp}')
        return False
    char, iso = get_flag_and_code(num_str)
    app_full_name, prem_app_html = get_service_info_html(app_name, msg_text)
    current_time = time.time()
    _prune_traffic(current_time)
    with _traffic_lock:
        recent_traffic.append({'service': app_full_name, 'iso': iso, 'flag': char, 'number': num_str, 'time': current_time})
    save_local_db()
    _deliver_otp_to_user(owner_id, num_str, app_full_name, prem_app_html, iso, otp, msg_text)
    try:
        clean_key = str(clean_num_key).replace('+', '').replace(' ', '').replace('-', '').strip()
        with _data_lock:
            otp_received_numbers.add(clean_key)
    except Exception as e:
        logger.warning(f'otp_received_numbers error [{caller_tag}]: {e}')
    return True

def _country_full_name_from_iso(iso):
    """Return the full English country name from an ISO-2 code.
    Uses pycountry when available, with an embedded ISO-3166 fallback so
    deployments without the pycountry package never display the short code.
    """
    code = str(iso or '').strip().upper()
    if not code:
        return 'Unknown Country'
    # Use the short/common country name in user-facing OTP messages.
    _COUNTRY_NAME_OVERRIDES = {
        'TZ': 'Tanzania',
        'CD': 'Democratic Republic of the Congo',
        'CG': 'Republic of the Congo',
        'BO': 'Bolivia',
        'IR': 'Iran',
        'KR': 'South Korea',
        'KP': 'North Korea',
        'LA': 'Laos',
        'MD': 'Moldova',
        'RU': 'Russia',
        'SY': 'Syria',
        'VE': 'Venezuela',
        'VN': 'Vietnam',
        'TW': 'Taiwan',
    }
    if code in _COUNTRY_NAME_OVERRIDES:
        return _COUNTRY_NAME_OVERRIDES[code]
    try:
        import pycountry
        c = pycountry.countries.get(alpha_2=code)
        if c and getattr(c, 'name', None):
            return c.name
    except Exception:
        pass
    _ISO_COUNTRY_NAMES = {'AD': 'Andorra', 'AE': 'United Arab Emirates', 'AF': 'Afghanistan', 'AG': 'Antigua and Barbuda', 'AI': 'Anguilla', 'AL': 'Albania', 'AM': 'Armenia', 'AO': 'Angola', 'AQ': 'Antarctica', 'AR': 'Argentina', 'AS': 'American Samoa', 'AT': 'Austria', 'AU': 'Australia', 'AW': 'Aruba', 'AX': 'Åland Islands', 'AZ': 'Azerbaijan', 'BA': 'Bosnia and Herzegovina', 'BB': 'Barbados', 'BD': 'Bangladesh', 'BE': 'Belgium', 'BF': 'Burkina Faso', 'BG': 'Bulgaria', 'BH': 'Bahrain', 'BI': 'Burundi', 'BJ': 'Benin', 'BL': 'Saint Barthélemy', 'BM': 'Bermuda', 'BN': 'Brunei Darussalam', 'BO': 'Bolivia, Plurinational State of', 'BQ': 'Bonaire, Sint Eustatius and Saba', 'BR': 'Brazil', 'BS': 'Bahamas', 'BT': 'Bhutan', 'BV': 'Bouvet Island', 'BW': 'Botswana', 'BY': 'Belarus', 'BZ': 'Belize', 'CA': 'Canada', 'CC': 'Cocos (Keeling) Islands', 'CD': 'Congo, The Democratic Republic of the', 'CF': 'Central African Republic', 'CG': 'Congo', 'CH': 'Switzerland', 'CI': "Côte d'Ivoire", 'CK': 'Cook Islands', 'CL': 'Chile', 'CM': 'Cameroon', 'CN': 'China', 'CO': 'Colombia', 'CR': 'Costa Rica', 'CU': 'Cuba', 'CV': 'Cabo Verde', 'CW': 'Curaçao', 'CX': 'Christmas Island', 'CY': 'Cyprus', 'CZ': 'Czechia', 'DE': 'Germany', 'DJ': 'Djibouti', 'DK': 'Denmark', 'DM': 'Dominica', 'DO': 'Dominican Republic', 'DZ': 'Algeria', 'EC': 'Ecuador', 'EE': 'Estonia', 'EG': 'Egypt', 'EH': 'Western Sahara', 'ER': 'Eritrea', 'ES': 'Spain', 'ET': 'Ethiopia', 'FI': 'Finland', 'FJ': 'Fiji', 'FK': 'Falkland Islands (Malvinas)', 'FM': 'Micronesia, Federated States of', 'FO': 'Faroe Islands', 'FR': 'France', 'GA': 'Gabon', 'GB': 'United Kingdom', 'GD': 'Grenada', 'GE': 'Georgia', 'GF': 'French Guiana', 'GG': 'Guernsey', 'GH': 'Ghana', 'GI': 'Gibraltar', 'GL': 'Greenland', 'GM': 'Gambia', 'GN': 'Guinea', 'GP': 'Guadeloupe', 'GQ': 'Equatorial Guinea', 'GR': 'Greece', 'GS': 'South Georgia and the South Sandwich Islands', 'GT': 'Guatemala', 'GU': 'Guam', 'GW': 'Guinea-Bissau', 'GY': 'Guyana', 'HK': 'Hong Kong', 'HM': 'Heard Island and McDonald Islands', 'HN': 'Honduras', 'HR': 'Croatia', 'HT': 'Haiti', 'HU': 'Hungary', 'ID': 'Indonesia', 'IE': 'Ireland', 'IL': 'Israel', 'IM': 'Isle of Man', 'IN': 'India', 'IO': 'British Indian Ocean Territory', 'IQ': 'Iraq', 'IR': 'Iran, Islamic Republic of', 'IS': 'Iceland', 'IT': 'Italy', 'JE': 'Jersey', 'JM': 'Jamaica', 'JO': 'Jordan', 'JP': 'Japan', 'KE': 'Kenya', 'KG': 'Kyrgyzstan', 'KH': 'Cambodia', 'KI': 'Kiribati', 'KM': 'Comoros', 'KN': 'Saint Kitts and Nevis', 'KP': "Korea, Democratic People's Republic of", 'KR': 'Korea, Republic of', 'KW': 'Kuwait', 'KY': 'Cayman Islands', 'KZ': 'Kazakhstan', 'LA': "Lao People's Democratic Republic", 'LB': 'Lebanon', 'LC': 'Saint Lucia', 'LI': 'Liechtenstein', 'LK': 'Sri Lanka', 'LR': 'Liberia', 'LS': 'Lesotho', 'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia', 'LY': 'Libya', 'MA': 'Morocco', 'MC': 'Monaco', 'MD': 'Moldova, Republic of', 'ME': 'Montenegro', 'MF': 'Saint Martin (French part)', 'MG': 'Madagascar', 'MH': 'Marshall Islands', 'MK': 'North Macedonia', 'ML': 'Mali', 'MM': 'Myanmar', 'MN': 'Mongolia', 'MO': 'Macao', 'MP': 'Northern Mariana Islands', 'MQ': 'Martinique', 'MR': 'Mauritania', 'MS': 'Montserrat', 'MT': 'Malta', 'MU': 'Mauritius', 'MV': 'Maldives', 'MW': 'Malawi', 'MX': 'Mexico', 'MY': 'Malaysia', 'MZ': 'Mozambique', 'NA': 'Namibia', 'NC': 'New Caledonia', 'NE': 'Niger', 'NF': 'Norfolk Island', 'NG': 'Nigeria', 'NI': 'Nicaragua', 'NL': 'Netherlands', 'NO': 'Norway', 'NP': 'Nepal', 'NR': 'Nauru', 'NU': 'Niue', 'NZ': 'New Zealand', 'OM': 'Oman', 'PA': 'Panama', 'PE': 'Peru', 'PF': 'French Polynesia', 'PG': 'Papua New Guinea', 'PH': 'Philippines', 'PK': 'Pakistan', 'PL': 'Poland', 'PM': 'Saint Pierre and Miquelon', 'PN': 'Pitcairn', 'PR': 'Puerto Rico', 'PS': 'Palestine, State of', 'PT': 'Portugal', 'PW': 'Palau', 'PY': 'Paraguay', 'QA': 'Qatar', 'RE': 'Réunion', 'RO': 'Romania', 'RS': 'Serbia', 'RU': 'Russian Federation', 'RW': 'Rwanda', 'SA': 'Saudi Arabia', 'SB': 'Solomon Islands', 'SC': 'Seychelles', 'SD': 'Sudan', 'SE': 'Sweden', 'SG': 'Singapore', 'SH': 'Saint Helena, Ascension and Tristan da Cunha', 'SI': 'Slovenia', 'SJ': 'Svalbard and Jan Mayen', 'SK': 'Slovakia', 'SL': 'Sierra Leone', 'SM': 'San Marino', 'SN': 'Senegal', 'SO': 'Somalia', 'SR': 'Suriname', 'SS': 'South Sudan', 'ST': 'Sao Tome and Principe', 'SV': 'El Salvador', 'SX': 'Sint Maarten (Dutch part)', 'SY': 'Syrian Arab Republic', 'SZ': 'Eswatini', 'TC': 'Turks and Caicos Islands', 'TD': 'Chad', 'TF': 'French Southern Territories', 'TG': 'Togo', 'TH': 'Thailand', 'TJ': 'Tajikistan', 'TK': 'Tokelau', 'TL': 'Timor-Leste', 'TM': 'Turkmenistan', 'TN': 'Tunisia', 'TO': 'Tonga', 'TR': 'Türkiye', 'TT': 'Trinidad and Tobago', 'TV': 'Tuvalu', 'TW': 'Taiwan, Province of China', 'TZ': 'Tanzania, United Republic of', 'UA': 'Ukraine', 'UG': 'Uganda', 'UM': 'United States Minor Outlying Islands', 'US': 'United States', 'UY': 'Uruguay', 'UZ': 'Uzbekistan', 'VA': 'Holy See (Vatican City State)', 'VC': 'Saint Vincent and the Grenadines', 'VE': 'Venezuela, Bolivarian Republic of', 'VG': 'Virgin Islands, British', 'VI': 'Virgin Islands, U.S.', 'VN': 'Viet Nam', 'VU': 'Vanuatu', 'WF': 'Wallis and Futuna', 'WS': 'Samoa', 'YE': 'Yemen', 'YT': 'Mayotte', 'ZA': 'South Africa', 'ZM': 'Zambia', 'ZW': 'Zimbabwe'}
    return _ISO_COUNTRY_NAMES.get(code, 'Unknown Country')

def _deliver_otp_to_user(owner_id, num_str, app_full_name, prem_app_html, iso, otp_code, msg_text):
    _reset_btn_counter()
    display_num = f'+{num_str}' if not str(num_str).startswith('+') else str(num_str)
    lang = detect_language(msg_text)
    masked = mask_number(display_num, user_id=owner_id)
    _g_clean = str(display_num).replace('+', '').replace(' ', '')
    _g_masked = f'{_g_clean[:4]}{_MASK_EMOJI}{_g_clean[-4:]}{_END_NUMBER_EMOJI}' if len(_g_clean) >= 8 else mask_number(display_num)
    group_iso = str(iso or '').strip().upper()
    iso_text = f' #{group_iso}' if group_iso else ''
    lang_text = str(lang or '').strip()
    lang_line = f'\n💬 {html.escape(lang_text)}' if lang_text and lang_text.lower() not in ('unknown','none','n/a') else ''
    group_msg = _otp_box_message(f'{get_flag_info_html(display_num)}{iso_text} {prem_app_html} {_g_masked}', lang_line)
    for fw in bot_settings.get('fw_groups', []):
        try:
            _reset_btn_counter()
            kb = [[{'text': f'{otp_code}', 'icon_custom_emoji_id': _OTP_COPY_EMOJI_ID, 'copy_text': {'text': otp_code}, 'style': _rs()}]]
            _fw_btns = []
            for btn in fw.get('buttons', []):
                if str(btn.get('text', '')).strip().lower() == 'full message':
                    continue
                _fw_btns.append(_make_fw_btn(btn, kb))
            for _i in range(0, len(_fw_btns), 2):
                kb.append(_fw_btns[_i:_i + 2])
            res_fw = send_message(fw['chat_id'], group_msg, reply_markup={'inline_keyboard': kb})
            if res_fw and res_fw.get('ok'):
                logger.debug(f"OTP forwarded to group {fw.get('chat_id')}")
            else:
                logger.warning(f"FW Group send failed ({fw.get('chat_id')}): {res_fw}")
        except Exception as e:
            logger.warning(f"FW Group delivery error ({fw.get('chat_id')}): {e}")
    _forward_otp_to_matching_topics(group_msg, otp_code, msg_text)
    if not owner_id:
        return
    country_full_name = _country_full_name_from_iso(iso)
    clean_number = str(display_num).replace('+', '').replace(' ', '').strip()
    flag_html = get_flag_info_html(clean_number)
    _otp_rate = _get_session_rate(owner_id, clean_number)
    display_msg = render_body_text(f'<b>{flag_html} ({country_full_name.upper()}) 📱</b>\n➖➖➖➖➖➖➖➖➖➖\n📞 <b>NUMBER:</b> <code>{clean_number}</code>')
    _reset_btn_counter()
    inbox_kb = [[{'text': f'OTP {otp_code}', 'icon_custom_emoji_id': _OTP_COPY_EMOJI_ID, 'copy_text': {'text': str(otp_code)}, 'style': _rs()}]]
    reward = _get_effective_otp_reward(owner_id, clean_number)
    if reward > 0:
        update_balance(owner_id, reward)
        inbox_kb.append([{'text': f'Added {reward:g}৳', 'icon_custom_emoji_id': '5420396762189831222', 'callback_data': 'ignore', 'style': _rs()}])
        logger.debug(f'OTP reward {reward} credited to user {owner_id}')
    try:
        send_message(owner_id, display_msg, reply_markup={'inline_keyboard': inbox_kb}, protect_from_menu_cleanup=True)
        logger.debug(f'OTP delivered to user {owner_id}: {otp_code}')
    except Exception as e:
        logger.warning(f'User OTP delivery error ({owner_id}): {e}')
    _increment_local_user(owner_id, 'total_otps', 1)

def _alert_group_gone(call):
    answer_callback(call['id'], '❌ Group not found!', show_alert=True)
_PANEL_SC_CFG = {'nexa': {'key': 'nexa_search_countries', 'del_cb': 'del_sc_', 'add_cb': 'add_search_country', 'back_cb': 'nexa_control', 'label': 'Nexa'}, 'voltx': {'key': 'voltx_search_countries', 'del_cb': 'del_vxsc_', 'add_cb': 'add_vx_search_country', 'back_cb': 'voltx_control', 'label': 'VoltX'}, 'stex': {'key': 'stex_search_countries', 'del_cb': 'del_stxsc_', 'add_cb': 'add_stx_search_country', 'back_cb': 'stex_control', 'label': 'Stex'}}

def _show_panel_search_countries(panel, chat_id, msg_id):
    """Show allowed search countries UI for a panel (nexa/voltx/stex)."""
    cfg = _PANEL_SC_CFG[panel]
    _reset_btn_counter()
    kb = []
    for idx, c in enumerate(bot_settings.get(cfg['key'], [])):
        kb.append([{'text': f'Delete {c}', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f"{cfg['del_cb']}{idx}", 'style': _rs()}])
    kb.append([{'text': 'Add Country Code', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': cfg['add_cb'], 'style': _rs()}])
    kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': cfg['back_cb'], 'style': _rs()}])
    edit_message(chat_id, msg_id, render_body_text(f"🌍 <b>{cfg['label']} Allowed Search Countries:</b>\nOnly these country codes will be allowed in Search Number for {cfg['label']}."), reply_markup={'inline_keyboard': kb})

def _alert_panel_gone(call):
    answer_callback(call['id'], '❌ Panel not found! List may have changed.', show_alert=True)

def _err_panel_gone(chat_id):
    send_message(chat_id, render_body_text('❌ Panel not found! It may have been deleted.'))

def _set_panel_temp(chat_id, msg_id, idx):
    panels = bot_settings.get('panels', [])
    if idx < 0 or idx >= len(panels):
        _err_panel_gone(chat_id)
        return
    temp_data[chat_id] = {'msg_id': msg_id, 'p_idx': idx, 'p_name': panels[idx]['name']}

def _add_close_btn(kb):
    kb.append([{'text': 'Close', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': 'close_msg', 'style': _rs()}])

def _append_custom_btns(kb, c_msg):
    for b in c_msg.get('buttons', []):
        b_copy = b.copy()
        b_copy['style'] = _rs()
        kb.append([b_copy])

TRAFFIC_RETENTION_SECONDS = 24 * 60 * 60

def _prune_traffic(current_time):
    # Keep traffic records for a full 24 hours so LIVE TRAFFIC can show
    # both the current 5-minute activity and the complete 24-hour Top Countries.
    with _traffic_lock:
        recent_traffic[:] = [
            t for t in recent_traffic
            if current_time - t.get('time', 0) <= TRAFFIC_RETENTION_SECONDS
        ]

def _find_flag_emoji_id(c, flags_db, default='5780471598922337683'):
    if c in flags_db and 'id' in flags_db[c]:
        return flags_db[c]['id']
    c_upper = c.upper()
    for flag_data in flags_db.values():
        iso = flag_data.get('iso', '').upper()
        name = flag_data.get('name', '').upper()
        if c_upper == iso or c_upper == name or c_upper in name or (name in c_upper):
            if 'id' in flag_data:
                return flag_data['id']
    return default

def _save_panel_field(chat_id, msg, field, value):
    if not _td_has(chat_id, 'p_idx', 'msg_id'):
        _err_panel_gone(chat_id)
        user_states.pop(chat_id, None)
        temp_data.pop(chat_id, None)
        return
    idx = _td(chat_id, 'p_idx', -1)
    edit_msg_id = _td(chat_id, 'msg_id', msg['message_id'])
    if idx < 0 or idx >= len(bot_settings['panels']):
        _err_panel_gone(chat_id)
    else:
        bot_settings['panels'][idx][field] = value
        save_local_db()
        delete_message(chat_id, msg['message_id'])
        _show_panel_cfg(chat_id, edit_msg_id, idx)
    user_states.pop(chat_id, None)
    temp_data.pop(chat_id, None)

def _show_fj_panel(chat_id, msg_id):
    edit_message(chat_id, msg_id, render_body_text(f"{PEM['link']} <b>FORCE JOIN SYSTEM</b>\nManage channels/groups below:"), reply_markup=fj_settings_keyboard())

def _show_admin_panel(chat_id, msg_id):
    edit_message(chat_id, msg_id, render_body_text(f"{PEM['user']} <b>ADMIN MANAGEMENT</b>\nManage your bot admins below:"), reply_markup=admin_settings_keyboard())

def _show_otp_groups_panel(chat_id, msg_id):
    edit_message(chat_id, msg_id, render_body_text('🛡 <b>OTP GROUP MANAGEMENT</b>\nManage settings below:'), reply_markup=otp_groups_list_keyboard())

def _show_abhi_panel(chat_id, msg_id, extra=''):
    txt = '🕹 <b>BOT CONTROL PANEL</b>'
    if extra:
        txt += f'\n\n{extra}'
    edit_message(chat_id, msg_id, render_body_text(txt), reply_markup=abhi_control_keyboard())

def _show_w_methods(chat_id, msg_id):
    edit_message(chat_id, msg_id, render_body_text('💳 <b>WITHDRAWAL METHODS</b>\n\nManage your withdrawal methods below:'), reply_markup=w_methods_keyboard())

def _show_cpanel_prompt(chat_id, msg_id, step, title, instruction):
    """Render the current Auto Captcha setup step in the SAME admin message.
    The message is edited for every step instead of creating a new prompt bubble.
    """
    step_text = f'{step}️⃣ <b>{title}</b>'
    body = f'{step_text}\n➡️ {instruction}'
    edit_message(chat_id, msg_id, render_body_text(body), reply_markup=get_cancel_kb())

def _show_panel_cfg(chat_id, edit_msg_id, idx):
    """Refresh panel config display after a field update."""
    if idx < 0 or idx >= len(bot_settings['panels']):
        _err_panel_gone(chat_id)
        return
    p = bot_settings['panels'][idx]
    if p['type'] == 'Auto Captcha Panel':
        text = f"⚙️ <b>Configure {p['name']}</b>\n\n<b>Type:</b> {p['type']}\n<b>Status:</b> {('🟢 Monitoring' if p['status'] == 'ON' else '🔴 Stopped')}\n<b>Login Status:</b> {p.get('login_status', 'Unknown')}\n<b>Login URL:</b> <code>{p.get('login_url', 'None')}</code>\n<b>User:</b> <code>{p.get('username', 'None')}</code>"
    else:
        hdr_info = f"\n<b>Token Header:</b> <code>{p.get('token_header')}</code>" if p.get('token_header') else ''
        text = f"⚙️ <b>Configure {p['name']}</b>\n\n<b>Type:</b> {p['type']}\n<b>Status:</b> {('🟢 Monitoring' if p['status'] == 'ON' else '🔴 Stopped')}\n<b>API URL:</b> <code>{p.get('api_url', 'None')}</code>\n<b>Token:</b> <code>{p.get('token', 'None')}</code>{hdr_info}\n<b>Full API URL:</b> <code>{p.get('full_api_url', 'None')}</code>"
    edit_message(chat_id, edit_msg_id, render_body_text(text), reply_markup=panel_config_keyboard(idx))

def _err_invalid_serial(chat_id):
    send_message(chat_id, render_body_text('❌ Please enter a valid number serial!'), reply_markup=get_cancel_kb())

def _err_invalid_id(chat_id):
    send_message(chat_id, render_body_text('❌ Invalid ID!'), reply_markup=get_cancel_kb())

def _show_2fa_name_input(chat_id, msg_id):
    """Helper: 2FA naam input screen. Duplicate code remove."""
    txt = f'➖➖➖➖➖➖➖➖➖➖➖➖\n《 📛 <b>ENTER THE NAME OF THE CODE.</b> 》\n➖➖➖➖➖➖➖➖➖➖➖➖\n📝 What would you like to name this 2FA code?\n➖➖➖➖➖➖➖➖➖➖➖➖\n👇 Type The Name And Send It.:'
    _reset_btn_counter()
    kb = {'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'cancel_2fa', 'style': _rs()}]]}
    edit_message(chat_id, msg_id, render_body_text(txt), reply_markup=kb)

def _make_fw_btn(btn, kb):
    b = {'text': btn['text'], 'url': btn['url'], 'style': _rs()}
    if 'icon_custom_emoji_id' in btn:
        b['icon_custom_emoji_id'] = btn['icon_custom_emoji_id']
    return b

def _build_services_keyboard(c_msg_key='get_number'):
    """Helper: GET NUMBER screen ke liye services list keyboard banata hai. Duplicate code remove."""
    local_srvs = set([b['service'] for b in number_batches.values() if b['numbers']])
    nexa_srvs = set(bot_settings.get('nexa_services', {}).keys())
    voltx_srvs = set(bot_settings.get('voltx_services', {}).keys())
    stex_srvs = set(bot_settings.get('stex_services', {}).keys())
    all_services = local_srvs.union(nexa_srvs).union(voltx_srvs).union(stex_srvs)
    c_msg = bot_settings['custom_messages'].get(c_msg_key, {})
    txt = render_body_text(c_msg.get('text', f"{PEM['pin']} Select Service"))
    apps_db = bot_settings.get('premium_apps', {})
    _reset_btn_counter()
    kb = []
    for s in sorted(all_services):
        emoji_id = _get_service_emoji_id(s, apps_db)
        kb.append([{'text': s, 'icon_custom_emoji_id': emoji_id, 'callback_data': f'g_s_{s}', 'style': _rs()}])
    _append_custom_btns(kb, c_msg)
    _add_close_btn(kb)
    return (all_services, txt, kb)

def _search_and_recycle_local(query, chat_id):
    """Search local number_batches for numbers matching prefix query.
    If all matching numbers are already used by this user, recycle them (reset shares/used_by).
    Returns list of (batch_id, index) tuples for available numbers."""
    found_indices = []
    for b_id, b_data in number_batches.items():
        for idx, n_obj in enumerate(b_data['numbers']):
            if n_obj['num'].replace('+', '').startswith(query) and chat_id not in n_obj.get('used_by', []):
                found_indices.append((b_id, idx))
    if not found_indices:
        has_matching = False
        for b_id, b_data in number_batches.items():
            for n_obj in b_data['numbers']:
                if n_obj['num'].replace('+', '').startswith(query):
                    has_matching = True
                    n_obj['shares'] = 0
                    n_obj['used_by'] = []
        if has_matching:
            for b_id, b_data in number_batches.items():
                for idx, n_obj in enumerate(b_data['numbers']):
                    if n_obj['num'].replace('+', '').startswith(query):
                        found_indices.append((b_id, idx))
    return found_indices

def handle_message(msg):
    global total_assigned_stats
    global total_uploaded_stats
    chat_id = msg['chat']['id']
    chat_type = msg['chat'].get('type', 'private')
    if chat_type != 'private':
        return
    text = msg.get('text', '') or ''
    register_user_local(chat_id)
    if is_user_banned(chat_id):
        send_message(chat_id, render_body_text('🚫 <b>You are banned from using this bot!</b>\nIf you think this is a mistake, please contact support.'))
        return
    if text.startswith('/start'):
        parts = text.split()
        if len(parts) > 1 and parts[1].isdigit():
            inviter = int(parts[1])
            if inviter != chat_id:
                u_data = _get_local_user(chat_id)
                if not u_data.get('referred_by'):
                    _update_local_user(chat_id, {'referred_by': inviter, 'ref_paid': False})
    if not check_force_join(chat_id):
        send_force_join_msg(chat_id)
        return
    MAIN_MENU_CMDS = ['GET NUMBER', 'TRAFFIC', 'LIVE TRAFFIC', 'BALANCE', 'SUPPORT', 'Admin Panel', 'DEPOSIT']
    is_main_cmd = False
    if text in MAIN_MENU_CMDS or text.startswith('/start'):
        current_user_msg_id = msg.get('message_id')
        cleanup_user_menu_messages(chat_id)
        if chat_id in user_states:
            user_states.pop(chat_id, None)
        if chat_id in temp_data:
            temp_data.pop(chat_id, None)
        is_main_cmd = True
    if chat_id in user_states and (not is_main_cmd):
        state = user_states[chat_id]

        if state == 'wait_for_deposit_amount' and text:
            try:
                amt = float(text.strip())
                if amt <= 0:
                    send_message(chat_id, render_body_text('❌ Amount must be greater than 0!'), reply_markup=get_cancel_kb())
                    return
                if amt < 50:
                    send_message(chat_id, render_body_text('❌ Minimum deposit is 50৳!'), reply_markup=get_cancel_kb())
                    return
                temp_data[chat_id]['dep_amount'] = amt
                user_states[chat_id] = 'wait_for_deposit_txn'
                delete_message(chat_id, msg['message_id'])
                edit_message(chat_id, temp_data[chat_id]['msg_id'], render_body_text('📝 Now send your Binance Transaction ID (TXN ID):'), reply_markup=get_cancel_kb())
            except ValueError:
                send_message(chat_id, render_body_text('❌ Invalid amount! Please send a valid number.'), reply_markup=get_cancel_kb())
            return

        elif state == 'wait_for_deposit_txn' and text:
            txn_id = text.strip()
            if len(txn_id) < 6:
                send_message(chat_id, render_body_text('❌ TXN ID is too short. Please send a valid Binance Transaction ID.'), reply_markup=get_cancel_kb())
                return
            delete_message(chat_id, msg['message_id'])
            amt = temp_data[chat_id].get('dep_amount', 0)
            req_id = f'D_{str(uuid.uuid4())[:6].upper()}'
            first_name = msg.get('from', {}).get('first_name', 'User')
            last_name = msg.get('from', {}).get('last_name', '')
            full_name = f'{first_name} {last_name}'.strip()
            pending_withdrawals[req_id] = {'user_id': chat_id, 'amount': amt, 'txn_id': txn_id, 'full_name': full_name, 'type': 'deposit'}
            _save_local_withdrawal(req_id, {'user_id': str(chat_id), 'amount': amt, 'txn_id': txn_id, 'type': 'deposit', 'status': 'pending'})
            admin_msg = f"💰 <b>NEW DEPOSIT REQUEST</b>\n\n👤 <b>USER:</b> <a href='tg://user?id={chat_id}'>{full_name}</a>\n💵 <b>AMOUNT:</b> {amt:g}৳\n🆔 <b>TXN ID:</b> <code>{txn_id}</code>\n\n🧾 <b>REQ ID:</b> {req_id}\n👨‍⚖️ <b>PROCESSED BY ADMIN</b>"
            _reset_btn_counter()
            wd_kb = {'inline_keyboard': [[{'text': 'APPROVE', 'icon_custom_emoji_id': '5352694861990501856', 'callback_data': f'dapp_{req_id}', 'style': _rs()}, {'text': 'REJECT', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'drej_{req_id}', 'style': _rs()}]]}
            rendered_admin_msg = render_body_text(admin_msg)
            sent_messages = []
            for adm_id in bot_settings.get('admins', []):
                try:
                    res = send_message(adm_id, rendered_admin_msg, reply_markup=wd_kb)
                    if res.get('ok') and res.get('result') and ('message_id' in res['result']):
                        sent_messages.append({'chat_id': adm_id, 'message_id': res['result']['message_id']})
                except Exception as e:
                    logger.warning(f'Deposit admin notify error: {e}')
            pending_withdrawals[req_id]['sent_messages'] = sent_messages
            _reset_btn_counter()
            kb = {'inline_keyboard': [[{'text': 'Close', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': 'close_msg', 'style': _rs()}]]}
            success_text = f"{PEM['ok']} Your deposit request has been submitted!\n\n🧾 <b>Req ID:</b> {req_id}\n💵 <b>Amount:</b> {amt:g}৳\n🆔 <b>TXN ID:</b> <code>{txn_id}</code>\n\n⏳ Please wait for admin approval."
            edit_message(chat_id, temp_data[chat_id]['msg_id'], render_body_text(success_text), reply_markup=kb)
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return

        if state == 'wait_for_cpanel_url' and text:
            temp_data[chat_id]['p_data']['login_url'] = text.strip()
            user_states[chat_id] = 'wait_for_cpanel_user'
            _show_cpanel_prompt(chat_id, temp_data[chat_id]['msg_id'], 2, 'Username', 'Enter Panel Username:')
            return
        elif state == 'wait_for_cpanel_user' and text:
            if chat_id not in temp_data or 'p_data' not in temp_data.get(chat_id, {}):
                user_states.pop(chat_id, None)
                send_message(chat_id, render_body_text('❌ Session expired. Please try again.'))
                return
            temp_data[chat_id]['p_data']['username'] = text.strip()
            user_states[chat_id] = 'wait_for_cpanel_pass'
            _show_cpanel_prompt(chat_id, temp_data[chat_id]['msg_id'], 3, 'Password', 'Enter Panel Password:')
            return
        elif state == 'wait_for_cpanel_pass' and text:
            if chat_id not in temp_data or 'p_data' not in temp_data.get(chat_id, {}):
                user_states.pop(chat_id, None)
                send_message(chat_id, render_body_text('❌ Session expired. Please try again.'))
                return
            temp_data[chat_id]['p_data']['password'] = text.strip()
            user_states[chat_id] = 'wait_for_cpanel_msg_link'
            _show_cpanel_prompt(chat_id, temp_data[chat_id]['msg_id'], 4, 'Message Link', 'Enter the link where SMS/OTP data (JSON) comes from:')
            return
        elif state == 'wait_for_cpanel_msg_link' and text:
            if chat_id not in temp_data or 'p_data' not in temp_data.get(chat_id, {}):
                user_states.pop(chat_id, None)
                send_message(chat_id, render_body_text('❌ Session expired. Please try again.'))
                return
            temp_data[chat_id]['p_data']['msg_link'] = text.strip()
            user_states[chat_id] = 'wait_for_cpanel_num_col_name'
            _show_cpanel_prompt(chat_id, temp_data[chat_id]['msg_id'], 5, 'Number Column Name', 'What is the Number column name in Data? (e.g. number, phone):')
            return
        elif state == 'wait_for_cpanel_num_col_name' and text:
            if chat_id not in temp_data or 'p_data' not in temp_data.get(chat_id, {}):
                user_states.pop(chat_id, None)
                send_message(chat_id, render_body_text('❌ Session expired. Please try again.'))
                return
            temp_data[chat_id]['p_data']['num_col_name'] = text.strip()
            user_states[chat_id] = 'wait_for_cpanel_num_col_idx'
            _show_cpanel_prompt(chat_id, temp_data[chat_id]['msg_id'], 6, 'Number Column Serial', 'What is the Number Column Serial Number? (e.g. 3, 5):')
            return
        elif state == 'wait_for_cpanel_num_col_idx' and text:
            if chat_id not in temp_data or 'p_data' not in temp_data.get(chat_id, {}):
                user_states.pop(chat_id, None)
                send_message(chat_id, render_body_text('❌ Session expired. Please try again.'))
                return
            if text.isdigit():
                temp_data[chat_id]['p_data']['num_col_idx'] = int(text)
                user_states[chat_id] = 'wait_for_cpanel_msg_col_name'
                _show_cpanel_prompt(chat_id, temp_data[chat_id]['msg_id'], 7, 'Message Column Name', 'What is the Message/OTP column name? (e.g. message, sms):')
            else:
                _err_invalid_serial(chat_id)
            return
        elif state == 'wait_for_cpanel_msg_col_name' and text:
            if chat_id not in temp_data or 'p_data' not in temp_data.get(chat_id, {}):
                user_states.pop(chat_id, None)
                send_message(chat_id, render_body_text('❌ Session expired. Please try again.'))
                return
            temp_data[chat_id]['p_data']['msg_col_name'] = text.strip()
            user_states[chat_id] = 'wait_for_cpanel_msg_col_idx'
            _show_cpanel_prompt(chat_id, temp_data[chat_id]['msg_id'], 8, 'Message Column Serial', 'What is the Message Column Serial Number? (e.g. 5, 7):')
            return
        elif state == 'wait_for_cpanel_msg_col_idx' and text:
            if text.isdigit():
                temp_data[chat_id]['p_data']['msg_col_idx'] = int(text)
                temp_data[chat_id]['p_data']['login_status'] = '⏳ Pending Auto-Login...'
                temp_data[chat_id]['p_data']['needs_warmup'] = True
                bot_settings['panels'].append(temp_data[chat_id]['p_data'])
                save_local_db()
                new_panel_idx = len(bot_settings['panels']) - 1
                threading.Thread(target=_eagerly_warmup_panel, args=(new_panel_idx, bot_settings['panels'][-1]), daemon=True).start()
                send_message(chat_id, render_body_text(f"{PEM['ok']} <b>Auto Captcha Panel Added Successfully!</b>\nBot will now automatically solve captcha and login in background."), reply_markup=main_menu(chat_id))
                msg_id = temp_data[chat_id]['msg_id']
                handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': 'manage_cpt_panels', 'id': 'internal'})
                user_states.pop(chat_id, None)
                temp_data.pop(chat_id, None)
            else:
                _err_invalid_serial(chat_id)
            return
        elif state == 'wait_for_um_bal_uid' and text:
            target_uid_str = text.strip()
            if not target_uid_str.isdigit():
                send_message(chat_id, render_body_text('❌ Invalid ID! Please send a numeric User ID.'), reply_markup=get_cancel_kb())
                return
            target_uid = int(target_uid_str)
            user_data = _get_local_user(target_uid)
            current_bal = user_data.get('balance', 0.0)
            temp_data[chat_id]['target_uid'] = target_uid
            user_states[chat_id] = 'wait_for_um_bal_amt'
            _admin_flow_prompt(chat_id, f'✅ User found!\n💰 Current Balance: {current_bal}৳\n\n📝 Send the amount to ADD (e.g. 50) or REMOVE (e.g. -50):', get_cancel_kb())
            return
        elif state == 'wait_for_um_bal_amt' and text:
            try:
                amt = float(text.strip())
                target_uid = temp_data[chat_id]['target_uid']
                old_bal = _get_local_user(target_uid).get('balance', 0.0)
                update_balance(target_uid, amt)
                new_bal = _get_local_user(target_uid).get('balance', 0.0)
                send_message(chat_id, render_body_text(f"{PEM['ok']} Balance updated!\n{PEM['user']} User: <code>{target_uid}</code>\n💰 Old: {old_bal}৳ → New: {new_bal}৳"), reply_markup=main_menu(chat_id))
                if amt >= 0:
                    notif_text = f"{PEM['gift']} <b>Balance Added!</b>\n➖➖➖➖➖➖➖\n💰 <b>Amount:</b> +{amt}৳\n💰 <b>New Balance:</b> {new_bal}৳\n➖➖➖➖➖➖➖\n👨\u200d⚖️ <b>By Admin</b>"
                else:
                    notif_text = f"{PEM['warn']} <b>Balance Removed!</b>\n➖➖➖➖➖➖➖\n💰 <b>Amount:</b> {amt}৳\n💰 <b>New Balance:</b> {new_bal}৳\n➖➖➖➖➖➖➖\n👨\u200d⚖️ <b>By Admin</b>"
                send_message(target_uid, render_body_text(notif_text))
                user_states.pop(chat_id, None)
                temp_data.pop(chat_id, None)
            except ValueError:
                send_message(chat_id, render_body_text('❌ Invalid amount! Please send a number.'), reply_markup=get_cancel_kb())
            return
        elif state == 'wait_for_um_ban_uid' and text:
            target_uid_str = text.strip()
            if not target_uid_str.isdigit():
                _err_invalid_id(chat_id)
                return
            target_uid = int(target_uid_str)
            user_data = _get_local_user(target_uid)
            current_status = user_data.get('banned', False)
            new_status = not current_status
            _update_local_user(target_uid, {'banned': new_status})
            user_banned_cache[target_uid] = {'banned': new_status, 'time': time.time()}
            status_text = 'BANNED 🚫' if new_status else 'UNBANNED ✅'
            send_message(chat_id, render_body_text(f'✅ User {target_uid} has been {status_text}!'), reply_markup=main_menu(chat_id))
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_um_prof_uid' and text:
            target_uid_str = text.strip()
            if not target_uid_str.isdigit():
                _err_invalid_id(chat_id)
                return
            target_uid = int(target_uid_str)
            data = _get_local_user(target_uid)
            is_verified = True if data.get('total_otps', 0) > 0 else data.get('verified', False)
            prof_text = f"➖➖➖➖➖➖➖➖\n👤 <b>USER PROFILE</b>\n➖➖➖➖➖➖➖➖\n🆔 ID: <code>{target_uid}</code>\n💰 Balance: {data.get('balance', 0.0)}৳\n🤝 Total Refers: {data.get('total_refers', 0)}\n🔐 Total OTPs: {data.get('total_otps', 0)}\n✅ Verified: {is_verified}\n🚫 Banned: {data.get('banned', False)}\n➖➖➖➖➖➖➖➖"
            _reset_btn_counter()
            kb = {'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'user_management', 'style': _rs()}]]}
            _admin_flow_prompt(chat_id, prof_text, kb)
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_menu_text' and text:
            try:
                menu_key = temp_data[chat_id]['menu_key']
                formatted_html_text = extract_premium_html(msg)
                bot_settings['custom_messages'][menu_key]['text'] = formatted_html_text
                save_local_db()
                delete_message(chat_id, msg['message_id'])
                preview_text = render_body_text(formatted_html_text)
                success_text = f"{PEM['ok']} <b>Message Body Updated successfully!</b>\n\n🎨 <b>Editing: {menu_key.upper()}</b>\n\nPreview of current Text:\n{preview_text}"
                edit_message(chat_id, temp_data[chat_id]['msg_id'], render_body_text(success_text), reply_markup=menu_edit_options_keyboard(menu_key))
            except Exception as e:
                send_message(chat_id, render_body_text(f'❌ Error saving text: {e}'))
            finally:
                if chat_id in user_states:
                    user_states.pop(chat_id, None)
                if chat_id in temp_data:
                    temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_menu_btn' and text:
            try:
                menu_key = temp_data[chat_id]['menu_key']
                btn_data = _parse_btn_from_text(text, msg.get('entities', []))
                if btn_data is not None:
                    bot_settings['custom_messages'][menu_key]['buttons'].append(btn_data)
                    save_local_db()
                    delete_message(chat_id, msg['message_id'])
                    edit_message(chat_id, temp_data[chat_id]['msg_id'], render_body_text(f"{PEM['gear']} <b>Edit Inline Buttons: {menu_key.upper()}</b>"), reply_markup=menu_buttons_list_keyboard(menu_key))
                else:
                    send_message(chat_id, render_body_text(f"{PEM['no']} Invalid format. Use <code>Button Text - https://link.com</code>"))
            except Exception as e:
                logger.warning(f'Error: {e}')
            finally:
                if chat_id in user_states:
                    user_states.pop(chat_id, None)
                if chat_id in temp_data:
                    temp_data.pop(chat_id, None)
            return
        elif state in ['wait_for_new_btn_emoji_id', 'wait_for_new_msg_emoji_id'] and text:
            td = temp_data.get(chat_id, {})
            new_id = text.strip()
            if not new_id.isdigit():
                back_page = td.get('idx', 0) // _SYS_EMJ_PAGE_SIZE
                back_cb = f'btn_emoji_page_{back_page}' if state == 'wait_for_new_btn_emoji_id' else f'msg_emoji_page_{back_page}'
                send_message(chat_id, render_body_text(f"{PEM['no']} Invalid! Emoji ID must be <b>numbers only</b>.\nExample: <code>5352552689983067014</code>\n\nTry again:"), reply_markup={'inline_keyboard': [[{'text': 'Cancel', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': back_cb, 'style': _rs()}]]})
                return
            orig_id = td.get('orig_id', '')
            label = td.get('label', '?')
            old_id = td.get('cur_id', orig_id)
            page_idx = td.get('idx', 0)
            kind = td.get('kind', 'btn')
            override_key = f'{kind}_{page_idx}'
            if 'sys_emoji_overrides' not in bot_settings:
                bot_settings['sys_emoji_overrides'] = {}
            bot_settings['sys_emoji_overrides'][override_key] = new_id
            _EMOJI_CHANGE_LOG[override_key] = (new_id, label)
            save_local_db()
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            back_page = page_idx // _SYS_EMJ_PAGE_SIZE
            back_cb = f'btn_emoji_page_{back_page}' if kind == 'btn' else f'msg_emoji_page_{back_page}'
            _reset_btn_counter()
            send_message(chat_id, render_body_text(f"{PEM['ok']} <b>Emoji Replaced!</b>\n\nLabel: <b>{label}</b>\nOld ID: <code>{old_id}</code>\nNew ID: <code>{new_id}</code>\n\n✅ Change saved! New emoji will appear on all future keyboards and messages."), reply_markup={'inline_keyboard': [[{'text': 'Back to List', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': back_cb, 'style': _rs()}]]})
            return
        elif state in ['wait_for_flag_txt', 'wait_for_app_txt'] and 'document' in msg:
            doc = msg['document']
            content = _download_telegram_txt_document(chat_id, doc)
            if content is None:
                return
            mode = 'flags' if state == 'wait_for_flag_txt' else 'apps'
            count = 0
            if mode == 'flags':
                for line in content.splitlines():
                    json_match = re.search('(\\{.*\\})', line)
                    if json_match:
                        try:
                            data = json.loads(json_match.group(1))
                            char = data.get('emoji')
                            eid = data.get('id')
                            prefix_str = line[:json_match.start()].strip()
                            code_match = re.search('\\((\\d+)\\)', prefix_str)
                            iso_match = re.search('\\(([A-Za-z]+)\\)', prefix_str)
                            if code_match and iso_match and char and eid:
                                code = code_match.group(1)
                                iso = iso_match.group(1).upper()
                                name = prefix_str.replace(f'({code})', '').replace(f'({iso_match.group(1)})', '').replace(char, '').strip()
                                bot_settings['premium_flags'][code] = {'char': char, 'iso': iso, 'name': name, 'id': eid}
                                count += 1
                        except Exception as e:
                            logger.warning(f'Error: {e}')
            else:
                for line in content.splitlines():
                    json_match = re.search('(\\{.*\\})', line)
                    if json_match:
                        try:
                            data = json.loads(json_match.group(1))
                            char = data.get('emoji')
                            eid = data.get('id')
                            name_part = line[:json_match.start()].strip()
                            name = name_part.replace(char, '').strip() if char else name_part
                            if char and eid and name:
                                bot_settings['premium_apps'][name.upper()] = {'char': char, 'id': eid, 'name': name}
                                count += 1
                        except Exception as e:
                            logger.warning(f'Error: {e}')
            save_local_db()
            send_message(chat_id, render_body_text(f"{PEM['ok']} Successfully loaded {count} Emojis!"), reply_markup=emoji_settings_keyboard())
            user_states.pop(chat_id, None)
            if chat_id in temp_data:
                temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_broadcast':
            msg_id = msg['message_id']
            send_message(chat_id, render_body_text(f"{PEM['ok']} Broadcast started..."))
            threading.Thread(target=broadcast_copymessage, args=(chat_id, msg_id)).start()
            user_states.pop(chat_id, None)
            if chat_id in temp_data:
                temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_txt' and 'document' in msg:
            doc = msg['document']
            number_lines = _download_telegram_number_document(chat_id, doc)
            if number_lines is None:
                return
            temp_data[chat_id] = {'numbers': number_lines, 'filename': doc.get('file_name', 'numbers.txt')}
            user_states[chat_id] = 'wait_for_service'
            _admin_flow_prompt(chat_id, f"{PEM['ok']} File received.\n\n📌 Enter the service name (e.g., WHATSAPP):", get_cancel_kb())
            return
        elif state == 'wait_for_service' and text:
            temp_data[chat_id]['service'] = text.upper()
            user_states[chat_id] = 'wait_for_country'
            _admin_flow_prompt(chat_id, f"{PEM['ok']} Service set.\n\n🌍 Enter the country name (e.g., YEMEN):", get_cancel_kb())
            return
        elif state == 'wait_for_country' and text:
            country = text.strip().upper()
            temp_data[chat_id]['country'] = country
            try:
                rate = float(bot_settings.get('otp_reward', 0.0) or 0.0)
            except (TypeError, ValueError):
                rate = 0.0
            service = temp_data[chat_id]['service']
            raw_numbers = temp_data[chat_id]['numbers']
            clean_nums = []
            for num in raw_numbers:
                num = num.strip()
                if num:
                    if not num.startswith('+'):
                        num = '+' + num
                    clean_nums.append(num)
            if not clean_nums:
                send_message(chat_id, render_body_text(f"{PEM['no']} No valid numbers found in file!"), reply_markup=main_menu(chat_id))
                user_states.pop(chat_id, None)
                temp_data.pop(chat_id, None)
                return
            batch_id = str(uuid.uuid4())[:8]
            number_batches[batch_id] = {'filename': temp_data[chat_id]['filename'], 'service': service, 'country': country, 'rate': rate, 'numbers': [{'num': n, 'shares': 0, 'used_by': []} for n in clean_nums]}
            with _stats_lock:
                total_uploaded_stats += len(clean_nums)
            save_local_db()
            app_full_name, prem_app_html = get_service_info_html(service)
            prem_flag_html = get_flag_info_html(clean_nums[0])
            broadcast_txt = f'➖➖➖➖➖➖➖➖\n《 NEW NUMBERS 》\n➖➖➖➖➖➖➖➖\n{prem_flag_html} {country} {prem_app_html} {service}\n➖➖➖➖➖➖➖➖\n📤 Total Added: <b>{len(clean_nums)}</b>\nRate: <b>{rate:g}৳</b>\n➖➖➖➖➖➖➖➖\nUse /start to get your numbers!'
            broadcast_txt = render_body_text(broadcast_txt)
            send_message(chat_id, render_body_text(f"{PEM['ok']} Numbers added to local stock!\n\n📊 Total Numbers: <b>{len(clean_nums)}</b>\nRate: <b>{rate:g}৳</b>\n✅ This rate applies to all numbers in this file."))
            threading.Thread(target=broadcast_text_message, args=(broadcast_txt,)).start()
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_sb_api_key' and text:
            bot_settings['smsbower_api_key'] = text.strip()
            save_local_db()
            delete_message(chat_id, msg['message_id'])
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': temp_data[chat_id]['msg_id']}, 'data': 'smsbower_control', 'id': 'internal'})
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_sb_service' and text:
            txt = text.strip()
            if ':' in txt:
                parts = txt.split(':', 1)
                svc = parts[0].strip().lower()
                try:
                    cid = int(parts[1].strip())
                    bot_settings.setdefault('smsbower_services', {})[svc] = cid
                    save_local_db()
                except ValueError:
                    pass
            delete_message(chat_id, msg['message_id'])
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': temp_data[chat_id]['msg_id']}, 'data': 'smsbower_control', 'id': 'internal'})
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return

        elif state == 'wait_for_add_nexa_key' and text:
            bot_settings['nexa_keys'].append(text.strip())
            save_local_db()
            _service_warmup_needed['nexa'] = True
            delete_message(chat_id, msg['message_id'])
            edit_message(chat_id, _td(chat_id, 'msg_id', msg['message_id']), render_body_text(f"✅ Nexa API Key Added! Total Keys: {len(bot_settings.get('nexa_keys', []))}"), reply_markup=_panel_control_keyboard('Nexa'))
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_add_sc' and text:
            code = text.strip().replace('+', '')
            if 'nexa_search_countries' not in bot_settings:
                bot_settings['nexa_search_countries'] = []
            if code not in bot_settings['nexa_search_countries']:
                bot_settings['nexa_search_countries'].append(code)
            save_local_db()
            delete_message(chat_id, msg['message_id'])
            _show_panel_search_countries('nexa', chat_id, _td(chat_id, 'msg_id', msg['message_id']))
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_nx_srv_name' and text:
            srv = text.strip().upper()
            if 'nexa_services' not in bot_settings:
                bot_settings['nexa_services'] = {}
            if srv not in bot_settings['nexa_services']:
                bot_settings['nexa_services'][srv] = {}
            save_local_db()
            delete_message(chat_id, msg['message_id'])
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': temp_data[chat_id]['msg_id']}, 'data': 'manage_nexa_srv', 'id': 'internal'})
            user_states.pop(chat_id, None)
            if chat_id in temp_data:
                temp_data.pop(chat_id, None)
            return
        elif state == 'wait_nx_cnt_name' and text:
            cnt = text.strip()
            srv = temp_data.get(chat_id, {}).get('srv')
            if not srv or srv not in bot_settings.get('nexa_services', {}):
                send_message(chat_id, render_body_text('❌ Session expired. Please start again.'))
                user_states.pop(chat_id, None)
                temp_data.pop(chat_id, None)
                return
            if cnt not in bot_settings['nexa_services'][srv]:
                bot_settings['nexa_services'][srv][cnt] = []
            save_local_db()
            delete_message(chat_id, msg['message_id'])
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': temp_data[chat_id]['msg_id']}, 'data': f'nx_srv_{srv}', 'id': 'internal'})
            user_states.pop(chat_id, None)
            if chat_id in temp_data:
                temp_data.pop(chat_id, None)
            return
        elif state == 'wait_nx_addr' and text:
            srv = temp_data.get(chat_id, {}).get('srv')
            cnt = temp_data.get(chat_id, {}).get('cnt')
            if not srv or not cnt or srv not in bot_settings.get('nexa_services', {}):
                send_message(chat_id, render_body_text('❌ Session expired. Please start again.'))
                user_states.pop(chat_id, None)
                temp_data.pop(chat_id, None)
                return
            new_range = text.strip().replace('+', '')
            if new_range not in bot_settings['nexa_services'][srv][cnt]:
                bot_settings['nexa_services'][srv][cnt].append(new_range)
                if 'nexa_search_countries' not in bot_settings:
                    bot_settings['nexa_search_countries'] = []
                nexa_prefix = new_range.replace('X', '').replace('x', '')
                if nexa_prefix and nexa_prefix not in bot_settings['nexa_search_countries']:
                    bot_settings['nexa_search_countries'].append(nexa_prefix)
                save_local_db()
            delete_message(chat_id, msg['message_id'])
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': temp_data[chat_id]['msg_id']}, 'data': f'nx_cnt_{srv}_{cnt}', 'id': 'internal'})
            user_states.pop(chat_id, None)
            if chat_id in temp_data:
                temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_add_voltx_key' and text:
            bot_settings['voltx_keys'].append(text.strip())
            save_local_db()
            _service_warmup_needed['voltx'] = True
            delete_message(chat_id, msg['message_id'])
            edit_message(chat_id, _td(chat_id, 'msg_id', msg['message_id']), render_body_text(f"✅ VoltX API Key Added! Total Keys: {len(bot_settings.get('voltx_keys', []))}"), reply_markup=_panel_control_keyboard('VoltX'))
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_vx_srv_name' and text:
            srv = text.strip().upper()
            if 'voltx_services' not in bot_settings:
                bot_settings['voltx_services'] = {}
            if srv not in bot_settings['voltx_services']:
                bot_settings['voltx_services'][srv] = {}
            save_local_db()
            delete_message(chat_id, msg['message_id'])
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': temp_data[chat_id]['msg_id']}, 'data': 'manage_voltx_srv', 'id': 'internal'})
            user_states.pop(chat_id, None)
            if chat_id in temp_data:
                temp_data.pop(chat_id, None)
            return
        elif state == 'wait_vx_cnt_name' and text:
            cnt = text.strip()
            srv = temp_data[chat_id]['srv']
            if cnt not in bot_settings['voltx_services'][srv]:
                bot_settings['voltx_services'][srv][cnt] = []
            save_local_db()
            delete_message(chat_id, msg['message_id'])
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': temp_data[chat_id]['msg_id']}, 'data': f'vx_srv_{srv}', 'id': 'internal'})
            user_states.pop(chat_id, None)
            if chat_id in temp_data:
                temp_data.pop(chat_id, None)
            return
        elif state == 'wait_vx_addr' and text:
            srv, cnt = (temp_data[chat_id]['srv'], temp_data[chat_id]['cnt'])
            new_range = text.strip()
            if new_range not in bot_settings['voltx_services'][srv][cnt]:
                bot_settings['voltx_services'][srv][cnt].append(new_range)
                if 'voltx_search_countries' not in bot_settings:
                    bot_settings['voltx_search_countries'] = []
                prefix = new_range.replace('X', '').replace('x', '')
                if prefix and prefix not in bot_settings['voltx_search_countries']:
                    bot_settings['voltx_search_countries'].append(prefix)
                save_local_db()
            delete_message(chat_id, msg['message_id'])
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': temp_data[chat_id]['msg_id']}, 'data': f'vx_cnt_{srv}_{cnt}', 'id': 'internal'})
            user_states.pop(chat_id, None)
            if chat_id in temp_data:
                temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_add_vxsc' and text:
            code = text.strip().replace('+', '')
            if 'voltx_search_countries' not in bot_settings:
                bot_settings['voltx_search_countries'] = []
            if code not in bot_settings['voltx_search_countries']:
                bot_settings['voltx_search_countries'].append(code)
            save_local_db()
            delete_message(chat_id, msg['message_id'])
            _show_panel_search_countries('voltx', chat_id, _td(chat_id, 'msg_id', msg['message_id']))
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_add_stex_key' and text:
            bot_settings['stex_keys'].append(text.strip())
            save_local_db()
            _service_warmup_needed['stex'] = True
            delete_message(chat_id, msg['message_id'])
            edit_message(chat_id, _td(chat_id, 'msg_id', msg['message_id']), render_body_text(f"✅ Stex API Key Added! Total Keys: {len(bot_settings.get('stex_keys', []))}"), reply_markup=_panel_control_keyboard('Stex'))
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_stx_srv_name' and text:
            srv = text.strip().upper()
            if 'stex_services' not in bot_settings:
                bot_settings['stex_services'] = {}
            if srv not in bot_settings['stex_services']:
                bot_settings['stex_services'][srv] = {}
            save_local_db()
            delete_message(chat_id, msg['message_id'])
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': temp_data[chat_id]['msg_id']}, 'data': 'manage_stex_srv', 'id': 'internal'})
            user_states.pop(chat_id, None)
            if chat_id in temp_data:
                temp_data.pop(chat_id, None)
            return
        elif state == 'wait_stx_cnt_name' and text:
            cnt = text.strip()
            srv = temp_data[chat_id]['srv']
            if cnt not in bot_settings['stex_services'][srv]:
                bot_settings['stex_services'][srv][cnt] = []
            save_local_db()
            delete_message(chat_id, msg['message_id'])
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': temp_data[chat_id]['msg_id']}, 'data': f'stx_srv_{srv}', 'id': 'internal'})
            user_states.pop(chat_id, None)
            if chat_id in temp_data:
                temp_data.pop(chat_id, None)
            return
        elif state == 'wait_stx_addr' and text:
            srv, cnt = (temp_data[chat_id]['srv'], temp_data[chat_id]['cnt'])
            new_range = text.strip()
            if new_range not in bot_settings['stex_services'][srv][cnt]:
                bot_settings['stex_services'][srv][cnt].append(new_range)
                if 'stex_search_countries' not in bot_settings:
                    bot_settings['stex_search_countries'] = []
                prefix = new_range.replace('X', '').replace('x', '')
                if prefix and prefix not in bot_settings['stex_search_countries']:
                    bot_settings['stex_search_countries'].append(prefix)
                save_local_db()
            delete_message(chat_id, msg['message_id'])
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': temp_data[chat_id]['msg_id']}, 'data': f'stx_cnt_{srv}_{cnt}', 'id': 'internal'})
            user_states.pop(chat_id, None)
            if chat_id in temp_data:
                temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_add_stxsc' and text:
            code = text.strip().replace('+', '')
            if 'stex_search_countries' not in bot_settings:
                bot_settings['stex_search_countries'] = []
            if code not in bot_settings['stex_search_countries']:
                bot_settings['stex_search_countries'].append(code)
            save_local_db()
            delete_message(chat_id, msg['message_id'])
            _show_panel_search_countries('stex', chat_id, _td(chat_id, 'msg_id', msg['message_id']))
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_add_wm' and text:
            bot_settings['w_methods'].append(text.strip())
            save_local_db()
            delete_message(chat_id, msg['message_id'])
            edit_message(chat_id, _td(chat_id, 'msg_id', msg['message_id']), render_body_text('💳 <b>WITHDRAWAL METHODS</b>\n\nManage your withdrawal methods below:'), reply_markup=w_methods_keyboard())
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_add_fj' and text:
            raw_input = text.strip()
            if 't.me/+' in raw_input or 't.me/joinchat/' in raw_input:
                delete_message(chat_id, msg['message_id'])
                edit_message(chat_id, temp_data[chat_id]['msg_id'], render_body_text('⚠️ <b>Private invite link detected!</b>\n\nFor a private channel/group, send the numeric ID (e.g. <code>-1001234567890</code>)\n\nHow to find the ID:\n1. Forward any message from the Channel/Group\n2. Forward it to @userinfobot\n3. It will show you the ID'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_fj', 'style': _rs()}]]})
                return
            parsed_id = parse_chat_id(raw_input)
            detected = auto_detect_chat(parsed_id)
            if detected:
                bot_settings['fj_channels'].append(detected)
                save_local_db()
                delete_message(chat_id, msg['message_id'])
                type_label = 'Channel' if detected['type'] == 'channel' else 'Group'
                priv_label = 'Private' if detected['is_private'] else 'Public'
                edit_message(chat_id, temp_data[chat_id]['msg_id'], render_body_text(f"✅ <b>Successfully Added!</b>\n\n{type_label} | {priv_label}\n📌 Title: <b>{detected['title']}</b>\n🆔 ID: <code>{detected['chat_id']}</code>\n🔗 Link: {detected.get('invite_link', 'N/A')}"), reply_markup=fj_settings_keyboard())
            else:
                delete_message(chat_id, msg['message_id'])
                edit_message(chat_id, temp_data[chat_id]['msg_id'], render_body_text('❌ <b>Error!</b> Bot is not admin in this channel/group or the ID is invalid.\n\nMake sure:\n1. Add the bot to the channel/group\n2. Make the bot an administrator\n3. Then try again'), reply_markup={'inline_keyboard': [[{'text': 'Try Again', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': 'add_fj', 'style': _rs()}, {'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_fj', 'style': _rs()}]]})
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_add_adm' and text:
            if text.isdigit():
                bot_settings['admins'].append(int(text))
                save_local_db()
            delete_message(chat_id, msg['message_id'])
            edit_message(chat_id, _td(chat_id, 'msg_id', msg['message_id']), render_body_text('👥 <b>ADMIN MANAGEMENT</b>\nManage your bot admins below:'), reply_markup=admin_settings_keyboard())
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_add_fw_id' and text:
            bot_settings['fw_groups'].append({'chat_id': text.strip(), 'buttons': []})
            save_local_db()
            delete_message(chat_id, msg['message_id'])
            edit_message(chat_id, _td(chat_id, 'msg_id', msg['message_id']), render_body_text('🛡 <b>OTP GROUP MANAGEMENT</b>\nManage settings below:'), reply_markup=otp_groups_list_keyboard())
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_add_fw_btn' and text:
            fw_idx = _td(chat_id, 'fw_idx', -1)
            if fw_idx < 0 or fw_idx >= len(bot_settings.get('fw_groups', [])):
                send_message(chat_id, render_body_text('❌ Group not found!'))
                user_states.pop(chat_id, None)
                temp_data.pop(chat_id, None)
                return
            btn_data = _parse_btn_from_text(text, msg.get('entities', []))
            if btn_data is not None:
                bot_settings['fw_groups'][fw_idx]['buttons'].append(btn_data)
            save_local_db()
            delete_message(chat_id, msg['message_id'])
            edit_message(chat_id, temp_data[chat_id]['msg_id'], render_body_text(f"🛡 <b>Manage Group:</b> {bot_settings['fw_groups'][fw_idx]['chat_id']}"), reply_markup=specific_fw_group_keyboard(fw_idx))
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_test_service' and text:
            temp_data.setdefault(chat_id, {})['service'] = text.strip()
            user_states[chat_id] = 'wait_for_test_number'
            send_message(chat_id, render_body_text('📝 Send the Number (e.g. +8801712345678):'), reply_markup=get_cancel_kb())
            return
        elif state == 'wait_for_test_number' and text:
            temp_data.setdefault(chat_id, {})['number'] = text.strip()
            user_states[chat_id] = 'wait_for_test_otp'
            send_message(chat_id, render_body_text('📝 Send the OTP (e.g. 556677):'), reply_markup=get_cancel_kb())
            return
        elif state == 'wait_for_test_otp' and text:
            temp_data.setdefault(chat_id, {})['otp'] = text.strip()
            user_states[chat_id] = 'wait_for_test_language'
            send_message(chat_id, render_body_text('📝 Send the OTP Language (e.g. English, French):'), reply_markup=get_cancel_kb())
            return
        elif state == 'wait_for_test_language' and text:
            temp_data.setdefault(chat_id, {})['language'] = text.strip()
            td = temp_data.get(chat_id, {})
            srv = str(td.get('service', '')).strip()
            num = str(td.get('number', '')).strip()
            otp = str(td.get('otp', '')).strip()

            display_num = f'+{num}' if not num.startswith('+') else num
            masked = mask_number(display_num)
            prem_flag_html = get_flag_info_html(display_num)
            _, iso = get_flag_and_code(display_num)
            app_full_name, prem_app_html = get_service_info_html(srv)

            _g_clean = str(display_num).replace('+', '').replace(' ', '')
            _g_masked = f'{_g_clean[:4]}{_MASK_EMOJI}{_g_clean[-4:]}{_END_NUMBER_EMOJI}' if len(_g_clean) >= 8 else masked
            iso_text = f' #{iso}' if iso else ''
            test_lang = str(td.get('language', '')).strip()
            lang_line = f'\n💬 {html.escape(test_lang)}' if test_lang else ''
            group_msg = _otp_box_message(f'{get_flag_info_html(display_num)}{iso_text} {prem_app_html} {_g_masked}', lang_line)

            fw_groups = bot_settings.get('fw_groups', [])
            if not fw_groups:
                send_message(chat_id, render_body_text('❌ No Forward Group is configured!'), reply_markup=main_menu(chat_id))
            else:
                for fw in fw_groups:
                    try:
                        _reset_btn_counter()
                        kb = [[{'text': otp, 'icon_custom_emoji_id': _OTP_COPY_EMOJI_ID, 'copy_text': {'text': otp}, 'style': _rs()}]]
                        _fw_btns = []
                        for btn in fw.get('buttons', []):
                            if str(btn.get('text', '')).strip().lower() == 'full message':
                                continue
                            _fw_btns.append(_make_fw_btn(btn, kb))
                        for _i in range(0, len(_fw_btns), 2):
                            kb.append(_fw_btns[_i:_i + 2])

                        send_message(fw['chat_id'], group_msg, reply_markup={'inline_keyboard': kb})
                    except Exception as e:
                        logger.warning(f'Test message send error ({fw.get("chat_id")}): {e}')
                send_message(chat_id, render_body_text(f"{PEM['ok']} Test OTP sent in original Forward Group format!"), reply_markup=main_menu(chat_id))
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_topic_name' and text:
            temp_data.setdefault(chat_id, {})['topic_name'] = text.strip()
            user_states[chat_id] = 'wait_for_topic_keyword'
            delete_message(chat_id, msg['message_id'])
            edit_message(chat_id, temp_data[chat_id]['msg_id'], render_body_text('📝 <b>Filter Keyword</b>\n\nSend the keyword to match in incoming OTP messages.\nExample: <code>whatsapp</code>'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'topic_settings', 'style': _rs()}]]})
            return
        elif state == 'wait_for_topic_keyword' and text:
            temp_data.setdefault(chat_id, {})['topic_keyword'] = text.strip()
            user_states[chat_id] = 'wait_for_topic_id'
            delete_message(chat_id, msg['message_id'])
            edit_message(chat_id, temp_data[chat_id]['msg_id'], render_body_text('📝 <b>Topic ID</b>\n\nSend the Telegram Topic ID (message_thread_id).\nExample: <code>803586</code>'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'topic_settings', 'style': _rs()}]]})
            return
        elif state == 'wait_for_topic_id' and text:
            try:
                topic_id = int(text.strip())
                if topic_id <= 0:
                    raise ValueError
            except ValueError:
                edit_message(chat_id, temp_data[chat_id]['msg_id'], render_body_text('❌ Invalid Topic ID. Please send a positive numeric Topic ID.'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'topic_settings', 'style': _rs()}]]})
                return
            td = temp_data.get(chat_id, {})
            bot_settings.setdefault('topics', []).append({'name': td.get('topic_name', 'Topic'), 'keyword': td.get('topic_keyword', ''), 'topic_id': topic_id})
            save_local_db()
            delete_message(chat_id, msg['message_id'])
            edit_message(chat_id, td['msg_id'], render_body_text(f"✅ <b>Topic Saved!</b>\n\nName: <b>{html.escape(str(td.get('topic_name', 'Topic')))}</b>\nKeyword: <code>{html.escape(str(td.get('topic_keyword', '')))}</code>\nTopic ID: <code>{topic_id}</code>"), reply_markup=topic_settings_keyboard())
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_otp_link' and text:
            bot_settings['otp_link'] = text.strip()
            save_local_db()
            delete_message(chat_id, msg['message_id'])
            edit_message(chat_id, temp_data[chat_id]['msg_id'], render_body_text('🛡 <b>OTP GROUP MANAGEMENT</b>\nManage settings below:'), reply_markup=otp_groups_list_keyboard())
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_panel_name' and text:
            p_name = text.strip()
            t_key = temp_data[chat_id].get('add_type', 'api')
            msg_id = temp_data[chat_id]['msg_id']
            delete_message(chat_id, msg['message_id'])
            if t_key == 'logc':
                user_states[chat_id] = 'wait_for_cpanel_url'
                temp_data[chat_id] = {'msg_id': msg_id, 'p_data': {'name': p_name, 'type': 'Auto Captcha Panel', 'status': 'ON', 'records': 0, 'login_status': '⏳ Pending First Login'}}
                edit_message(chat_id, msg_id, render_body_text('1️⃣ <b>Login URL</b>\n➡️ Enter Panel Login Link:'), reply_markup=get_cancel_kb())
                return
            else:
                bot_settings['panels'].append({'name': p_name, 'type': 'API Panel', 'status': 'OFF', 'api_url': '', 'token': '', 'records': 0, 'needs_warmup': True})
                save_local_db()
                handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': 'manage_api_panels', 'id': 'internal'})
                if chat_id in user_states:
                    user_states.pop(chat_id, None)
                if chat_id in temp_data:
                    temp_data.pop(chat_id, None)
                return
        elif state == 'wait_for_p_api' and text:
            _save_panel_field(chat_id, msg, 'api_url', text.strip())
            return
        elif state == 'wait_for_p_tok' and text:
            _save_panel_field(chat_id, msg, 'token', text.strip())
            return
        elif state == 'wait_for_p_tokheader' and text:
            idx = _td(chat_id, 'p_idx', -1)
            if idx < 0 or idx >= len(bot_settings['panels']):
                _err_panel_gone(chat_id)
            else:
                val = text.strip()
                if val.lower() == 'none':
                    bot_settings['panels'][idx].pop('token_header', None)
                else:
                    bot_settings['panels'][idx]['token_header'] = val
                save_local_db()
                delete_message(chat_id, msg['message_id'])
                _show_panel_cfg(chat_id, _td(chat_id, 'msg_id', msg['message_id']), idx)
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_p_fapi' and text:
            _save_panel_field(chat_id, msg, 'full_api_url', text.strip())
            return
        elif state == 'wait_for_p_rec' and text:
            if text.isdigit():
                idx = temp_data[chat_id]['p_idx']
                if idx < 0 or idx >= len(bot_settings['panels']):
                    _err_panel_gone(chat_id)
                else:
                    bot_settings['panels'][idx]['records'] = int(text)
                    save_local_db()
                    delete_message(chat_id, msg['message_id'])
                    _show_panel_cfg(chat_id, temp_data[chat_id]['msg_id'], idx)
                user_states.pop(chat_id, None)
                temp_data.pop(chat_id, None)
            else:
                send_message(chat_id, render_body_text('❌ Please enter a valid number! Try again.'))
            return
        elif state == 'set_abhi':
            msg_id = _td(chat_id, 'msg_id', msg['message_id'])
            key = _td(chat_id, 'key', '')
            if not key:
                user_states.pop(chat_id, None)
                temp_data.pop(chat_id, None)
                return
            try:
                if key in ['min_withdraw', 'otp_reward', 'refer_reward']:
                    bot_settings[key] = float(text)
                elif key in ['cooldown', 'num_req', 'num_share']:
                    bot_settings[key] = int(text)
                else:
                    bot_settings[key] = text
                save_local_db()
                delete_message(chat_id, msg['message_id'])
                _show_abhi_panel(chat_id, msg_id)
            except Exception as e:
                delete_message(chat_id, msg['message_id'])
                _show_abhi_panel(chat_id, msg_id, '❌ Invalid value!')
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_search' and text:
            query = text.strip().replace('+', '').replace(' ', '').upper()
            if not re.fullmatch('\\d{3,9}X{1,9}', query) and (not re.fullmatch('\\d{3,9}', query)):
                send_message(chat_id, render_body_text('❌ Use a valid range like <code>26134XXXX</code> or a 3-9 digit prefix.'))
                return
            api_query = query.rstrip('X')
            wait_msg = send_message(chat_id, render_body_text('⌛ <i>Processing... Finding Number...</i>'))
            wait_msg_id = wait_msg.get('result', {}).get('message_id') if isinstance(wait_msg, dict) else None
            if wait_msg_id:
                edit_message(chat_id, wait_msg_id, render_body_text('⌛ <i>Processing... Finding Number via API...</i>'))
            fetched_nums = []
            target_count = max(1, int(bot_settings.get('num_req', 1) or 1))
            max_attempts = max(target_count * 4, 4)
            seen_nums = set()
            for _attempt in range(max_attempts):
                if len(fetched_nums) >= target_count:
                    break
                _api_num, _api_panel = _fetch_number_via_panels(api_query, chat_id, force_auto=True)
                if not _api_num:
                    continue
                clean_api_num = re.sub('\\D', '', str(_api_num))
                if not clean_api_num or clean_api_num in seen_nums:
                    continue
                seen_nums.add(clean_api_num)
                fetched_nums.append(clean_api_num)
            if not fetched_nums:
                if wait_msg_id:
                    delete_message(chat_id, wait_msg_id)
                send_message(chat_id, render_body_text('❌ <b>No number was returned by the enabled API panels for this range.</b>\n\nPlease try another prefix.'), reply_markup=main_menu(chat_id))
                user_states.pop(chat_id, None)
                temp_data.pop(chat_id, None)
                return
            save_local_db()
            if wait_msg_id:
                edit_message(chat_id, wait_msg_id, render_body_text('✅ Number Found!'))
            _sess_msg = {'nums': fetched_nums, 'service': '', 'country': '', 'ctx': 'search', 'query': query, 'rate_by_num': {str(_n).replace('+', '').replace(' ', '').replace('-', '').strip(): bot_settings.get('otp_reward', 0.0) for _n in fetched_nums}, 'rates': [bot_settings.get('otp_reward', 0.0)] * len(fetched_nums), 'cc_codes': _build_cc_codes(fetched_nums), 'cc_state': [True] * len(fetched_nums), 'msg_id': wait_msg_id or 0}
            user_active_sessions[chat_id] = _sess_msg
            user_otp_delivery_active[chat_id] = True
            kb = _rebuild_num_kb(chat_id)
            num_text = render_body_text(_build_num_text(chat_id))
            if wait_msg_id:
                try:
                    edit_message(chat_id, wait_msg_id, num_text, reply_markup={'inline_keyboard': kb})
                except Exception:
                    msg_res = send_message(chat_id, num_text, reply_markup={'inline_keyboard': kb})
                    if msg_res and msg_res.get('ok') and msg_res.get('result'):
                        user_active_sessions[chat_id]['msg_id'] = msg_res['result']['message_id']
            else:
                msg_res = send_message(chat_id, num_text, reply_markup={'inline_keyboard': kb})
                if msg_res and msg_res.get('ok') and msg_res.get('result'):
                    user_active_sessions[chat_id]['msg_id'] = msg_res['result']['message_id']
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return
        elif state == 'wait_for_withdraw_amount' and text:
            msg_id_to_edit = temp_data[chat_id].get('msg_id')
            try:
                amount = float(text.strip())
                bal = _td(chat_id, 'balance', 0.0)
                min_w = bot_settings.get('min_withdraw', 30.0)
                if amount < min_w:
                    if msg_id_to_edit:
                        edit_message(chat_id, msg_id_to_edit, render_body_text(f'❌ Minimum withdrawal is {min_w}৳!\n💰 Balance: {bal}৳\n\n📝 Enter again:'), reply_markup=get_cancel_kb())
                    return
                if amount > bal:
                    if msg_id_to_edit:
                        edit_message(chat_id, msg_id_to_edit, render_body_text(f"❌ You don't have enough balance!\n💰 Balance: {bal}৳\n\n📝 Enter again:"), reply_markup=get_cancel_kb())
                    return
                temp_data[chat_id]['amount'] = amount
                user_states[chat_id] = 'wait_for_withdraw_number'
                if msg_id_to_edit:
                    edit_message(chat_id, msg_id_to_edit, render_body_text(f"✅ Amount: {amount}৳\n\n📱 Now send your <b>{temp_data[chat_id]['method']}</b> account number:"), reply_markup=get_cancel_kb())
            except ValueError:
                if msg_id_to_edit:
                    edit_message(chat_id, msg_id_to_edit, render_body_text('❌ Invalid amount!\n\n📝 Please send a valid number:'), reply_markup=get_cancel_kb())
            return
        elif state == 'wait_for_2fa_name' and text:
            msg_id_to_edit = temp_data.get(chat_id, {}).get('msg_id')
            delete_message(chat_id, msg.get('message_id'))
            if not msg_id_to_edit:
                send_message(chat_id, render_body_text('❌ Error: Message not found. Try again.'))
                user_states.pop(chat_id, None)
                if chat_id in temp_data:
                    temp_data.pop(chat_id, None)
                return
            name = text.strip()[:30]
            temp_data[chat_id]['2fa_name'] = name
            user_states[chat_id] = 'wait_for_2fa_key'
            ask_key_txt = f'➖➖➖➖➖➖➖➖➖➖➖➖\n《 🔑 <b>ENTER 2FA KEY</b> 》\n➖➖➖➖➖➖➖➖➖➖➖➖\n📛 <b>NAME:</b> {name}\n➖➖➖➖➖➖➖➖➖➖➖➖\n📝 Now send your <b>2FA</b> Secret Key\n➖➖➖➖➖➖➖➖➖➖➖➖\n💡 <b>Where can I find the Secret Key?</b>\nCopy and send the <b>32-digit key</b> written below the <b>QR code</b>.\n➖➖➖➖➖➖➖➖➖➖➖➖'
            _reset_btn_counter()
            cancel_kb = {'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'back_to_2fa_name', 'style': _rs()}]]}
            edit_message(chat_id, msg_id_to_edit, render_body_text(ask_key_txt), reply_markup=cancel_kb)
            return
        elif state == 'wait_for_2fa_key' and text:
            msg_id_to_edit = temp_data.get(chat_id, {}).get('msg_id')
            delete_message(chat_id, msg.get('message_id'))
            if not msg_id_to_edit:
                send_message(chat_id, render_body_text('❌ Error: Message not found. Try again.'))
                user_states.pop(chat_id, None)
                if chat_id in temp_data:
                    temp_data.pop(chat_id, None)
                return
            entry_name = temp_data.get(chat_id, {}).get('2fa_name', 'My Account')
            try:
                secret = text.strip().replace(' ', '')
                totp = pyotp.TOTP(secret)
                code = totp.now()
                remaining_time = 30 - int(time.time()) % 30
                if chat_id not in user_2fa_saved:
                    user_2fa_saved[chat_id] = []
                existing_keys = [e['key'] for e in user_2fa_saved[chat_id]]
                if secret not in existing_keys:
                    user_2fa_saved[chat_id].append({'name': entry_name, 'key': secret})
                    _save_2fa_saved()
                success_txt = _build_2fa_code_txt(entry_name, code, remaining_time)
                kb = _build_2fa_code_kb(code, secret)
                edit_message(chat_id, msg_id_to_edit, render_body_text(success_txt), reply_markup={'inline_keyboard': kb})
                user_states.pop(chat_id, None)
                if chat_id in temp_data:
                    temp_data.pop(chat_id, None)
            except Exception as e:
                logger.warning(f'2FA key validation error: {e}')
                error_txt = f'➖➖➖➖➖➖➖➖➖➖➖➖\n《 🔑 <b>ENTER 2FA KEY</b> 》\n➖➖➖➖➖➖➖➖➖➖➖➖\n📛 <b>NAME:</b> {entry_name}\n➖➖➖➖➖➖➖➖➖➖➖➖\n📝 <b>Send your 2FA Secret Key</b>\n➖➖➖➖➖➖➖➖➖➖➖➖\n❌ <b>Invalid Secret Key! Please try again.</b>\n➖➖➖➖➖➖➖➖➖➖➖➖'
                _reset_btn_counter()
                cancel_kb = {'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'back_to_2fa_name', 'style': _rs()}]]}
                edit_message(chat_id, msg_id_to_edit, render_body_text(error_txt), reply_markup=cancel_kb)
            return
        elif state == 'wait_for_withdraw_number':
            if not _td_has(chat_id, 'method', 'amount'):
                send_message(chat_id, render_body_text('❌ Session expired. Please start withdrawal again.'))
                user_states.pop(chat_id, None)
                temp_data.pop(chat_id, None)
                return
            msg_id_to_edit = _td(chat_id, 'msg_id')
            method = _td(chat_id, 'method', 'UPI')
            amount = _td(chat_id, 'amount', 0)
            number = text
            req_id = f'W_{str(uuid.uuid4())[:6].upper()}'
            first_name = msg.get('from', {}).get('first_name', 'User')
            last_name = msg.get('from', {}).get('last_name', '')
            full_name = f'{first_name} {last_name}'.strip()
            update_balance(chat_id, -amount)
            pending_withdrawals[req_id] = {'user_id': chat_id, 'amount': amount, 'method': method, 'number': number, 'full_name': full_name}
            _save_local_withdrawal(req_id, {'user_id': str(chat_id), 'amount': amount, 'method': method, 'status': 'pending'})
            admin_msg = f"🎙 <b>NEW WITHDRAWAL REQUEST</b>\n\n👤 <b>USER:</b> <a href='tg://user?id={chat_id}'>{full_name}</a>\n💳 <b>WITHDRAWAL:</b> {amount}৳\n🍏 <b>NUMBER:</b> <code>{number}</code>\n🏦 <b>METHOD:</b> {method}\n\n🧾 <b>REQ ID:</b> {req_id}\n👨\u200d⚖️ <b>PROCESSED BY ADMIN</b>"
            _reset_btn_counter()
            wd_kb = {'inline_keyboard': [[{'text': 'APPROVE', 'icon_custom_emoji_id': '5352694861990501856', 'callback_data': f'wapp_{req_id}', 'style': _rs()}, {'text': 'REJECT', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'wrej_{req_id}', 'style': _rs()}]]}
            rendered_admin_msg = render_body_text(admin_msg)
            sent_messages = []
            if bot_settings.get('w_group'):
                try:
                    res = send_message(bot_settings['w_group'], rendered_admin_msg, reply_markup=wd_kb)
                    if res.get('ok') and res.get('result') and ('message_id' in res['result']):
                        sent_messages.append({'chat_id': bot_settings['w_group'], 'message_id': res['result']['message_id']})
                    else:
                        for adm_id in bot_settings.get('admins', []):
                            try:
                                send_message(adm_id, render_body_text(f"⚠️ W.GROUP ({bot_settings['w_group']}) message delivery failed. Please check the Group ID."))
                            except Exception as e:
                                logger.warning(f'Error: {e}')
                except Exception as e:
                    logger.warning(f'Error: {e}')
            for adm_id in bot_settings.get('admins', []):
                if adm_id != chat_id:
                    try:
                        res = send_message(adm_id, rendered_admin_msg, reply_markup=wd_kb)
                        if res.get('ok') and res.get('result') and ('message_id' in res['result']):
                            sent_messages.append({'chat_id': adm_id, 'message_id': res['result']['message_id']})
                    except Exception as e:
                        logger.warning(f'Error: {e}')
            pending_withdrawals[req_id]['sent_messages'] = sent_messages
            _reset_btn_counter()
            kb = {'inline_keyboard': [[{'text': 'Close', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': 'close_msg', 'style': _rs()}]]}
            success_text = f"{PEM['ok']} Your withdrawal request has been submitted!\n\n🧾 <b>Req ID:</b> {req_id}\n💰 <b>Amount:</b> {amount}৳\n🏦 <b>Method:</b> {method}\n📱 <b>Number:</b> <code>{number}</code>"
            if msg_id_to_edit:
                edit_message(chat_id, msg_id_to_edit, render_body_text(success_text), reply_markup=kb)
            else:
                send_message(chat_id, render_body_text(success_text), reply_markup=kb)
            user_states.pop(chat_id, None)
            temp_data.pop(chat_id, None)
            return

    if text.startswith('/start'):
        first_name = msg.get('from', {}).get('first_name', 'User')
        _welcome_user(chat_id, first_name)
    elif text == 'TRAFFIC' or text == 'LIVE TRAFFIC':
        txt, markup = build_traffic_ui()
        send_message(chat_id, txt, reply_markup=markup)
    elif text == 'BALANCE':
        u_data = get_user(chat_id)
        bal = u_data.get('balance', 0.0)
        c_msg = bot_settings['custom_messages'].get('balance', DEFAULT_CUSTOM_MESSAGES['balance'])
        raw_txt = c_msg.get('text', DEFAULT_CUSTOM_MESSAGES['balance']['text']).replace('{bal}', str(bal)).replace('{total_otp}', str(u_data.get('total_otps', 0))).replace('{total_ref}', str(u_data.get('total_refers', 0))).replace('{min_w}', str(bot_settings.get('min_withdraw', 30.0)))
        txt = render_body_text(raw_txt)
        _reset_btn_counter()
        kb = [[{'text': 'WITHDRAWAL', 'icon_custom_emoji_id': '5352585194295564660', 'callback_data': 'balance_withdrawal', 'style': 'primary'}], [{'text': 'CLOSE', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': 'close_msg', 'style': 'danger'}]]
        send_message(chat_id, txt, reply_markup={'inline_keyboard': kb})

    elif text == 'DEPOSIT':
        deposit_txt = (
            "➖➖➖➖➖➖➖➖➖➖\n"
            "《 💰 DEPOSIT 》\n"
            "➖➖➖➖➖➖➖➖➖➖\n"
            "💳 <b>Payment Method:</b> Binance Pay\n"
            "🆔 <b>Binance Pay ID:</b> <code>732182215</code>\n"
            "➖➖➖➖➖➖➖➖➖➖\n"
            "📝 <b>How to Deposit:</b>\n"
            "1️⃣ Binance App এ যান\n"
            "2️⃣ Binance Pay → Send এ ক্লিক করুন\n"
            "3️⃣ উপরের ID তে টাকা পাঠান\n"
            "4️⃣ Payment screenshot Support এ পাঠান\n"
            "➖➖➖➖➖➖➖➖➖➖"
        )
        _reset_btn_counter()
        kb = [
            [{'text': '732182215', 'icon_custom_emoji_id': '5192739271886282680', 'copy_text': {'text': '732182215'}, 'style': _rs()}],
            [{'text': 'I HAVE PAID', 'icon_custom_emoji_id': '5352694861990501856', 'callback_data': 'dep_paid_start', 'style': _rs()}],
            [{'text': 'CLOSE', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': 'close_msg', 'style': _rs()}]
        ]
        send_message(chat_id, render_body_text(deposit_txt), reply_markup={'inline_keyboard': kb})

    elif text == 'Admin Panel' and is_admin(chat_id):
        send_message(chat_id, get_admin_text(), reply_markup=admin_panel_keyboard())
    elif text == 'GET NUMBER':
        all_services, txt, kb = _build_services_keyboard('get_number')
        if not all_services:
            send_message(chat_id, render_body_text(f"{PEM['no']} No numbers or services available!"))
        else:
            send_message(chat_id, txt, reply_markup={'inline_keyboard': kb})
    elif text == 'Search Number':
        user_states[chat_id] = 'wait_for_search'
        c_msg = bot_settings['custom_messages'].get('search_number', {})
        txt = render_body_text(c_msg.get('text', f"{PEM['num']} Search Number"))
        _reset_btn_counter()
        kb = []
        _append_custom_btns(kb, c_msg)
        _add_close_btn(kb)
        send_message(chat_id, txt, reply_markup={'inline_keyboard': kb})

    elif text == 'SUPPORT':
        c_msg = bot_settings['custom_messages'].get('support', {})
        txt = render_body_text(c_msg.get('text', f"{PEM['msg']} Support"))
        if not txt.strip():
            txt = render_body_text(f"{PEM['msg']} Support")
        _reset_btn_counter()
        kb = []
        sup_link = bot_settings.get('support_link', '')
        if sup_link:
            kb.append([{'text': 'Contact Support', 'icon_custom_emoji_id': '5337302974806922068', 'url': sup_link, 'style': _rs()}])
        for b in c_msg.get('buttons', []):
            b_copy = b.copy()
            b_copy['style'] = _rs()
            kb.append([b_copy])
        _add_close_btn(kb)
        send_message(chat_id, txt, reply_markup={'inline_keyboard': kb} if kb else None)

def _build_cc_codes(nums):
    """Build a parallel list of country-code strings for each number in nums."""
    codes = []
    for num in nums:
        _, iso, _ = get_flag_info_from_num(num)
        codes.append(_get_cc_from_iso(iso) or _get_cc_from_num(num))
    return codes

def _rebuild_num_kb(chat_id):
    """Rebuild the number-display inline keyboard from user_active_sessions, honouring cc_state."""
    session = user_active_sessions.get(chat_id, {})
    nums = session.get('nums', [])
    service = session.get('service', '')
    country = session.get('country', '')
    ctx = session.get('ctx', 'regular')
    cc_codes = session.get('cc_codes', [])
    if len(cc_codes) < len(nums):
        cc_codes = _build_cc_codes(nums)
        session['cc_codes'] = cc_codes
    cc_state = session.get('cc_state', [True] * len(nums))
    query = session.get('query', '')
    _reset_btn_counter()
    kb = []
    any_cc_added = False
    has_any_cc = False
    for i, num in enumerate(nums):
        raw = str(num).lstrip('+')
        _, iso, flag_eid = get_flag_info_from_num(raw)
        flag_emoji_id = flag_eid or '5780471598922337683'
        cc = cc_codes[i] if i < len(cc_codes) else None
        added = cc_state[i] if i < len(cc_state) else False
        if cc:
            has_any_cc = True
        if added and cc:
            any_cc_added = True
        local_raw = raw[len(cc):] if cc and raw.startswith(str(cc)) else raw
        if added and cc:
            display_num = f'+{cc}{local_raw}'
        else:
            display_num = local_raw
        kb.append([{'text': display_num, 'icon_custom_emoji_id': flag_emoji_id, 'copy_text': {'text': display_num}, 'style': _rs()}])
    # Always keep the country-code toggle visible whenever numbers have a detectable country code.
    if has_any_cc:
        if any_cc_added:
            kb.append([{'text': 'Remove Country Code', 'icon_custom_emoji_id': '6206108815075579644', 'callback_data': 'rem_cc_all', 'style': _rs()}])
        else:
            kb.append([{'text': 'Add Country Code', 'icon_custom_emoji_id': '6206375377925839184', 'callback_data': 'add_cc_all', 'style': _rs()}])
    if ctx == 'regular':
        change_cb = f'c_n_{service}_{country}'
        c_msg_key = 'get_number'
        last_btn_meta = {'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'g_s_{service}'}
    else:
        change_cb = f"c_n_s_{query}_{service or ''}"
        c_msg_key = 'search_number'
        last_btn_meta = {'text': 'Close', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': 'close_msg'}
    kb.append([{'text': 'Change Number', 'icon_custom_emoji_id': '6264896248659056036', 'callback_data': change_cb, 'style': _rs()}, {'text': 'OTP Group', 'icon_custom_emoji_id': '5190447043545438788', 'url': bot_settings.get('otp_link', ''), 'style': _rs()}])
    _append_custom_btns(kb, bot_settings['custom_messages'].get(c_msg_key, {}))
    last_btn = {**last_btn_meta, 'style': _rs()}
    kb.append([last_btn])
    return kb

def _get_country_batch_rate(service, country):
    """Service rate for Nexa/VoltX/Stex is controlled by Global OTP Reward."""
    try:
        return float(bot_settings.get('otp_reward', 0.0) or 0.0)
    except (TypeError, ValueError):
        return 0.0

def _format_rate(rate):
    try:
        return f'{float(rate):g}'
    except (TypeError, ValueError):
        return '0'

def _get_manual_batch_rate(number):
    clean = str(number).replace('+', '').replace(' ', '').replace('-', '').strip()
    for b_data in number_batches.values():
        for n_obj in b_data.get('numbers', []):
            stored = str(n_obj.get('num', '')).replace('+', '').replace(' ', '').replace('-', '').strip()
            if stored == clean:
                return b_data.get('rate', 0.0)
    return 0.0

def _get_session_rate(chat_id, number=None):
    """Single global rate shown everywhere: OTP Reward."""
    try:
        return float(bot_settings.get('otp_reward', 0.0) or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _get_effective_otp_reward(owner_id, number):
    """Return the single global OTP Reward for every OTP, everywhere."""
    try:
        return float(bot_settings.get('otp_reward', 0.0) or 0.0)
    except (TypeError, ValueError):
        return 0.0

def _build_num_text(chat_id):
    """Build the number waiting text box.

    Layout requested by user:
        🇪🇬 Egypt ⭐ Number
        ➖➖➖➖➖➖➖➖➖➖
        ⏳ WAITING FOR OTP.... 

    The actual phone numbers are NOT displayed in the text. They remain
    copyable inline buttons underneath the text box.
    """
    session = user_active_sessions.get(chat_id, {})
    nums = session.get('nums', [])
    if not nums:
        return '<tg-emoji emoji-id="5807903945883917416">⏳</tg-emoji> <i>Waiting for Number...</i>'
    raw = str(nums[0]).replace('+', '').replace(' ', '').strip()
    _, iso, _ = get_flag_info_from_num(raw)
    country_name = _country_full_name_from_iso(iso) if iso else 'Unknown'
    flag_html = get_flag_info_html(raw)
    service_name = str(session.get('service', '')).strip()
    app_full_name, service_logo = get_service_info_html(service_name) if service_name else ('Number', '⭐')
    return f'<b>{flag_html} {country_name} {service_logo} {app_full_name}</b>\n➖➖➖➖➖➖➖➖➖➖\n<tg-emoji emoji-id="5807903945883917416">⏳</tg-emoji> <i>WAITING FOR OTP...</i>  💰 {_get_session_rate(chat_id, nums[0] if nums else None):.2f}৳'

def expire_previous_number(chat_id):
    if chat_id in user_active_sessions:
        prev_data = user_active_sessions[chat_id]
        prev_msg_id = prev_data['msg_id']
        nums = prev_data['nums']
        for num in nums:
            if num in nexa_assigned_numbers:
                del nexa_assigned_numbers[num]
            if num in voltx_assigned_numbers:
                del voltx_assigned_numbers[num]
            if num in stex_assigned_numbers:
                del stex_assigned_numbers[num]
        save_local_db()
        try:
            edit_message(chat_id, prev_msg_id, '<tg-emoji emoji-id="5807903945883917416">⏳</tg-emoji> <b>Change Number</b>', reply_markup={'inline_keyboard': []})
        except Exception as e:
            logger.warning(f'Error expiring number message: {e}')
        del user_active_sessions[chat_id]
        user_otp_delivery_active[chat_id] = False

def _show_getting_numbers_loading(chat_id, msg_id):
    """Loading animation disabled for faster Get/Change Number response."""
    return

def handle_callback(call):
    try:
        _handle_callback_inner(call)
    except Exception as e:
        try:
            answer_callback(call.get('id', ''), f'⚠️ Error: {str(e)[:40]}')
        except Exception as answer_err:
            logger.warning(f'Error: {answer_err}')
        logger.warning(f"Callback error ({call.get('data', '')}): {e}")

def _safe_int(val, default=-1):
    """Safe int conversion — returns default on error."""
    try:
        return int(val)
    except (ValueError, IndexError, TypeError):
        return default

def _td(chat_id, key, default=None):
    """Safe temp_data access — returns default if missing."""
    return temp_data.get(chat_id, {}).get(key, default)

def _td_has(chat_id, *keys):
    """Check temp_data has chat_id and all given keys."""
    d = temp_data.get(chat_id, {})
    return all((k in d for k in keys))

def _admin_flow_prompt(chat_id, text, reply_markup=None, msg_id=None):
    """Edit the active Admin Panel flow message instead of creating a new bubble.
    Falls back to send_message only if the original admin message is unavailable.
    """
    if msg_id is None:
        msg_id = _td(chat_id, 'msg_id')
    rendered = render_body_text(text)
    if msg_id:
        try:
            edit_message(chat_id, msg_id, rendered, reply_markup=reply_markup)
            return msg_id
        except Exception:
            pass
    send_message(chat_id, rendered, reply_markup=reply_markup)
    return None

def _set_admin_flow(chat_id, msg_id, state, **extra):
    """Keep one message/state context for every Admin Panel multi-step flow."""
    d = temp_data.setdefault(chat_id, {})
    d['msg_id'] = msg_id
    d.update(extra)
    user_states[chat_id] = state

def _handle_callback_inner(call):
    global total_assigned_stats
    chat_id = call['message']['chat']['id']
    chat_type = call['message']['chat'].get('type', 'private')
    data = call.get('data', '')
    # Informational buttons must still acknowledge the callback so Telegram
    # does not leave the loading spinner running.
    if data == 'ignore':
        try:
            answer_callback(call.get('id', ''))
        except Exception:
            pass
        return
    _skip_auto_answer = call.get('id') == 'internal' or data.startswith(('test_p_conn_', 'c_n_', 'g_c_')) or data in {'toggle_nexa', 'toggle_voltx', 'toggle_stex', 'check_fj'} or data.startswith(('del_b_', 'del_nxa_', 'del_sc_', 'del_vxsc_', 'del_vx_', 'del_stxsc_', 'del_stx_', 'del_adm_', 'del_fwbtn_', 'del_fw_', 'del_2fa_', 'del_fj_', 'del_wm_', 'nx_dr_', 'vx_dr_', 'stx_dr_', 'wapp_', 'wrej_', 'dapp_', 'drej_'))
    if not _skip_auto_answer:
        try:
            threading.Thread(target=answer_callback, args=(call['id'],)).start()
        except Exception as e:
            logger.warning(f'Error: {e}')
    if chat_type != 'private' and (not (data.startswith('wapp_') or data.startswith('wrej_'))):
        return
    msg_id = call['message']['message_id']
    if is_admin(chat_id):
        temp_data.setdefault(chat_id, {})['msg_id'] = msg_id
    if chat_type == 'private':
        if is_user_banned(chat_id):
            answer_callback(call['id'], '🚫 You are banned from using this bot!', show_alert=True)
            return
        if not check_force_join(chat_id) and data != 'check_fj':
            send_force_join_msg(chat_id)
            return
    if data == 'check_fj':
        if check_force_join(chat_id):
            answer_callback(call['id'], '✅ Verified! Starting...')
            delete_message(chat_id, msg_id)
            first_name = call.get('from', {}).get('first_name', 'User')
            _welcome_user(chat_id, first_name)
        else:
            answer_callback(call['id'], "❌ You haven't joined all channels yet!", show_alert=True)
        return
    if data == 'dep_paid_start':
        answer_callback(call['id'])
        user_states[chat_id] = 'wait_for_deposit_amount'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('💰 <b>DEPOSIT</b>\n\n📝 Enter the amount you paid (in ৳):\n\n💡 Minimum: <b>50৳</b>'), reply_markup=get_cancel_kb())
        return
        
    if data == 'close_msg':
        if chat_id in user_states:
            user_states.pop(chat_id, None)
        if chat_id in temp_data:
            temp_data.pop(chat_id, None)
        answer_callback(call['id'])
        delete_message(chat_id, msg_id)
        send_message(chat_id, render_body_text(f"{PEM['hi']} Main Menu:"), reply_markup=main_menu(chat_id))
        
    elif data == "cancel_2fa":
        # Back must return to the 2FA key-entry screen in the same message.
        user_states[chat_id] = "wait_for_2fa_key"
        temp_data[chat_id] = {"msg_id": msg_id, "2fa_name": "My 2FA"}
        _show_2fa_key_input(chat_id, msg_id)
        answer_callback(call["id"])
    elif data == 'back_to_2fa_name':
        user_states[chat_id] = 'wait_for_2fa_name'
        prev_msg = temp_data.get(chat_id, {}).get('msg_id', msg_id)
        temp_data[chat_id] = {'msg_id': prev_msg}
        _show_2fa_name_input(chat_id, msg_id)
        answer_callback(call['id'])

    elif data == "gen_2fa":
        user_states[chat_id] = "wait_for_2fa_key"
        temp_data[chat_id] = {"msg_id": msg_id, "2fa_name": "My 2FA"}
        _show_2fa_key_input(chat_id, msg_id)
        answer_callback(call["id"])

    elif data.startswith("ref_2fa_"):
        secret = data.replace("ref_2fa_", "")
        try:
            # Acknowledge immediately, then briefly show a loading state so the
            # Refresh tap has visible feedback before the newly generated code appears.
            answer_callback(call["id"])
            edit_message(
                chat_id,
                msg_id,
                render_body_text(_build_2fa_refresh_txt("", 0)),
                reply_markup={"inline_keyboard": _build_2fa_code_kb("", secret)},
            )
            time.sleep(0.45)

            totp = pyotp.TOTP(secret)
            code = totp.now()
            remaining_time = 30 - (int(time.time()) % 30)
            entry_name = next((e["name"] for e in user_2fa_saved.get(chat_id, []) if e["key"] == secret), "My Account")
            success_txt = _build_2fa_code_txt(entry_name, code, remaining_time)
            kb = _build_2fa_code_kb(code, secret)
            edit_message(chat_id, msg_id, render_body_text(success_txt), reply_markup={"inline_keyboard": kb})
        except Exception as e:
            logger.warning(f"2FA refresh error: {e}")
            answer_callback(call["id"], "Error refreshing code!", show_alert=True)
    elif data.startswith('how_2fa_'):
        secret = data.replace('how_2fa_', '')
        cur_text = call['message'].get('text', call['message'].get('caption', ''))
        m = re.search('CODE:\\s*([0-9]{4,8})', cur_text)
        code = m.group(1) if m else '------'
        entry_name = next((e['name'] for e in user_2fa_saved.get(chat_id, []) if e['key'] == secret), 'My Account')
        guide_txt = f'➖➖➖➖➖➖➖➖➖➖➖➖\n《 🔑 <b>HOW TO USE A 2FA CODE?</b> 》\n➖➖➖➖➖➖➖➖➖➖➖➖\n📛 <b>Account:</b> {entry_name}\n🔐 <b>Current Code:</b> <code>{code}</code>\n➖➖➖➖➖➖➖➖➖➖➖➖\n<b>Step-by-Step Guide:</b>\n➖➖➖➖➖➖➖➖➖➖➖➖\n1️⃣ <b>Open the app/website</b> where you want to log in.\n   (Instagram, Facebook, Gmail, etc.)\n➖➖➖➖➖➖➖➖➖➖➖➖\n2️⃣ <b>Enter your Email + Password</b> to log in.\n➖➖➖➖➖➖➖➖➖➖➖➖\n3️⃣ A screen will appear after login:\n   <i>"Enter your 6-digit code" or</i>\n   <i>"Go to your authentication app"</i>\n➖➖➖➖➖➖➖➖➖➖➖➖\n4️⃣ <b>Paste the above code</b> into the code box:\n   <tg-emoji emoji-id="5416117059207572332">👉</tg-emoji> <code>{code}</code>\n➖➖➖➖➖➖➖➖➖➖➖➖\n5️⃣ Press the <b>Continue / Verify</b> button ✅\n➖➖➖➖➖➖➖➖➖➖➖➖\n⚠️ <b>Important:</b> This code is valid for only <b>30 seconds</b>!\nIf the code expires, press the <b>Refresh</b> button to get a new code.\n➖➖➖➖➖➖➖➖➖➖➖➖\n💾 <b>For recovery:</b> Go to "MY 2FA ADDED"\nYour Secret Key is saved — you can generate a code anytime.\n➖➖➖➖➖➖➖➖➖➖➖➖'
        _reset_btn_counter()
        guide_kb = {'inline_keyboard': [[{'text': 'Click to copy', 'icon_custom_emoji_id': '5353022963132174959', 'copy_text': {'text': code}, 'style': _rs()}], [{'text': 'MY 2FA ADDED', 'icon_custom_emoji_id': '5337255927735163754', 'callback_data': 'my_2fa_list', 'style': _rs()}], [{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'ref_2fa_{secret}', 'style': _rs()}]]}
        edit_message(chat_id, msg_id, render_body_text(guide_txt), reply_markup=guide_kb)
        try:
            answer_callback(call['id'])
        except Exception as e:
            logger.warning(f'Error: {e}')
    elif data == 'my_2fa_list':
        _show_2fa_list(chat_id, msg_id)
        try:
            answer_callback(call['id'])
        except Exception as e:
            logger.warning(f'Error: {e}')
    elif data.startswith('gen_saved_2fa_'):
        try:
            idx = int(data.replace('gen_saved_2fa_', ''))
            saved = user_2fa_saved.get(chat_id, [])
            if idx < 0 or idx >= len(saved):
                answer_callback(call['id'], '❌ Entry not found!', show_alert=True)
                return
            entry = saved[idx]
            secret = entry['key']
            entry_name = entry['name']
            totp = pyotp.TOTP(secret)
            code = totp.now()
            remaining_time = 30 - int(time.time()) % 30
            success_txt = _build_2fa_code_txt(entry_name, code, remaining_time)
            kb = _build_2fa_code_kb(code, secret)
            edit_message(chat_id, msg_id, render_body_text(success_txt), reply_markup={'inline_keyboard': kb})
            try:
                answer_callback(call['id'])
            except Exception as e:
                logger.warning(f'Error: {e}')
        except Exception as e:
            answer_callback(call['id'], '❌ Error generating code!', show_alert=True)
    elif data.startswith('del_2fa_'):
        try:
            idx = int(data.replace('del_2fa_', ''))
            saved = user_2fa_saved.get(chat_id, [])
            if idx < 0 or idx >= len(saved):
                answer_callback(call['id'], '❌ Entry not found!', show_alert=True)
                return
            del_name = saved[idx]['name']
            user_2fa_saved[chat_id].pop(idx)
            _save_2fa_saved()
            answer_callback(call['id'], f"🗑 '{del_name}' has been deleted!", show_alert=True)
            _show_2fa_list(chat_id, msg_id)
        except Exception as e:
            answer_callback(call['id'], '❌ Error!', show_alert=True)
    elif data == 'cancel_abhi_edit':
        if chat_id in user_states:
            user_states.pop(chat_id, None)
        if chat_id in temp_data:
            temp_data.pop(chat_id, None)
        _show_abhi_panel(chat_id, msg_id)
    elif data == 'dummy_alert':
        answer_callback(call['id'], 'This feature will be added later!', show_alert=True)
    elif data == 'refresh_traffic':
        # IMPORTANT: Refresh must ONLY edit the existing LIVE TRAFFIC message.
        # Never send a new message and never delete the current one.
        try:
            txt, markup = build_traffic_ui()
            edit_message(chat_id, msg_id, txt, reply_markup=markup)
            answer_callback(call['id'], '✅ Traffic Refreshed!', show_alert=False)
        except Exception as e:
            logger.warning(f'LIVE TRAFFIC refresh edit failed: {e}')
            # Do not fall back to sendMessage: that would create a new chat message.
            answer_callback(call['id'], '❌ Refresh failed. Please try again.', show_alert=True)
    elif data.startswith('exp_rng_'):
        srv_query = data.replace('exp_rng_', '')
        country_stats = {}
        current_time = time.time()
        with _traffic_lock:
            traffic_snapshot = list(recent_traffic)
        for t in traffic_snapshot:
            if current_time - t.get('time', 0) <= 3600:
                if t.get('service', '').startswith(srv_query):
                    iso = t.get('iso', 'XX')
                    flag = t.get('flag', '🌍')
                    if iso not in country_stats:
                        country_stats[iso] = {'count': 0, 'flag': flag}
                    country_stats[iso]['count'] += 1
        if not country_stats:
            answer_callback(call['id'], '❌ No recent traffic found for this service!', show_alert=True)
            return
        _reset_btn_counter()
        kb = []
        for iso, c_data in sorted(country_stats.items(), key=lambda x: x[1]['count'], reverse=True):
            count = c_data['count']
            c_name = iso
            emoji_id = '5780471598922337683'
            for code, fdata in bot_settings.get('premium_flags', {}).items():
                if fdata.get('iso') == iso:
                    c_name = fdata.get('name', iso)
                    if 'id' in fdata:
                        emoji_id = fdata['id']
                    break
            btn_text = f'{c_name} ({iso}) - {count} OTP'
            kb.append([{'text': btn_text, 'icon_custom_emoji_id': emoji_id, 'callback_data': f'exp_c_{srv_query}_{iso}', 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'refresh_traffic', 'style': _rs()}])
        app_full_name, prem_app_html = get_service_info_html(srv_query)
        edit_message(chat_id, msg_id, render_body_text(f'📊 <b>Explore  {prem_app_html} {app_full_name}</b>\n\nSelect a country to view available ranges:'), reply_markup={'inline_keyboard': kb})
        answer_callback(call['id'])
    elif data.startswith('exp_c_'):
        _sfx = data[len('exp_c_'):]
        srv_query, _, iso_query = _sfx.rpartition('_')
        nums = []
        current_time = time.time()
        with _traffic_lock:
            traffic_snapshot = list(recent_traffic)
        for t in traffic_snapshot:
            if current_time - t.get('time', 0) <= 3600:
                if t.get('service', '').startswith(srv_query) and t.get('iso') == iso_query:
                    num = t.get('number', '').replace('+', '').strip()
                    if num:
                        nums.append(num)
        if not nums:
            answer_callback(call['id'], '❌ No recent numbers found for this country!', show_alert=True)
            return
        known_ranges = set()
        for s_name, c_dict in bot_settings.get('nexa_services', {}).items():
            for c_name, r_list in c_dict.items():
                for r in r_list:
                    known_ranges.add(r)
        sorted_known = sorted(list(known_ranges), key=len, reverse=True)
        r_counts = Counter()
        for num in nums:
            matched = False
            for r in sorted_known:
                if num.startswith(r):
                    r_counts[r] += 1
                    matched = True
                    break
            if not matched:
                if len(num) >= 7:
                    r_counts[num[:7]] += 1
                else:
                    r_counts[num] += 1
        r_list = r_counts.most_common(12)
        _reset_btn_counter()
        kb = []
        for r, count in r_list:
            kb.append([{'text': f'{r} ({count})', 'icon_custom_emoji_id': '5352862640592949843', 'copy_text': {'text': r}, 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'exp_rng_{srv_query}', 'style': _rs()}])
        app_full_name, prem_app_html = get_service_info_html(srv_query)
        prem_flag_html = get_flag_info_html(iso_query)
        edit_message(chat_id, msg_id, render_body_text(f'📊 <b>Ranges for {prem_app_html} {app_full_name} - {prem_flag_html} {iso_query}</b>\n\nClick on any range to copy it.'), reply_markup={'inline_keyboard': kb})
        answer_callback(call['id'])
    elif data == 'user_management':
        edit_message(chat_id, msg_id, get_user_management_text(), reply_markup=user_management_keyboard())
    elif data == 'um_manage_balance':
        user_states[chat_id] = 'wait_for_um_bal_uid'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Send the User ID to Manage Balance:'), reply_markup=get_cancel_kb())
    elif data == 'um_ban_unban':
        user_states[chat_id] = 'wait_for_um_ban_uid'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Send the User ID to Ban or Unban:'), reply_markup=get_cancel_kb())
    elif data == 'um_user_profile':
        user_states[chat_id] = 'wait_for_um_prof_uid'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Send the User ID to View Profile:'), reply_markup=get_cancel_kb())
    elif data == 'menu_design_list':
        edit_message(chat_id, msg_id, render_body_text(f'🎨 <b>Menu Design Editor</b>\n\nSelect a menu block to edit its Body Text and Inline Buttons. You can use Premium Emojis too!'), reply_markup=menu_design_list_keyboard())
    elif data == 'md_reset_defaults':
        bot_settings['custom_messages'] = DEFAULT_CUSTOM_MESSAGES.copy()
        save_local_db()
        answer_callback(call['id'], '✅ Resetted to Premium Defaults!', show_alert=True)
    elif data.startswith('md_edit_'):
        answer_callback(call['id'])
        if chat_id in user_states:
            user_states.pop(chat_id, None)
        if chat_id in temp_data:
            temp_data.pop(chat_id, None)
        key = data.replace('md_edit_', '')
        cm_text = render_body_text(bot_settings['custom_messages'].get(key, {}).get('text', '...'))
        try:
            edit_message(chat_id, msg_id, render_body_text(f'🎨 <b>Editing: {key.upper()}</b>\n\nPreview of current Text:\n{cm_text}'), reply_markup=menu_edit_options_keyboard(key))
        except Exception as e:
            logger.warning(f'Error: {e}')
    elif data.startswith('md_text_'):
        key = data.replace('md_text_', '')
        user_states[chat_id] = 'wait_for_menu_text'
        temp_data[chat_id] = {'msg_id': msg_id, 'menu_key': key}
        edit_message(chat_id, msg_id, render_body_text(f'📝 <b>Edit Body: {key.upper()}</b>\n\nSend the new text. You can use Premium Emojis directly here.\n(Use standard HTML like <b>bold</b>, <i>italic</i> for formatting)'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'md_edit_{key}', 'style': _rs()}]]})
    elif data.startswith('md_btns_'):
        answer_callback(call['id'])
        if chat_id in user_states:
            user_states.pop(chat_id, None)
        if chat_id in temp_data:
            temp_data.pop(chat_id, None)
        key = data.replace('md_btns_', '')
        try:
            edit_message(chat_id, msg_id, render_body_text(f'⚙️ <b>Edit Inline Buttons: {key.upper()}</b>'), reply_markup=menu_buttons_list_keyboard(key))
        except Exception as e:
            logger.warning(f'Error: {e}')
    elif data.startswith('md_addbtn_'):
        key = data.replace('md_addbtn_', '')
        user_states[chat_id] = 'wait_for_menu_btn'
        temp_data[chat_id] = {'msg_id': msg_id, 'menu_key': key}
        edit_message(chat_id, msg_id, render_body_text(f'➕ <b>Add Button: {key.upper()}</b>\n\nSend custom button in this format:\n<code>Button Text - https://link.com</code>\n\n<i>(Only normal Emojis supported here!)</i>'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'md_btns_{key}', 'style': _rs()}]]})
    elif data.startswith('md_delbtn_'):
        after_prefix = data[len('md_delbtn_'):]
        key, b_idx_str = after_prefix.rsplit('_', 1)
        b_idx = int(b_idx_str)
        if key in bot_settings['custom_messages'] and b_idx < len(bot_settings['custom_messages'][key].get('buttons', [])):
            del bot_settings['custom_messages'][key]['buttons'][b_idx]
            save_local_db()
            answer_callback(call['id'], '✅ Button Deleted!', show_alert=True)
            edit_message(chat_id, msg_id, render_body_text(f'⚙️ <b>Edit Inline Buttons: {key.upper()}</b>'), reply_markup=menu_buttons_list_keyboard(key))
        else:
            answer_callback(call['id'], '❌ Button not found!', show_alert=True)
    elif data == 'balance_refer':
        u_data = get_user(chat_id)
        ref_link = f"https://t.me/{BOT_USERNAME.lstrip('@').strip()}?start={chat_id}"
        c_msg = bot_settings['custom_messages'].get('refer', {})
        raw_txt = c_msg.get('text', f"{PEM['gift']} Refer").replace('{ref_link}', ref_link).replace('{total_ref}', str(u_data.get('total_refers', 0))).replace('{ref_reward}', str(bot_settings['refer_reward']))
        txt = render_body_text(raw_txt)
        _reset_btn_counter()
        kb = [[{'text': 'COPY LINK', 'icon_custom_emoji_id': '5192739271886282680', 'copy_text': {'text': ref_link}, 'style': 'primary'}]]
        _append_custom_btns(kb, c_msg)
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'back_to_balance', 'style': 'danger'}])
        edit_message(chat_id, msg_id, txt, reply_markup={'inline_keyboard': kb})
        answer_callback(call['id'])
    elif data == 'balance_support':
        c_msg = bot_settings['custom_messages'].get('support', {})
        txt = render_body_text(c_msg.get('text', f"{PEM['msg']} Support"))
        sup_link = bot_settings.get('support_link', '')
        kb = []
        if sup_link:
            kb.append([{'text': 'Contact Support', 'icon_custom_emoji_id': '5337302974806922068', 'url': sup_link, 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'back_to_balance', 'style': _rs()}])
        edit_message(chat_id, msg_id, txt, reply_markup={'inline_keyboard': kb})
    elif data == 'balance_withdrawal':
        if not bot_settings['withdraw_on']:
            send_message(chat_id, render_body_text(f"{PEM['no']} Withdrawals are currently disabled."))
            answer_callback(call['id'])
            return
        u_data = get_user(chat_id)
        bal = u_data.get('balance', 0.0)
        c_msg = bot_settings['custom_messages'].get('withdrawal', {})
        raw_txt = c_msg.get('text', DEFAULT_CUSTOM_MESSAGES['withdrawal']['text']).replace('{bal}', str(bal)).replace('{total_otp}', str(u_data.get('total_otps', 0))).replace('{total_ref}', str(u_data.get('total_refers', 0))).replace('{min_w}', str(bot_settings['min_withdraw']))
        txt = render_body_text(raw_txt)
        _reset_btn_counter()
        kb = []
        for m in bot_settings['w_methods']:
            kb.append([{'text': m.strip(), 'icon_custom_emoji_id': '5190899075968441286', 'callback_data': f'sel_wm_{m.strip()}', 'style': 'primary'}])
        _append_custom_btns(kb, c_msg)
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'back_to_balance', 'style': 'danger'}])
        edit_message(chat_id, msg_id, txt, reply_markup={'inline_keyboard': kb})
        answer_callback(call['id'])
    elif data == 'back_to_balance':
        u_data = get_user(chat_id)
        bal = u_data.get('balance', 0.0)
        c_msg = bot_settings['custom_messages'].get('balance', DEFAULT_CUSTOM_MESSAGES['balance'])
        raw_txt = c_msg.get('text', DEFAULT_CUSTOM_MESSAGES['balance']['text']).replace('{bal}', str(bal)).replace('{total_otp}', str(u_data.get('total_otps', 0))).replace('{total_ref}', str(u_data.get('total_refers', 0))).replace('{min_w}', str(bot_settings.get('min_withdraw', 30.0)))
        kb = [[{'text': 'WITHDRAWAL', 'icon_custom_emoji_id': '5352585194295564660', 'callback_data': 'balance_withdrawal', 'style': 'primary'}], [{'text': 'CLOSE', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': 'close_msg', 'style': 'danger'}]]
        edit_message(chat_id, msg_id, render_body_text(raw_txt), reply_markup={'inline_keyboard': kb})
        answer_callback(call['id'])
    elif data.startswith('sel_wm_'):
        method = data.replace('sel_wm_', '')
        bal = get_user(chat_id).get('balance', 0.0)
        min_w = bot_settings.get('min_withdraw', 30.0)
        if bal < min_w:
            answer_callback(call['id'], f'❌ Insufficient balance!\nMinimum {min_w}৳ required.\nYour balance: {bal}৳', show_alert=True)
            return
        answer_callback(call['id'], f'💳 Method: {method} selected!\n💰 Balance: {bal}৳\n\nNow enter the amount below.', show_alert=True)
        temp_data[chat_id] = {'method': method, 'balance': bal, 'msg_id': msg_id}
        user_states[chat_id] = 'wait_for_withdraw_amount'
        amount_kb = {'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'back_to_withdrawal', 'style': 'danger'}, {'text': 'CLOSE', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': 'close_msg', 'style': 'danger'}]]}
        try:
            edit_message(chat_id, msg_id, render_body_text(f'💳 Method: <b>{method}</b>\n💰 Available Balance: <b>{bal}৳</b>\n\n📝 Enter the amount you want to withdraw (Min: {min_w}৳):'), reply_markup=amount_kb)
        except Exception as e:
            send_message(chat_id, render_body_text(f'💳 Method: <b>{method}</b>\n💰 Available Balance: <b>{bal}৳</b>\n\n📝 Enter the amount you want to withdraw (Min: {min_w}৳):'), reply_markup=amount_kb)
    elif data == 'back_to_withdrawal':
        u_data = get_user(chat_id)
        bal = u_data.get('balance', 0.0)
        c_msg = bot_settings['custom_messages'].get('withdrawal', DEFAULT_CUSTOM_MESSAGES['withdrawal'])
        raw_txt = c_msg.get('text', DEFAULT_CUSTOM_MESSAGES['withdrawal']['text']).replace('{bal}', str(bal)).replace('{total_otp}', str(u_data.get('total_otps', 0))).replace('{total_ref}', str(u_data.get('total_refers', 0))).replace('{min_w}', str(bot_settings.get('min_withdraw', 30.0)))
        kb = []
        for m in bot_settings.get('w_methods', []):
            kb.append([{'text': m.strip(), 'icon_custom_emoji_id': '5190899075968441286', 'callback_data': f'sel_wm_{m.strip()}', 'style': 'primary'}])
        _append_custom_btns(kb, c_msg)
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'back_to_balance', 'style': 'danger'}, {'text': 'CLOSE', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': 'close_msg', 'style': 'danger'}])
        edit_message(chat_id, msg_id, render_body_text(raw_txt), reply_markup={'inline_keyboard': kb})
        answer_callback(call['id'])
    elif data == 'manage_emojis':
        edit_message(chat_id, msg_id, render_body_text(f"{PEM['star']} <b>Premium Emoji Management</b>\n\nSelect a category below:"), reply_markup=emoji_settings_keyboard())
    elif data == 'emoji_upload_menu':
        edit_message(chat_id, msg_id, render_body_text(f'📤 <b>All Uploading System</b>\n\nSelect what you want to upload:'), reply_markup=emoji_upload_keyboard())
    elif data == 'emoji_delete_menu':
        edit_message(chat_id, msg_id, render_body_text(f'🗑 <b>All Deleting System</b>\n\nSelect what you want to delete:'), reply_markup=emoji_delete_keyboard())
    elif data == 'emoji_download_menu':
        edit_message(chat_id, msg_id, render_body_text(f'📥 <b>All Downloading System</b>\n\nSelect what you want to download:'), reply_markup=emoji_download_keyboard())
    elif data == 'up_flags_txt':
        user_states[chat_id] = 'wait_for_flag_txt'
        edit_message(chat_id, msg_id, render_body_text('📂 Please upload the <b>Flag Emojis</b> <code>.txt</code> file.'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'emoji_upload_menu', 'style': _rs()}]]})
    elif data == 'up_apps_txt':
        user_states[chat_id] = 'wait_for_app_txt'
        edit_message(chat_id, msg_id, render_body_text('📂 Please upload the <b>Service Apps</b> <code>.txt</code> file.'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'emoji_upload_menu', 'style': _rs()}]]})
    elif data == 'dl_flags_txt':
        content = generate_emoji_txt('flags')
        if content:
            send_document(chat_id, 'Flag_Emojis.txt', content)
            answer_callback(call['id'], '✅ Downloaded!')
        else:
            answer_callback(call['id'], '❌ No Flag Emojis found!', show_alert=True)
    elif data == 'dl_apps_txt':
        content = generate_emoji_txt('apps')
        if content:
            send_document(chat_id, 'Service_Apps.txt', content)
            answer_callback(call['id'], '✅ Downloaded!')
        else:
            answer_callback(call['id'], '❌ No App Emojis found!', show_alert=True)
    elif data == 'del_all_flags':
        bot_settings['premium_flags'] = {}
        save_local_db()
        answer_callback(call['id'], '✅ All Premium Flags Deleted Successfully!', show_alert=True)
        edit_message(chat_id, msg_id, render_body_text(f'🗑 <b>All Deleting System</b>\n\nSelect what you want to delete:'), reply_markup=emoji_delete_keyboard())
    elif data == 'del_all_apps':
        bot_settings['premium_apps'] = {}
        save_local_db()
        answer_callback(call['id'], '✅ All Service Emojis Deleted Successfully!', show_alert=True)
        edit_message(chat_id, msg_id, render_body_text(f'🗑 <b>All Deleting System</b>\n\nSelect what you want to delete:'), reply_markup=emoji_delete_keyboard())
    elif data == 'all_system_emoji':
        overrides = bot_settings.get('sys_emoji_overrides', {})
        edit_message(chat_id, msg_id, render_body_text(f"{PEM['star']} <b>All System Emoji</b>\n\n{PEM['admin']} Button emojis: <b>{len(_SYS_BTN_EMOJIS)}</b>\n{PEM['msg']} Message emojis: <b>{len(_SYS_MSG_EMOJIS)}</b>\n{PEM['gear']} Overrides active: <b>{len(overrides)}</b>\n\nSelect a category to browse and replace emojis:"), reply_markup=_all_system_emoji_keyboard())
    elif data == 'dl_system_emoji':
        content = _generate_sys_emoji_txt()
        send_document(chat_id, 'System_Emojis.txt', content)
        answer_callback(call['id'], 'System Emoji file downloaded!')
    elif data.startswith('btn_emoji_page_'):
        page = _safe_int(data.replace('btn_emoji_page_', ''), 0)
        total = len(_SYS_BTN_EMOJIS)
        pages = max(1, (total + _SYS_EMJ_PAGE_SIZE - 1) // _SYS_EMJ_PAGE_SIZE)
        page = max(0, min(page, pages - 1))
        edit_message(chat_id, msg_id, render_body_text(f"{PEM['gear']} <b>Button Emojis</b> — Page {page + 1}/{pages}\n\nEach row shows the button emoji icon + name.\nTap <b>Replace</b> to change an emoji ID."), reply_markup=_sys_btn_emoji_page_keyboard(page))
    elif data.startswith('msg_emoji_page_'):
        page = _safe_int(data.replace('msg_emoji_page_', ''), 0)
        total = len(_SYS_MSG_EMOJIS)
        pages = max(1, (total + _SYS_EMJ_PAGE_SIZE - 1) // _SYS_EMJ_PAGE_SIZE)
        page = max(0, min(page, pages - 1))
        edit_message(chat_id, msg_id, render_body_text(f"{PEM['msg']} <b>Message Emojis</b> — Page {page + 1}/{pages}\n\nCovers PEM dict, GLOBAL_BODY_EMOJIS, and hardcoded tg-emoji.\nTap <b>Replace</b> to change an emoji ID."), reply_markup=_sys_msg_emoji_page_keyboard(page))
    elif data.startswith('rm_btn_emoji_'):
        idx = _safe_int(data.replace('rm_btn_emoji_', ''))
        if 0 <= idx < len(_SYS_BTN_EMOJIS):
            btn_text, orig_id = _SYS_BTN_EMOJIS[idx]
            overrides = bot_settings.get('sys_emoji_overrides', {})
            cur_id = overrides.get(f'btn_{idx}', orig_id)
            user_states[chat_id] = 'wait_for_new_btn_emoji_id'
            temp_data[chat_id] = {'orig_id': orig_id, 'cur_id': cur_id, 'label': btn_text, 'kind': 'btn', 'idx': idx, 'msg_id': msg_id}
            edit_message(chat_id, msg_id, render_body_text(f"{PEM['gear']} <b>Replace Button Emoji</b>\n\nButton: <b>{btn_text}</b>\nCurrent ID: <code>{cur_id}</code>\n\n{PEM['upload']} Send the <b>new emoji ID</b> (numbers only, e.g. <code>5352552689983067014</code>):"), reply_markup={'inline_keyboard': [[{'text': 'Cancel', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'btn_emoji_page_{idx // _SYS_EMJ_PAGE_SIZE}', 'style': _rs()}]]})
        else:
            answer_callback(call['id'], 'Index out of range!', show_alert=True)
    elif data.startswith('rm_msg_emoji_'):
        idx = _safe_int(data.replace('rm_msg_emoji_', ''))
        if 0 <= idx < len(_SYS_MSG_EMOJIS):
            label, orig_id, char, usage = _SYS_MSG_EMOJIS[idx]
            overrides = bot_settings.get('sys_emoji_overrides', {})
            cur_id = overrides.get(f'msg_{idx}', orig_id)
            user_states[chat_id] = 'wait_for_new_msg_emoji_id'
            temp_data[chat_id] = {'orig_id': orig_id, 'cur_id': cur_id, 'label': label, 'char': char, 'kind': 'msg', 'idx': idx, 'msg_id': msg_id}
            edit_message(chat_id, msg_id, render_body_text(f"{PEM['msg']} <b>Replace Message Emoji</b>\n\nKey: <b>{usage}</b>\nCurrent ID: <code>{cur_id}</code>\n\n{PEM['upload']} Send the <b>new emoji ID</b> (numbers only, e.g. <code>5352552689983067014</code>):"), reply_markup={'inline_keyboard': [[{'text': 'Cancel', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'msg_emoji_page_{idx // _SYS_EMJ_PAGE_SIZE}', 'style': _rs()}]]})
        else:
            answer_callback(call['id'], 'Index out of range!', show_alert=True)
    elif data == 'broadcast_msg':
        user_states[chat_id] = 'wait_for_broadcast'
        edit_message(chat_id, msg_id, render_body_text('📢 <b>Broadcast Mode</b>\n\nSend the message you want to broadcast (Text, Photo, Video, File etc).'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'back_to_admin', 'style': _rs()}]]})
    elif data == 'upload_num':
        user_states[chat_id] = 'wait_for_txt'
        edit_message(chat_id, msg_id, render_body_text('📂 Please upload the numbers in a <b>.txt</b> or <b>.csv</b> file.'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'back_to_admin', 'style': _rs()}]]})
    elif data == 'delete_files':
        _reset_btn_counter()
        kb = []
        for b_id, b_data in number_batches.items():
            kb.append([{'text': f"{b_data['filename']} ({len(b_data['numbers'])})", 'icon_custom_emoji_id': '5422557736330106570', 'callback_data': f'del_b_{b_id}', 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'back_to_admin', 'style': _rs()}])
        txt = '🗑 Select a file to delete:' if len(kb) > 1 else f"{PEM['no']} No files found."
        edit_message(chat_id, msg_id, render_body_text(txt), reply_markup={'inline_keyboard': kb})
    elif data.startswith('del_b_'):
        b_id = data.split('del_b_')[1]
        if b_id in number_batches:
            del number_batches[b_id]
            save_local_db()
            answer_callback(call['id'], '✅ File deleted!', show_alert=True)
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': 'delete_files', 'id': 'internal'})
    elif data == 'show_used':
        all_nums = _get_all_numbers_set()
        otp_used = [n for n in all_nums if n in otp_received_numbers]
        _reset_btn_counter()
        kb = {'inline_keyboard': [[{'text': 'Download TXT', 'icon_custom_emoji_id': '5257969839313526622', 'callback_data': 'dl_used', 'style': _rs()}], [{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'back_to_admin', 'style': _rs()}]]}
        edit_message(chat_id, msg_id, render_body_text(f"{PEM['ok']} <b>Used Numbers (OTP Received):</b> {len(otp_used)}"), reply_markup=kb)
    elif data == 'show_unused':
        all_nums = _get_all_numbers_set()
        otp_unused = [n for n in all_nums if n not in otp_received_numbers]
        _reset_btn_counter()
        kb = {'inline_keyboard': [[{'text': 'Download TXT', 'icon_custom_emoji_id': '5257969839313526622', 'callback_data': 'dl_unused', 'style': _rs()}], [{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'back_to_admin', 'style': _rs()}]]}
        edit_message(chat_id, msg_id, render_body_text(f"{PEM['rocket']} <b>Unused Numbers (No OTP):</b> {len(otp_unused)}"), reply_markup=kb)
    elif data == 'dl_used':
        all_nums = _get_all_numbers_set()
        otp_used = [n for n in all_nums if n in otp_received_numbers]
        if not otp_used:
            answer_callback(call['id'], 'No OTP received numbers found!', show_alert=True)
            return
        content = '\n'.join(otp_used).encode('utf-8')
        send_document(chat_id, 'used_otp_numbers.txt', content)
        answer_callback(call['id'])
    elif data == 'dl_unused':
        all_nums = _get_all_numbers_set()
        otp_unused = [n for n in all_nums if n not in otp_received_numbers]
        if not otp_unused:
            answer_callback(call['id'], 'All numbers have received OTP!', show_alert=True)
            return
        content = '\n'.join(otp_unused).encode('utf-8')
        send_document(chat_id, 'unused_no_otp_numbers.txt', content)
        answer_callback(call['id'])
    elif data == 'lb_main':
        txt = f"➖➖➖➖➖➖➖➖➖➖➖➖\n《 {PEM['admin']} <b>LEADER BOARD MENU</b> 》\n➖➖➖➖➖➖➖➖➖➖➖➖\n<i>Select a category to view the top performers or history.</i>\n➖➖➖➖➖➖➖➖➖➖➖➖"
        _reset_btn_counter()
        kb = [[{'text': 'Top Referrers', 'icon_custom_emoji_id': '5420145051336485498', 'callback_data': 'lb_top_refs', 'style': _rs()}], [{'text': 'Top OTP Receivers', 'icon_custom_emoji_id': '5353001161878182134', 'callback_data': 'lb_top_otps', 'style': _rs()}], [{'text': 'Withdrawal History', 'icon_custom_emoji_id': '5348469219761626211', 'callback_data': 'lb_w_history', 'style': _rs()}], [{'text': 'Back to Admin', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'back_to_admin', 'style': _rs()}]]
        edit_message(chat_id, msg_id, render_body_text(txt), reply_markup={'inline_keyboard': kb})
    elif data.startswith('lb_'):
        sub = data.replace('lb_', '')
        edit_message(chat_id, msg_id, render_body_text('⌛ <i>Fetching Data...</i>'))
        num_map = {'1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣', '0': '0️⃣'}

        def get_p_num(n):
            return ''.join([num_map.get(c, c) for c in str(n)])
        try:
            if sub == 'top_refs':
                title, field, limit_n, icon = ('TOP 5 REFERRERS', 'total_refers', 5, PEM.get('user', '👥'))
                res_txt = ''
                count = 1
                sorted_users = sorted(local_users_db.items(), key=lambda x: x[1].get(field, 0), reverse=True)[:limit_n]
                for uid, d in sorted_users:
                    if d.get(field, 0) > 0:
                        p = '└' if count == limit_n else '├'
                        res_txt += f"{p} {get_p_num(count)} <a href='tg://user?id={uid}'>{uid}</a> ➔ <b>{d.get(field, 0)}</b>\n"
                        count += 1
                if not res_txt:
                    res_txt = '└ <i>No data found.</i>\n'
            elif sub == 'top_otps':
                title, field, limit_n, icon = ('TOP 5 OTP RECEIVERS', 'total_otps', 5, PEM.get('msg', '📩'))
                res_txt = ''
                count = 1
                sorted_users = sorted(local_users_db.items(), key=lambda x: x[1].get(field, 0), reverse=True)[:limit_n]
                for uid, d in sorted_users:
                    if d.get(field, 0) > 0:
                        p = '└' if count == limit_n else '├'
                        res_txt += f"{p} {get_p_num(count)} <a href='tg://user?id={uid}'>{uid}</a> ➔ <b>{d.get(field, 0)}</b>\n"
                        count += 1
                if not res_txt:
                    res_txt = '└ <i>No data found.</i>\n'
            elif sub == 'w_history':
                title, limit_n, icon = ('LAST 10 WITHDRAWALS', 10, PEM.get('money', '💸'))
                res_txt = ''
                count = 1
                sorted_ws = sorted(local_withdrawals_db.items(), key=lambda x: x[1].get('timestamp', 0), reverse=True)[:limit_n]
                for wid, d in sorted_ws:
                    s = str(d.get('status', 'Pending')).lower()
                    stat_icon = PEM.get('ok', '✅') if s in ['approved', 'success'] else PEM.get('no', '❌') if s == 'rejected' else '⏳'
                    uid = d.get('user_id', 'User')
                    p = '└' if count == limit_n else '├'
                    res_txt += f"{p} {get_p_num(count)} <a href='tg://user?id={uid}'>{uid}</a> ➔ <b>{d.get('amount', 0)}৳</b> {stat_icon}\n"
                    count += 1
                if not res_txt:
                    res_txt = '└ <i>No history found.</i>\n'
            final_msg = f'➖➖➖➖➖➖➖➖➖➖➖➖\n{icon} <b>{title}</b>\n➖➖➖➖➖➖➖➖➖➖➖➖\n{res_txt}➖➖➖➖➖➖➖➖➖➖➖➖'
            _reset_btn_counter()
            kb = [[{'text': 'Refresh', 'icon_custom_emoji_id': '5420155432272438703', 'callback_data': data, 'style': _rs()}, {'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'lb_main', 'style': _rs()}]]
            edit_message(chat_id, msg_id, render_body_text(final_msg), reply_markup={'inline_keyboard': kb})
        except Exception as e:
            edit_message(chat_id, msg_id, render_body_text(f'❌ Error: {e}'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'lb_main', 'style': _rs()}]]})
    elif data == 'back_to_admin':
        if chat_id in user_states:
            user_states.pop(chat_id, None)
        if chat_id in temp_data:
            temp_data.pop(chat_id, None)
        edit_message(chat_id, msg_id, get_admin_text(), reply_markup=admin_panel_keyboard())
    elif data == 'system_settings':
        edit_message(chat_id, msg_id, render_body_text(f"{PEM['gear']} <b>System Settings</b>\nManage advanced bot configurations below:"), reply_markup=system_settings_keyboard())
    elif data == 'test_message_flow':
        user_states[chat_id] = 'wait_for_test_service'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('🧪 <b>Test Mode</b>\n\n📝 Send the Service Name (e.g. IG):'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'system_settings', 'style': _rs()}]]})
    elif data == 'auto_mode':
        nexa_cnt = len(bot_settings.get('nexa_keys', []))
        voltx_cnt = len(bot_settings.get('voltx_keys', []))
        stex_cnt = len(bot_settings.get('stex_keys', []))
        nexa_on = bot_settings.get('nexa_on', False)
        voltx_on = bot_settings.get('voltx_on', False)
        stex_on = bot_settings.get('stex_on', False)
        _on_txt = '<tg-emoji emoji-id="6266827283135207188">✅</tg-emoji> ON'
        _off_txt = '<tg-emoji emoji-id="6267237615720731788">🔴</tg-emoji> OFF'
        edit_message(chat_id, msg_id, render_body_text(f'➖➖➖➖➖➖➖\n  <tg-emoji emoji-id="6318566568011764192">⚡</tg-emoji>  <b>AUTO MODE</b>  <tg-emoji emoji-id="6318566568011764192">⚡</tg-emoji>\n➖➖➖➖➖➖➖\n\n<b>Nexa</b>   »  Keys: <b>{nexa_cnt}</b>   {(_on_txt if nexa_on else _off_txt)}\n<b>VoltX</b>  »  Keys: <b>{voltx_cnt}</b>  {(_on_txt if voltx_on else _off_txt)}\n<b>Stex</b>   »  Keys: <b>{stex_cnt}</b>   {(_on_txt if stex_on else _off_txt)}\n\n➖➖➖➖➖➖➖'), reply_markup=auto_mode_keyboard())
    elif data == 'toggle_nexa':
        bot_settings['nexa_on'] = not bot_settings.get('nexa_on', False)
        save_local_db()
        if bot_settings['nexa_on']:
            _service_warmup_needed['nexa'] = True
        answer_callback(call['id'], f"Nexa is now {'ON' if bot_settings['nexa_on'] else 'OFF'}")
        handle_callback({'message': call['message'], 'data': 'auto_mode', 'id': 'internal'})
    elif data == 'toggle_voltx':
        bot_settings['voltx_on'] = not bot_settings.get('voltx_on', False)
        save_local_db()
        if bot_settings['voltx_on']:
            _service_warmup_needed['voltx'] = True
        answer_callback(call['id'], f"VoltX is now {'ON' if bot_settings['voltx_on'] else 'OFF'}")
        handle_callback({'message': call['message'], 'data': 'auto_mode', 'id': 'internal'})
    elif data == 'toggle_stex':
        bot_settings['stex_on'] = not bot_settings.get('stex_on', False)
        save_local_db()
        if bot_settings['stex_on']:
            _service_warmup_needed['stex'] = True
        answer_callback(call['id'], f"Stex is now {'ON' if bot_settings['stex_on'] else 'OFF'}")
        handle_callback({'message': call['message'], 'data': 'auto_mode', 'id': 'internal'})
         elif data == 'toggle_smsbower':
            bot_settings['smsbower_on'] = not bot_settings.get('smsbower_on', False)
            save_local_db()
    answer_callback(call['id'], f"SMSBower is now {'ON' if bot_settings['smsbower_on'] else 'OFF'}")
    handle_callback({'message': call['message'], 'data': 'auto_mode', 'id': 'internal'})
        elif data == 'smsbower_control':
    _reset_btn_counter()
    api_key_set = '✅ Set' if bot_settings.get('smsbower_api_key') else '❌ Not Set'
    svc_count = len(bot_settings.get('smsbower_services', {}))
    kb = {
        'inline_keyboard': [
            [{'text': 'Set API Key', 'icon_custom_emoji_id': '5353022963132174959', 'callback_data': 'sb_set_key', 'style': _rs()}],
            [{'text': f'Add Service ({svc_count})', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': 'sb_add_service', 'style': _rs()}],
            [{'text': 'View Services', 'icon_custom_emoji_id': '5353032893096567467', 'callback_data': 'sb_view_services', 'style': _rs()}],
            [{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'auto_mode', 'style': _rs()}]
        ]
    }
    edit_message(chat_id, msg_id, render_body_text(
        f'<tg-emoji emoji-id="6282760761399841824">🔹</tg-emoji> <b>SMSBower Control</b>\n\n'
        f'API Key: {api_key_set}\n'
        f'Services: <b>{svc_count}</b>'
    ), reply_markup=kb)
elif data == 'sb_set_key':
    user_states[chat_id] = 'wait_for_sb_api_key'
    temp_data[chat_id] = {'msg_id': msg_id}
    edit_message(chat_id, msg_id, render_body_text('📝 Send your <b>SMSBower API Key</b>:'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'smsbower_control', 'style': _rs()}]]})
elif data == 'sb_add_service':
    user_states[chat_id] = 'wait_for_sb_service'
    temp_data[chat_id] = {'msg_id': msg_id}
    edit_message(chat_id, msg_id, render_body_text('📝 Send in format: <code>service_code:country_id</code>\n\n<b>Example:</b>\n<code>tg:6</code> (Telegram, Indonesia)\n<code>wa:22</code> (WhatsApp, Bangladesh)\n<code>fb:0</code> (Facebook, Russia)'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'smsbower_control', 'style': _rs()}]]})
elif data == 'sb_view_services':
    services = bot_settings.get('smsbower_services', {})
    _reset_btn_counter()
    kb = []
    for svc, cid in services.items():
        kb.append([{'text': f'Delete {svc}:{cid}', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'sb_del_{svc}', 'style': _rs()}])
    kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'smsbower_control', 'style': _rs()}])
    edit_message(chat_id, msg_id, render_body_text(f'📋 <b>SMSBower Services</b> ({len(services)}):'), reply_markup={'inline_keyboard': kb})
elif data.startswith('sb_del_'):
    svc = data.replace('sb_del_', '')
    if svc in bot_settings.get('smsbower_services', {}):
        del bot_settings['smsbower_services'][svc]
        save_local_db()
        answer_callback(call['id'], f'✅ {svc} deleted!', show_alert=True)
        handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': 'sb_view_services', 'id': 'internal'})
    else:
        answer_callback(call['id'], '❌ Service not found!', show_alert=True)
    elif data == 'nexa_control':
        edit_message(chat_id, msg_id, render_body_text(f'<tg-emoji emoji-id="6282760761399841824">🔹</tg-emoji> <b>Nexa</b>\n\nTotal API Keys: {len(bot_settings.get("nexa_keys", []))}\nManage your Nexa API Keys below:'), reply_markup=_panel_control_keyboard("Nexa"))
    elif data == 'add_nexa_key':
        user_states[chat_id] = 'wait_for_add_nexa_key'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Send the new Nexa API Key (e.g. nxa_...):'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'nexa_control', 'style': _rs()}]]})
    elif data == 'view_nexa_keys':
        _reset_btn_counter()
        kb = []
        for idx, key in enumerate(bot_settings.get('nexa_keys', [])):
            safe_name = key[:10] + '...' if len(key) > 10 else key
            kb.append([{'text': f'Delete {safe_name}', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'del_nxa_{idx}', 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'nexa_control', 'style': _rs()}])
        edit_message(chat_id, msg_id, render_body_text('🗑 <b>Select Nexa Key to Delete:</b>'), reply_markup={'inline_keyboard': kb})
    elif data.startswith('del_nxa_'):
        idx = _safe_int(data.split('_')[2] if len(data.split('_')) > 2 else -1)
        if 0 <= idx < len(bot_settings.get('nexa_keys', [])):
            del bot_settings['nexa_keys'][idx]
            save_local_db()
            answer_callback(call['id'], '✅ Nexa Key Deleted!', show_alert=True)
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': 'view_nexa_keys', 'id': 'internal'})
        else:
            answer_callback(call['id'], '❌ Key not found!', show_alert=True)
    elif data == 'nexa_search_country':
        _show_panel_search_countries('nexa', chat_id, msg_id)
    elif data == 'add_search_country':
        user_states[chat_id] = 'wait_for_add_sc'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Send the Country Code (e.g. 880 or 92):'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'nexa_search_country', 'style': _rs()}]]})
    elif data.startswith('del_sc_'):
        idx = _safe_int(data.split('_')[2] if len(data.split('_')) > 2 else -1)
        if 0 <= idx < len(bot_settings.get('nexa_search_countries', [])):
            del bot_settings['nexa_search_countries'][idx]
            save_local_db()
            answer_callback(call['id'], '✅ Country Deleted!', show_alert=True)
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': 'nexa_search_country', 'id': 'internal'})
        else:
            answer_callback(call['id'], '❌ Country not found!', show_alert=True)
    elif data == 'manage_nexa_srv':
        _reset_btn_counter()
        kb = []
        srvs = bot_settings.get('nexa_services', {})
        apps_db = bot_settings.get('premium_apps', {})
        for si, srv in enumerate(srvs):
            emoji_id = _get_service_emoji_id(srv, apps_db)
            kb.append([{'text': f'{srv}', 'icon_custom_emoji_id': emoji_id, 'callback_data': f'nx_srv_{srv}', 'style': _rs()}])
        kb.append([{'text': 'Add New Service', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': 'nx_add_srv', 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'nexa_control', 'style': _rs()}])
        edit_message(chat_id, msg_id, render_body_text('📦 <b>Nexa Services Manager</b>\nManage your API-based dynamic services below:'), reply_markup={'inline_keyboard': kb})
    elif data == 'nx_add_srv':
        user_states[chat_id] = 'wait_nx_srv_name'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Enter Service Name (e.g. TELEGRAM):'), reply_markup=get_cancel_kb())
    elif data.startswith('nx_srv_'):
        srv = data.replace('nx_srv_', '')
        _reset_btn_counter()
        kb = []
        countries = bot_settings['nexa_services'].get(srv, {})
        flags_db = bot_settings.get('premium_flags', {})
        for ci, c in enumerate(countries):
            emoji_id = _find_flag_emoji_id(c, flags_db)
            kb.append([{'text': f'{c} ({len(countries[c])} Ranges)', 'icon_custom_emoji_id': emoji_id, 'callback_data': f'nx_cnt_{srv}_{c}', 'style': _rs()}])
        kb.append([{'text': 'Add Country', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': f'nx_add_cnt_{srv}', 'style': _rs()}])
        kb.append([{'text': 'Delete Service', 'icon_custom_emoji_id': '5422557736330106570', 'callback_data': f'nx_del_srv_{srv}', 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_nexa_srv', 'style': _rs()}])
        edit_message(chat_id, msg_id, render_body_text(f'📂 <b> {srv}</b>\nManage countries for this service:'), reply_markup={'inline_keyboard': kb})
    elif data.startswith('nx_add_cnt_'):
        srv = data.replace('nx_add_cnt_', '')
        user_states[chat_id] = 'wait_nx_cnt_name'
        temp_data[chat_id] = {'msg_id': msg_id, 'srv': srv}
        edit_message(chat_id, msg_id, render_body_text(f'🌍 Enter Country Name for <b>{srv}</b> (e.g. BD, INDIA):'), reply_markup=get_cancel_kb())
    elif data.startswith('nx_cnt_'):
        _sfx = data[len('nx_cnt_'):]
        srv, _, cnt = _sfx.partition('_')
        ranges = bot_settings['nexa_services'][srv].get(cnt, [])
        _reset_btn_counter()
        kb = []
        row = []
        for ri, r in enumerate(ranges):
            row.append({'text': f'Delete {r}', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'nx_dr_{srv}_{cnt}_{r}', 'style': _rs()})
            if len(row) == 2:
                kb.append(row)
                row = []
        if row:
            kb.append(row)
        kb.append([{'text': 'Add Range', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': f'nx_addr_{srv}_{cnt}', 'style': _rs()}])
        kb.append([{'text': 'Delete Entire Country', 'icon_custom_emoji_id': '5422557736330106570', 'callback_data': f'nx_del_cnt_{srv}_{cnt}', 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'nx_srv_{srv}', 'style': _rs()}])
        txt = f'📍 <b> {srv} | Country: {cnt}</b>\n\n<b>Total Ranges:</b> {len(ranges)}\n<i>Click on a range below to delete it, or add a new one.</i>'
        edit_message(chat_id, msg_id, render_body_text(txt), reply_markup={'inline_keyboard': kb})
    elif data.startswith('nx_addr_'):
        _sfx = data[len('nx_addr_'):]
        srv, _, cnt = _sfx.partition('_')
        user_states[chat_id] = 'wait_nx_addr'
        temp_data[chat_id] = {'msg_id': msg_id, 'srv': srv, 'cnt': cnt}
        edit_message(chat_id, msg_id, render_body_text(f'📝 Send the new Range for <b>{cnt}</b> (e.g. 88017):'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'nx_cnt_{srv}_{cnt}', 'style': _rs()}]]})
    elif data.startswith('nx_dr_'):
        _sfx = data[len('nx_dr_'):]
        srv, _, _rest = _sfx.partition('_')
        cnt, _, rng = _rest.partition('_')
        if rng in bot_settings['nexa_services'].get(srv, {}).get(cnt, []):
            bot_settings['nexa_services'][srv][cnt].remove(rng)
            save_local_db()
            answer_callback(call['id'], f'✅ Range {rng} deleted!', show_alert=True)
        handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': f'nx_cnt_{srv}_{cnt}', 'id': 'internal'})
    elif data.startswith('nx_del_srv_'):
        srv = data.replace('nx_del_srv_', '')
        if srv in bot_settings['nexa_services']:
            del bot_settings['nexa_services'][srv]
        save_local_db()
        handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': 'manage_nexa_srv', 'id': 'internal'})
    elif data.startswith('nx_del_cnt_'):
        _sfx = data[len('nx_del_cnt_'):]
        srv, _, cnt = _sfx.partition('_')
        if cnt in bot_settings['nexa_services'].get(srv, {}):
            del bot_settings['nexa_services'][srv][cnt]
        save_local_db()
        handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': f'nx_srv_{srv}', 'id': 'internal'})
    elif data == 'voltx_control':
        edit_message(chat_id, msg_id, render_body_text(f'<tg-emoji emoji-id="6282760761399841824">🔹</tg-emoji> <b>VoltX</b>\n\nTotal API Keys: {len(bot_settings.get("voltx_keys", []))}\nManage your VoltX API Keys below:'), reply_markup=_panel_control_keyboard("VoltX"))
    elif data == 'add_voltx_key':
        user_states[chat_id] = 'wait_for_add_voltx_key'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Send the new VoltX API Key (mauthapi key):'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'voltx_control', 'style': _rs()}]]})
    elif data == 'view_voltx_keys':
        _reset_btn_counter()
        kb = []
        for idx, key in enumerate(bot_settings.get('voltx_keys', [])):
            safe_name = key[:10] + '...' if len(key) > 10 else key
            kb.append([{'text': f'Delete {safe_name}', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'del_vx_{idx}', 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'voltx_control', 'style': _rs()}])
        edit_message(chat_id, msg_id, render_body_text('🗑 <b>Select VoltX Key to Delete:</b>'), reply_markup={'inline_keyboard': kb})
    elif data.startswith('del_vxsc_'):
        idx = _safe_int(data.split('_')[2] if len(data.split('_')) > 2 else -1)
        if 0 <= idx < len(bot_settings.get('voltx_search_countries', [])):
            del bot_settings['voltx_search_countries'][idx]
            save_local_db()
            answer_callback(call['id'], '✅ Country Deleted!', show_alert=True)
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': 'voltx_search_country', 'id': 'internal'})
        else:
            answer_callback(call['id'], '❌ Country not found!', show_alert=True)
    elif data.startswith('del_vx_'):
        idx = _safe_int(data.split('_')[2] if len(data.split('_')) > 2 else -1)
        if 0 <= idx < len(bot_settings.get('voltx_keys', [])):
            del bot_settings['voltx_keys'][idx]
            save_local_db()
            answer_callback(call['id'], '✅ VoltX Key Deleted!', show_alert=True)
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': 'view_voltx_keys', 'id': 'internal'})
        else:
            answer_callback(call['id'], '❌ Key not found!', show_alert=True)
    elif data == 'voltx_search_country':
        _show_panel_search_countries('voltx', chat_id, msg_id)
    elif data == 'add_vx_search_country':
        user_states[chat_id] = 'wait_for_add_vxsc'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Send the Country Code (e.g. 880 or 92):'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'voltx_search_country', 'style': _rs()}]]})
    elif data == 'manage_voltx_srv':
        _reset_btn_counter()
        kb = []
        srvs = bot_settings.get('voltx_services', {})
        apps_db = bot_settings.get('premium_apps', {})
        for si, srv in enumerate(srvs):
            emoji_id = _get_service_emoji_id(srv, apps_db)
            kb.append([{'text': f'{srv}', 'icon_custom_emoji_id': emoji_id, 'callback_data': f'vx_srv_{srv}', 'style': _rs()}])
        kb.append([{'text': 'Add New Service', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': 'vx_add_srv', 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'voltx_control', 'style': _rs()}])
        edit_message(chat_id, msg_id, render_body_text('📦 <b>VoltX Services Manager</b>\nManage your API-based dynamic services below:'), reply_markup={'inline_keyboard': kb})
    elif data == 'vx_add_srv':
        user_states[chat_id] = 'wait_vx_srv_name'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Enter Service Name (e.g. WHATSAPP, FACEBOOK):'), reply_markup=get_cancel_kb())
    elif data.startswith('vx_srv_'):
        srv = data.replace('vx_srv_', '')
        _reset_btn_counter()
        kb = []
        countries = bot_settings['voltx_services'].get(srv, {})
        flags_db = bot_settings.get('premium_flags', {})
        for ci, c in enumerate(countries):
            emoji_id = _find_flag_emoji_id(c, flags_db)
            kb.append([{'text': f'{c} ({len(countries[c])} Ranges)', 'icon_custom_emoji_id': emoji_id, 'callback_data': f'vx_cnt_{srv}_{c}', 'style': _rs()}])
        kb.append([{'text': 'Add Country', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': f'vx_add_cnt_{srv}', 'style': _rs()}])
        kb.append([{'text': 'Delete Service', 'icon_custom_emoji_id': '5422557736330106570', 'callback_data': f'vx_del_srv_{srv}', 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_voltx_srv', 'style': _rs()}])
        edit_message(chat_id, msg_id, render_body_text(f'📂 <b> {srv}</b>\nManage countries for this service:'), reply_markup={'inline_keyboard': kb})
    elif data.startswith('vx_add_cnt_'):
        srv = data.replace('vx_add_cnt_', '')
        user_states[chat_id] = 'wait_vx_cnt_name'
        temp_data[chat_id] = {'msg_id': msg_id, 'srv': srv}
        edit_message(chat_id, msg_id, render_body_text(f'🌍 Enter Country Name for <b>{srv}</b> (e.g. BD, INDIA):'), reply_markup=get_cancel_kb())
    elif data.startswith('vx_cnt_'):
        _sfx = data[len('vx_cnt_'):]
        srv, _, cnt = _sfx.partition('_')
        ranges = bot_settings['voltx_services'][srv].get(cnt, [])
        _reset_btn_counter()
        kb = []
        row = []
        for ri, r in enumerate(ranges):
            row.append({'text': f'Del {r}', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'vx_dr_{srv}_{cnt}_{r}', 'style': _rs()})
            if len(row) == 2:
                kb.append(row)
                row = []
        if row:
            kb.append(row)
        kb.append([{'text': 'Add Range', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': f'vx_addr_{srv}_{cnt}', 'style': _rs()}])
        kb.append([{'text': 'Delete Entire Country', 'icon_custom_emoji_id': '5422557736330106570', 'callback_data': f'vx_del_cnt_{srv}_{cnt}', 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'vx_srv_{srv}', 'style': _rs()}])
        txt = f'📍 <b> {srv} | Country: {cnt}</b>\n\n<b>Total Ranges:</b> {len(ranges)}\n<i>Click on a range below to delete it, or add a new one.</i>'
        edit_message(chat_id, msg_id, render_body_text(txt), reply_markup={'inline_keyboard': kb})
    elif data.startswith('vx_addr_'):
        _sfx = data[len('vx_addr_'):]
        srv, _, cnt = _sfx.partition('_')
        user_states[chat_id] = 'wait_vx_addr'
        temp_data[chat_id] = {'msg_id': msg_id, 'srv': srv, 'cnt': cnt}
        edit_message(chat_id, msg_id, render_body_text(f'📝 Send the new Range for <b>{cnt}</b> (e.g. 88017):'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'vx_cnt_{srv}_{cnt}', 'style': _rs()}]]})
    elif data.startswith('vx_dr_'):
        _sfx = data[len('vx_dr_'):]
        srv, _, _rest = _sfx.partition('_')
        cnt, _, rng = _rest.partition('_')
        if rng in bot_settings['voltx_services'].get(srv, {}).get(cnt, []):
            bot_settings['voltx_services'][srv][cnt].remove(rng)
            save_local_db()
            answer_callback(call['id'], f'✅ Range {rng} deleted!', show_alert=True)
        handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': f'vx_cnt_{srv}_{cnt}', 'id': 'internal'})
    elif data.startswith('vx_del_srv_'):
        srv = data.replace('vx_del_srv_', '')
        if srv in bot_settings['voltx_services']:
            del bot_settings['voltx_services'][srv]
        save_local_db()
        handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': 'manage_voltx_srv', 'id': 'internal'})
    elif data.startswith('vx_del_cnt_'):
        _sfx = data[len('vx_del_cnt_'):]
        srv, _, cnt = _sfx.partition('_')
        if cnt in bot_settings['voltx_services'].get(srv, {}):
            del bot_settings['voltx_services'][srv][cnt]
        save_local_db()
        handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': f'vx_srv_{srv}', 'id': 'internal'})
    elif data == 'stex_control':
        edit_message(chat_id, msg_id, render_body_text(f'<tg-emoji emoji-id="6282760761399841824">🔹</tg-emoji> <b>Stex</b>\n\nTotal API Keys: {len(bot_settings.get("stex_keys", []))}\nManage your Stex API Keys below:'), reply_markup=_panel_control_keyboard("Stex"))
    elif data == 'add_stex_key':
        user_states[chat_id] = 'wait_for_add_stex_key'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Send the new Stex API Key (api-key):'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'stex_control', 'style': _rs()}]]})
    elif data == 'view_stex_keys':
        _reset_btn_counter()
        kb = []
        for idx, key in enumerate(bot_settings.get('stex_keys', [])):
            safe_name = key[:10] + '...' if len(key) > 10 else key
            kb.append([{'text': f'Delete {safe_name}', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'del_stx_{idx}', 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'stex_control', 'style': _rs()}])
        edit_message(chat_id, msg_id, render_body_text('🗑 <b>Select Stex Key to Delete:</b>'), reply_markup={'inline_keyboard': kb})
    elif data.startswith('del_stxsc_'):
        idx = _safe_int(data.split('_')[2] if len(data.split('_')) > 2 else -1)
        if 0 <= idx < len(bot_settings.get('stex_search_countries', [])):
            del bot_settings['stex_search_countries'][idx]
            save_local_db()
            answer_callback(call['id'], '✅ Country Deleted!', show_alert=True)
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': 'stex_search_country', 'id': 'internal'})
        else:
            answer_callback(call['id'], '❌ Country not found!', show_alert=True)
    elif data.startswith('del_stx_'):
        idx = _safe_int(data.split('_')[2] if len(data.split('_')) > 2 else -1)
        if 0 <= idx < len(bot_settings.get('stex_keys', [])):
            del bot_settings['stex_keys'][idx]
            save_local_db()
            answer_callback(call['id'], '✅ Stex Key Deleted!', show_alert=True)
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': 'view_stex_keys', 'id': 'internal'})
        else:
            answer_callback(call['id'], '❌ Key not found!', show_alert=True)
    elif data == 'stex_search_country':
        _show_panel_search_countries('stex', chat_id, msg_id)
    elif data == 'add_stx_search_country':
        user_states[chat_id] = 'wait_for_add_stxsc'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Send the Country Code (e.g. 880 or 92):'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'stex_search_country', 'style': _rs()}]]})
    elif data == 'manage_stex_srv':
        _reset_btn_counter()
        kb = []
        srvs = bot_settings.get('stex_services', {})
        apps_db = bot_settings.get('premium_apps', {})
        for si, srv in enumerate(srvs):
            emoji_id = _get_service_emoji_id(srv, apps_db)
            kb.append([{'text': f'{srv}', 'icon_custom_emoji_id': emoji_id, 'callback_data': f'stx_srv_{srv}', 'style': _rs()}])
        kb.append([{'text': 'Add New Service', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': 'stx_add_srv', 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'stex_control', 'style': _rs()}])
        edit_message(chat_id, msg_id, render_body_text('📦 <b>Stex Services Manager</b>\nManage your API-based dynamic services below:'), reply_markup={'inline_keyboard': kb})
    elif data == 'stx_add_srv':
        user_states[chat_id] = 'wait_stx_srv_name'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Enter Service Name (e.g. WHATSAPP, FACEBOOK):'), reply_markup=get_cancel_kb())
    elif data.startswith('stx_srv_'):
        srv = data.replace('stx_srv_', '')
        _reset_btn_counter()
        kb = []
        countries = bot_settings['stex_services'].get(srv, {})
        flags_db = bot_settings.get('premium_flags', {})
        for ci, c in enumerate(countries):
            emoji_id = _find_flag_emoji_id(c, flags_db)
            kb.append([{'text': f'{c} ({len(countries[c])} Ranges)', 'icon_custom_emoji_id': emoji_id, 'callback_data': f'stx_cnt_{srv}_{c}', 'style': _rs()}])
        kb.append([{'text': 'Add Country', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': f'stx_add_cnt_{srv}', 'style': _rs()}])
        kb.append([{'text': 'Delete Service', 'icon_custom_emoji_id': '5422557736330106570', 'callback_data': f'stx_del_srv_{srv}', 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_stex_srv', 'style': _rs()}])
        edit_message(chat_id, msg_id, render_body_text(f'📂 <b> {srv}</b>\nManage countries for this service:'), reply_markup={'inline_keyboard': kb})
    elif data.startswith('stx_add_cnt_'):
        srv = data.replace('stx_add_cnt_', '')
        user_states[chat_id] = 'wait_stx_cnt_name'
        temp_data[chat_id] = {'msg_id': msg_id, 'srv': srv}
        edit_message(chat_id, msg_id, render_body_text(f'🌍 Enter Country Name for <b>{srv}</b> (e.g. BD, INDIA):'), reply_markup=get_cancel_kb())
    elif data.startswith('stx_cnt_'):
        _sfx = data[len('stx_cnt_'):]
        srv, _, cnt = _sfx.rpartition('_')
        ranges = bot_settings['stex_services'][srv].get(cnt, [])
        _reset_btn_counter()
        kb = []
        row = []
        for ri, r in enumerate(ranges):
            row.append({'text': f'Del {r}', 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'stx_dr_{srv}_{cnt}_{r}', 'style': _rs()})
            if len(row) == 2:
                kb.append(row)
                row = []
        if row:
            kb.append(row)
        kb.append([{'text': 'Add Range', 'icon_custom_emoji_id': '5420323438508155202', 'callback_data': f'stx_addr_{srv}_{cnt}', 'style': _rs()}])
        kb.append([{'text': 'Delete Entire Country', 'icon_custom_emoji_id': '5422557736330106570', 'callback_data': f'stx_del_cnt_{srv}_{cnt}', 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'stx_srv_{srv}', 'style': _rs()}])
        txt = f'📍 <b> {srv} | Country: {cnt}</b>\n\n<b>Total Ranges:</b> {len(ranges)}\n<i>Click on a range below to delete it, or add a new one.</i>'
        edit_message(chat_id, msg_id, render_body_text(txt), reply_markup={'inline_keyboard': kb})
    elif data.startswith('stx_addr_'):
        _sfx = data[len('stx_addr_'):]
        srv, _, cnt = _sfx.rpartition('_')
        user_states[chat_id] = 'wait_stx_addr'
        temp_data[chat_id] = {'msg_id': msg_id, 'srv': srv, 'cnt': cnt}
        edit_message(chat_id, msg_id, render_body_text(f'📝 Send the new Range for <b>{cnt}</b> (e.g. 88017):'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'stx_cnt_{srv}_{cnt}', 'style': _rs()}]]})
    elif data.startswith('stx_dr_'):
        _sfx = data[len('stx_dr_'):]
        _left, _, rng = _sfx.rpartition('_')
        srv, _, cnt = _left.rpartition('_')
        if rng in bot_settings['stex_services'].get(srv, {}).get(cnt, []):
            bot_settings['stex_services'][srv][cnt].remove(rng)
            save_local_db()
            answer_callback(call['id'], f'✅ Range {rng} deleted!', show_alert=True)
        handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': f'stx_cnt_{srv}_{cnt}', 'id': 'internal'})
    elif data.startswith('stx_del_srv_'):
        srv = data.replace('stx_del_srv_', '')
        if srv in bot_settings['stex_services']:
            del bot_settings['stex_services'][srv]
        save_local_db()
        handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': 'manage_stex_srv', 'id': 'internal'})
    elif data.startswith('stx_del_cnt_'):
        _sfx = data[len('stx_del_cnt_'):]
        srv, _, cnt = _sfx.rpartition('_')
        if cnt in bot_settings['stex_services'].get(srv, {}):
            del bot_settings['stex_services'][srv][cnt]
        save_local_db()
        handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': f'stx_srv_{srv}', 'id': 'internal'})
    elif data == 'manage_fj':
        _show_fj_panel(chat_id, msg_id)
    elif data == 'toggle_fj':
        bot_settings['fj_on'] = not bot_settings['fj_on']
        save_local_db()
        _show_fj_panel(chat_id, msg_id)
    elif data == 'add_fj':
        user_states[chat_id] = 'wait_for_add_fj'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 <b>Add Channel or Group</b>\n\n✅ Bot must already be an admin in the channel/group!\n\nSend any one of the following:\n• Username: <code>@channelname</code>\n• Public Link: <code>https://t.me/channelname</code>\n• Numeric ID: <code>-1001234567890</code>\n\n🔄 Bot will auto-detect Channel/Group and Private/Public!'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_fj', 'style': _rs()}]]})
    elif data.startswith('del_fj_'):
        idx = _safe_int(data.split('_')[2] if len(data.split('_')) > 2 else -1)
        if 0 <= idx < len(bot_settings['fj_channels']):
            removed = bot_settings['fj_channels'][idx]
            info = _get_fj_info(removed)
            del bot_settings['fj_channels'][idx]
            save_local_db()
            answer_callback(call['id'], f"✅ {info.get('title', 'Item')} deleted!", show_alert=True)
            _show_fj_panel(chat_id, msg_id)
        else:
            answer_callback(call['id'], '❌ Item not found!', show_alert=True)
    elif data == 'manage_admins':
        _show_admin_panel(chat_id, msg_id)
    elif data == 'add_adm':
        user_states[chat_id] = 'wait_for_add_adm'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Send the User ID of the new Admin:'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_admins', 'style': _rs()}]]})
    elif data.startswith('del_adm_'):
        adm_id = _safe_int(data.split('_')[2] if len(data.split('_')) > 2 else -1)
        if adm_id in bot_settings['admins'] and adm_id != OWNER_ID:
            bot_settings['admins'].remove(adm_id)
            save_local_db()
            answer_callback(call['id'], '✅ Admin deleted!', show_alert=True)
            _show_admin_panel(chat_id, msg_id)
        else:
            answer_callback(call['id'], '❌ Admin not found!', show_alert=True)
    elif data == 'manage_otp_groups':
        _show_otp_groups_panel(chat_id, msg_id)
    elif data == 'add_fw':
        user_states[chat_id] = 'wait_for_add_fw_id'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Send the Group ID/Username to forward messages to:'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_otp_groups', 'style': _rs()}]]})
    elif data.startswith('manage_fw_'):
        idx = _safe_int(data.split('_')[2] if len(data.split('_')) > 2 else -1)
        if 0 <= idx < len(bot_settings['fw_groups']):
            grp_id = bot_settings['fw_groups'][idx]['chat_id']
            edit_message(chat_id, msg_id, render_body_text(f'🛡 <b>Manage Group:</b> {grp_id}'), reply_markup=specific_fw_group_keyboard(idx))
        else:
            _alert_group_gone(call)
    elif data.startswith('add_fwbtn_'):
        idx = _safe_int(data.split('_')[2] if len(data.split('_')) > 2 else -1)
        if not 0 <= idx < len(bot_settings['fw_groups']):
            _alert_group_gone(call)
            return
        user_states[chat_id] = 'wait_for_add_fw_btn'
        temp_data[chat_id] = {'msg_id': msg_id, 'fw_idx': idx}
        edit_message(chat_id, msg_id, render_body_text('📝 <b>Add Inline Button</b>\n\n➖➖➖➖➖➖➖\n📌 <b>Format (without emoji):</b>\n<code>Button Text - https://link.com</code>\n\n📌 <b>Format (with premium emoji ID):</b>\n<code>6228781436330054904 Button Text - https://link.com</code>\n➖➖➖➖➖➖➖\n💡 <b>Examples:</b>\n<code>Join Channel - https://t.me/mychannel</code>\n<code>6228781436330054904 Join VIP - https://t.me/vip</code>\n➖➖➖➖➖➖➖\n⚠️ Enter the Emoji ID first, then the button text, then <code> - </code>, then the link.'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'manage_fw_{idx}', 'style': _rs()}]]})
    elif data.startswith('del_fwbtn_'):
        parts = data.split('_')
        idx = _safe_int(parts[2] if len(parts) > 2 else -1)
        b_idx = _safe_int(parts[3] if len(parts) > 3 else -1)
        if 0 <= idx < len(bot_settings['fw_groups']):
            if 0 <= b_idx < len(bot_settings['fw_groups'][idx]['buttons']):
                del bot_settings['fw_groups'][idx]['buttons'][b_idx]
                save_local_db()
                answer_callback(call['id'], '✅ Button deleted!', show_alert=True)
                edit_message(chat_id, msg_id, render_body_text(f"🛡 <b>Manage Group:</b> {bot_settings['fw_groups'][idx]['chat_id']}"), reply_markup=specific_fw_group_keyboard(idx))
            else:
                answer_callback(call['id'], '❌ Button not found!', show_alert=True)
        else:
            _alert_group_gone(call)
    elif data.startswith('del_fw_'):
        idx = _safe_int(data.split('_')[2] if len(data.split('_')) > 2 else -1)
        if 0 <= idx < len(bot_settings['fw_groups']):
            del bot_settings['fw_groups'][idx]
            save_local_db()
            answer_callback(call['id'], '✅ Group deleted!', show_alert=True)
            _show_otp_groups_panel(chat_id, msg_id)
        else:
            _alert_group_gone(call)
    elif data == 'edit_otp_link':
        user_states[chat_id] = 'wait_for_otp_link'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Send the new OTP Group Link:'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_otp_groups', 'style': _rs()}]]})
    elif data == 'topic_settings':
        _show_topic_settings(chat_id, msg_id)
    elif data == 'add_topic':
        user_states[chat_id] = 'wait_for_topic_name'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 <b>Add Topic</b>\n\n1️⃣ Send the Topic Name:'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'topic_settings', 'style': _rs()}]]})
    elif data == 'topic_list':
        _show_topic_list(chat_id, msg_id, delete_mode=False)
    elif data == 'delete_topic_menu':
        _show_topic_list(chat_id, msg_id, delete_mode=True)
    elif data.startswith('del_topic_'):
        idx = _safe_int(data.split('_')[2] if len(data.split('_')) > 2 else -1)
        topics = bot_settings.get('topics', [])
        if 0 <= idx < len(topics):
            deleted = topics.pop(idx)
            save_local_db()
            answer_callback(call['id'], f"✅ {deleted.get('name', 'Topic')} deleted!", show_alert=True)
            _show_topic_list(chat_id, msg_id, delete_mode=True)
        else:
            answer_callback(call['id'], '❌ Topic not found!', show_alert=True)
    elif data == 'manage_panels':
        api_count = len([p for p in bot_settings['panels'] if p.get('type') == 'API Panel'])
        cpt_count = len([p for p in bot_settings['panels'] if p.get('type', 'API Panel') == 'Auto Captcha Panel'])
        text = f"{PEM['gear']} <b>Panel Management</b>\n\nSelect which type of panel system you want to manage:"
        _reset_btn_counter()
        kb = {'inline_keyboard': [[{'text': f'Manage API Panels ({api_count})', 'icon_custom_emoji_id': '5336972142066047577', 'callback_data': 'manage_api_panels', 'style': _rs()}], [{'text': f'Manage Auto Captcha Panels ({cpt_count})', 'icon_custom_emoji_id': '5353022963132174959', 'callback_data': 'manage_cpt_panels', 'style': _rs()}], [{'text': 'Back to System', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'system_settings', 'style': _rs()}]]}
        edit_message(chat_id, msg_id, render_body_text(text), reply_markup=kb)
    elif data in ['manage_api_panels', 'manage_cpt_panels']:
        p_type = 'API Panel' if data == 'manage_api_panels' else 'Auto Captcha Panel'
        p_list = [p for p in bot_settings['panels'] if p.get('type', 'API Panel') == p_type]
        icon = f"{PEM['world']} API" if p_type == 'API Panel' else f"{PEM['lock']} Auto Captcha"
        text = f'{icon} <b>{p_type}s Management</b>\n\n👀 <b>Active Monitors:</b> {len(p_list)}\n\n🟢 <b>Available Providers:</b>\n'
        for p in p_list:
            status = 'Monitoring' if p['status'] == 'ON' else 'Stopped'
            login_state = p.get('login_status', '')
            if p['type'] == 'Auto Captcha Panel':
                conf = f' {login_state}' if login_state else f"{PEM['ok']} Configured"
            else:
                conf = f"{PEM['ok']} Configured" if p.get('api_url') else f"{PEM['no']} Not Configured"
            text += f"• {p['name']}: {(PEM['ok'] if p['status'] == 'ON' else PEM['no'])} {status} | {conf}\n"
        edit_message(chat_id, msg_id, render_body_text(text), reply_markup=typed_panels_list_keyboard(p_type))
    elif data in ['add_api_panel', 'add_cpt_panel']:
        user_states[chat_id] = 'wait_for_panel_name'
        p_type = 'api' if data == 'add_api_panel' else 'logc'
        temp_data[chat_id] = {'msg_id': msg_id, 'add_type': p_type}
        edit_message(chat_id, msg_id, render_body_text('📝 Please send the name of the New Provider:'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f"manage_{('api' if p_type == 'api' else 'cpt')}_panels", 'style': _rs()}]]})
    elif data in ['list_del_api', 'list_del_cpt']:
        p_type = 'API Panel' if data == 'list_del_api' else 'Auto Captcha Panel'
        _reset_btn_counter()
        kb = []
        for idx, p in enumerate(bot_settings['panels']):
            if p.get('type', 'API Panel') == p_type:
                kb.append([{'text': f"Delete {p['name']}", 'icon_custom_emoji_id': '5420130255174145507', 'callback_data': f'do_del_pnl_{idx}', 'style': _rs()}])
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f"manage_{('api' if p_type == 'API Panel' else 'cpt')}_panels", 'style': _rs()}])
        edit_message(chat_id, msg_id, render_body_text(f"{PEM['trash']} <b>Select a Provider to Delete:</b>"), reply_markup={'inline_keyboard': kb})
    elif data.startswith('do_del_pnl_'):
        idx = _safe_int(data.split('_')[3] if len(data.split('_')) > 3 else -1)
        if 0 <= idx < len(bot_settings['panels']):
            p_type = bot_settings['panels'][idx].get('type', 'API Panel')
            if idx in panel_sessions:
                del panel_sessions[idx]
            new_sessions = {}
            for k, v in panel_sessions.items():
                if k > idx:
                    new_sessions[k - 1] = v
                elif k < idx:
                    new_sessions[k] = v
            panel_sessions.clear()
            panel_sessions.update(new_sessions)
            del bot_settings['panels'][idx]
            save_local_db()
            answer_callback(call['id'], '✅ Provider Deleted!', show_alert=True)
            handle_callback({'message': {'chat': {'id': chat_id}, 'message_id': msg_id}, 'data': f"manage_{('api' if p_type == 'API Panel' else 'cpt')}_panels", 'id': 'internal'})
        else:
            answer_callback(call['id'], '❌ Panel not found! May have already been deleted.', show_alert=True)
    elif data.startswith('tog_pnl_'):
        idx = _safe_int(data.split('_')[2] if len(data.split('_')) > 2 else -1)
        if not 0 <= idx < len(bot_settings['panels']):
            _alert_panel_gone(call)
            return
        p = bot_settings['panels'][idx]
        new_status = 'ON' if p['status'] == 'OFF' else 'OFF'
        if new_status == 'ON':
            p['needs_warmup'] = True
        p['status'] = new_status
        save_local_db()
        if new_status == 'ON':
            threading.Thread(target=_eagerly_warmup_panel, args=(idx, p), daemon=True).start()
        _show_panel_cfg(chat_id, msg_id, idx)
    elif data.startswith('conf_pnl_'):
        idx = _safe_int(data.split('_')[2] if len(data.split('_')) > 2 else -1)
        if not 0 <= idx < len(bot_settings['panels']):
            _alert_panel_gone(call)
            return
        _show_panel_cfg(chat_id, msg_id, idx)
    elif data.startswith('set_p_api_'):
        idx = _safe_int(data.split('_')[3] if len(data.split('_')) > 3 else -1)
        if idx < 0 or idx >= len(bot_settings['panels']):
            _alert_panel_gone(call)
            return
        user_states[chat_id] = 'wait_for_p_api'
        _set_panel_temp(chat_id, msg_id, idx)
        edit_message(chat_id, msg_id, render_body_text('📝 Send the API URL for this provider:'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'conf_pnl_{idx}', 'style': _rs()}]]})
    elif data.startswith('set_p_tok_'):
        idx = _safe_int(data.split('_')[3] if len(data.split('_')) > 3 else -1)
        if idx < 0 or idx >= len(bot_settings['panels']):
            _alert_panel_gone(call)
            return
        user_states[chat_id] = 'wait_for_p_tok'
        _set_panel_temp(chat_id, msg_id, idx)
        edit_message(chat_id, msg_id, render_body_text('📝 Send the Token for this provider:'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'conf_pnl_{idx}', 'style': _rs()}]]})
    elif data.startswith('set_p_tokh_'):
        idx = _safe_int(data.split('_')[3] if len(data.split('_')) > 3 else -1)
        if idx < 0 or idx >= len(bot_settings['panels']):
            _alert_panel_gone(call)
            return
        user_states[chat_id] = 'wait_for_p_tokheader'
        _set_panel_temp(chat_id, msg_id, idx)
        edit_message(chat_id, msg_id, render_body_text('📝 Send the <b>Header Name</b> for token authentication.\n\n<b>Example:</b> <code>mauthapi</code> (for VoltX SMS)\n\nWhen set, the token will be sent as an HTTP header instead of a URL parameter.\n\nType <code>none</code> to remove and use URL parameter mode.'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'conf_pnl_{idx}', 'style': _rs()}]]})
    elif data.startswith('set_p_fapi_'):
        idx = _safe_int(data.split('_')[3] if len(data.split('_')) > 3 else -1)
        if idx < 0 or idx >= len(bot_settings['panels']):
            _alert_panel_gone(call)
            return
        user_states[chat_id] = 'wait_for_p_fapi'
        _set_panel_temp(chat_id, msg_id, idx)
        edit_message(chat_id, msg_id, render_body_text('📝 Send the FULL API URL (Example: http://api.com/get?key=YOUR_TOKEN&start=0):'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'conf_pnl_{idx}', 'style': _rs()}]]})
    elif data.startswith('set_p_rec_'):
        idx = _safe_int(data.split('_')[3] if len(data.split('_')) > 3 else -1)
        if idx < 0 or idx >= len(bot_settings['panels']):
            _alert_panel_gone(call)
            return
        user_states[chat_id] = 'wait_for_p_rec'
        _set_panel_temp(chat_id, msg_id, idx)
        edit_message(chat_id, msg_id, render_body_text('📝 Send the number of records to fetch (e.g. 10).\nType <code>0</code> for Unlimited:'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': f'conf_pnl_{idx}', 'style': _rs()}]]})
    elif data.startswith('test_p_conn_'):
        idx = _safe_int(data.split('_')[3] if len(data.split('_')) > 3 else -1)
        if idx < 0 or idx >= len(bot_settings['panels']):
            _alert_panel_gone(call)
            return
        p = bot_settings['panels'][idx]
        wait_msg = send_message(chat_id, render_body_text('⏳ Testing connection. Please wait...'))
        wait_msg_id = wait_msg.get('result', {}).get('message_id') if wait_msg else None
        answer_callback(call['id'])
        try:
            parsed = []
            raw_text = ''
            if p['type'] == 'Auto Captcha Panel':
                sess = panel_sessions.get(idx)
                if not sess:
                    now = time.time()
                    retry_wait = p.get('retry_wait', 90)
                    last_attempt = p.get('last_login_attempt', 0)
                    time_since = now - last_attempt
                    if time_since < retry_wait:
                        remaining = int(retry_wait - time_since)
                        if wait_msg_id:
                            delete_message(chat_id, wait_msg_id)
                        locked_status = p.get('login_status', 'Panel Locked')
                        send_message(chat_id, render_body_text(f'🔒 <b>Panel Locked — Please wait!</b>\n\nStatus: {html.escape(str(locked_status))}\n⏳ <b>{remaining}s</b> Auto-retry will start in that time.\n\n<i>Tap Test Connection after login succeeds.</i>'))
                        return
                    success = attempt_auto_login(p, idx)
                    if not success:
                        if wait_msg_id:
                            delete_message(chat_id, wait_msg_id)
                        send_message(chat_id, render_body_text(f"❌ <b>Auto Login Failed!</b>\nReason: {html.escape(str(p.get('login_status', 'Unknown')))}"))
                        return
                    sess = panel_sessions.get(idx)
                if p.get('api_base'):
                    parsed, raw_text = _fetch_json_api_panel_data(p, sess)
                else:
                    login_url = p.get('login_url', '').strip()
                    if not login_url.startswith('http'):
                        login_url = 'http://' + login_url
                    msg_link = p.get('msg_link', '').strip()
                    if not msg_link.startswith('http') and msg_link != '':
                        msg_link = 'http://' + msg_link
                    _base_u = login_url
                    for _seg in ['/login', '/signin', '/auth', '/sign-in', '/log-in']:
                        if _seg in _base_u.lower():
                            _base_u = _base_u[:_base_u.lower().index(_seg)]
                            break
                    check_url = msg_link if msg_link else f'{_base_u}/client/SMSCDRStats'
                    parsed, raw_text = fetch_cpt_panel_cdrs(p, sess, check_url)
            else:
                full_url = p.get('full_api_url', '').strip()
                url = p.get('api_url', '').strip()
                token = p.get('token', '').strip()
                if not full_url and (not url):
                    if wait_msg_id:
                        delete_message(chat_id, wait_msg_id)
                    send_message(chat_id, render_body_text('❌ Please Set API URL or Full API URL first!'))
                    return
                urls_to_try, headers = _build_api_urls(p)
                parsed = []
                raw_text = ''
                for try_url in urls_to_try:
                    try:
                        res = tg_session.get(try_url, headers=headers, timeout=10)
                        raw_text = res.text
                        if res.status_code == 429 or _is_rate_limited_response(raw_text):
                            if wait_msg_id:
                                delete_message(chat_id, wait_msg_id)
                            send_message(chat_id, render_body_text(f'⚠️ <b>API Rate Limited!</b>\n\nAPI ne bahut zyada requests ke wajah se temporarily block kar diya.\n<i>Try Test Connection again after 5–10 seconds.</i>\n\n<b>Raw:</b> <code>{html.escape(raw_text[:200])}</code>'))
                            return
                        parsed = parse_panel_response(raw_text, p, max_results=3)
                        if parsed:
                            if not full_url and try_url != url and token and (not p.get('token_header', '')):
                                p['api_url'] = try_url.replace(token, '{token}')
                                save_local_db()
                            break
                    except Exception as e:
                        logger.warning(f'API URL test attempt failed: {e}')
            if wait_msg_id:
                delete_message(chat_id, wait_msg_id)
            if parsed:
                total = min(3, len(parsed))
                send_message(chat_id, render_body_text(f'✅ <b>Connection Successful!</b>\n🎯 Top <b>{total}</b> messages — real format:'))
                for i, sample in enumerate(parsed[:3]):
                    num = sample['number']
                    msg = sample['message']
                    otp = sample['otp']
                    detected_app = detect_service(msg)
                    app_name = detected_app if detected_app else p.get('name', 'Unknown')
                    app_full_name, prem_app_html = get_service_info_html(app_name, msg)
                    display_num = f'+{num}' if not str(num).startswith('+') else str(num)
                    char, iso = get_flag_and_code(num)
                    country_full_name = _country_full_name_from_iso(iso)
                    clean_number = str(display_num).replace('+', '').replace(' ', '').strip()
                    flag_html = get_flag_info_html(clean_number)
                    otp_msg = render_body_text(f'<b>{flag_html} ({country_full_name.upper()}) 📱</b>\n➖➖➖➖➖➖➖➖➖➖\n📞 <b>NUMBER:</b> <code>{clean_number}</code>')
                    _reset_btn_counter()
                    kb = [[{'text': f'OTP {otp}', 'copy_text': {'text': str(otp)}, 'style': _rs()}]]
                    send_message(chat_id, otp_msg, reply_markup={'inline_keyboard': kb})
            elif p['type'] == 'Auto Captcha Panel':
                if p.get('api_base'):
                    send_message(chat_id, render_body_text(f"✅ <b>Connection Successful!</b>\n\n🔗 API: <code>{html.escape(p.get('api_base', ''))}/api/message-data-record</code>\n👤 User: <code>{html.escape(p.get('username', ''))}</code>\n\n⚠️ <b>No OTP message has been received yet.</b>\n<i>When a new SMS arrives in the panel, it will automatically be sent to the group.</i>"))
                else:
                    try:
                        soup = BeautifulSoup(raw_text, 'html.parser')
                        tables = soup.find_all('table')
                        if tables:
                            full_table_data = '🔍 FULL TABLE DATA (A-Z)\n' + '=' * 50 + '\n\n'
                            for t_idx, table in enumerate(tables):
                                full_table_data += f'--- Table {t_idx + 1} ---\n'
                                rows = table.find_all('tr')
                                for r_idx, row in enumerate(rows):
                                    cols = row.find_all(['th', 'td'])
                                    col_texts = [f"[{c_idx + 1}] {c.get_text(separator=' ', strip=True)}" for c_idx, c in enumerate(cols)]
                                    full_table_data += f"Row {r_idx + 1}: {' | '.join(col_texts)}\n"
                                full_table_data += '\n' + '=' * 50 + '\n'
                            send_document(chat_id, f'Full_Panel_Data_{idx}.txt', full_table_data.encode('utf-8'))
                            fail_txt = f"⚠️ <b>Connected, but couldn't parse OTP data!</b>\n\n<i>I have sent the complete (A-Z) data of that link in a Text File. Open the file and check the correct Column Number (e.g.: [1], [3]) then update in panel.</i>"
                            send_message(chat_id, render_body_text(fail_txt))
                        else:
                            send_message(chat_id, render_body_text(f'⚠️ <b>Connected, but no HTML Table found!</b>\nMake sure the message link is correct.'))
                    except Exception as e:
                        send_message(chat_id, render_body_text(f'❌ <b>Error parsing HTML:</b> {html.escape(str(e))}'))
            else:
                excerpt = raw_text[:600] if raw_text else ''
                if '\n' not in excerpt:
                    debug_raw = re.sub('(?<![a-zA-Z])nn(?![a-zA-Z])', '\n', excerpt)
                else:
                    debug_raw = excerpt
                safe_html = html.escape(str(debug_raw)[:400])
                diagnosis = ''
                if not raw_text:
                    diagnosis = '❌ No data was returned by the API (empty response).'
                else:
                    try:
                        test_data = json.loads(raw_text)
                        if isinstance(test_data, list) and test_data:
                            first = test_data[0]
                            if isinstance(first, list):
                                p_num_idx = int(p.get('num_col_idx', 2)) - 1
                                p_msg_idx = int(p.get('msg_col_idx', 3)) - 1
                                cols = len(first)
                                diagnosis = f"✅ JSON parse: OK ({len(test_data)} rows, {cols} columns per row)\n• Number column {p.get('num_col_idx', 2)} (index {p_num_idx}): <code>{html.escape(str(first[p_num_idx]) if p_num_idx < cols else 'OUT OF RANGE')}</code>\n• Message column {p.get('msg_col_idx', 3)} (index {p_msg_idx}): <code>{html.escape(str(first[p_msg_idx])[:80] if p_msg_idx < cols else 'OUT OF RANGE')}</code>\n• OTP found: <code>{html.escape(str(extract_otp_code(str(first[p_msg_idx]).replace('nn', chr(10))) or 'NOT FOUND'))}</code>"
                            elif isinstance(first, dict):
                                diagnosis = f'✅ JSON parse: OK ({len(test_data)} records, dict format)\n⚠️ OTP/Number fields were not found — check the key names.'
                            else:
                                diagnosis = f'⚠️ JSON parse: OK lekin format unknown ({type(first).__name__})'
                        elif isinstance(test_data, dict):
                            diagnosis = f'⚠️ JSON is an object (a list was expected) — check the API response structure.'
                        else:
                            diagnosis = f'⚠️ JSON parse: OK lekin empty list mili.'
                    except Exception as je:
                        diagnosis = f'❌ JSON parsing failed: <code>{html.escape(str(je)[:100])}</code>\n⚠️ The API is not returning JSON — check the URL/Token.'
                send_message(chat_id, render_body_text(f"⚠️ <b>Connected, but couldn't parse OTP data.</b>\n\n<b>Diagnosis:</b>\n{diagnosis}\n\n<b>Raw Data (excerpt):</b>\n<code>{safe_html}...</code>"))
        except Exception as e:
            if wait_msg_id:
                delete_message(chat_id, wait_msg_id)
            send_message(chat_id, render_body_text(f'❌ <b>Connection Failed!</b>\nError: {html.escape(str(e))}'))
    elif data == 'abhi_control':
        if chat_id in user_states:
            user_states.pop(chat_id, None)
        if chat_id in temp_data:
            temp_data.pop(chat_id, None)
        _show_abhi_panel(chat_id, msg_id)
    elif data == 'abhi_toggle_w':
        bot_settings['withdraw_on'] = not bot_settings['withdraw_on']
        save_local_db()
        _show_abhi_panel(chat_id, msg_id)
    elif data == 'manage_w_methods':
        _show_w_methods(chat_id, msg_id)
    elif data == 'add_wm':
        user_states[chat_id] = 'wait_for_add_wm'
        temp_data[chat_id] = {'msg_id': msg_id}
        edit_message(chat_id, msg_id, render_body_text('📝 Send the name of the new Withdrawal Method:'), reply_markup={'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'manage_w_methods', 'style': _rs()}]]})
    elif data.startswith('del_wm_'):
        if not is_admin(chat_id):
            answer_callback(call['id'], '❌ Admin only!', show_alert=True)
            return
        idx = _safe_int(data.split('_')[2] if len(data.split('_')) > 2 else -1)
        if 0 <= idx < len(bot_settings['w_methods']):
            del bot_settings['w_methods'][idx]
            save_local_db()
            answer_callback(call['id'], '✅ Method deleted!', show_alert=True)
            _show_w_methods(chat_id, msg_id)
        else:
            answer_callback(call['id'], '❌ Method not found!', show_alert=True)
    elif data.startswith('abhi_'):
        if not is_admin(chat_id):
            answer_callback(call['id'], '❌ Admin only!', show_alert=True)
            return
        key = data.replace('abhi_', '')
        key_map = {'min_w': 'min_withdraw', 'otp_r': 'otp_reward', 'ref_r': 'refer_reward', 'cool': 'cooldown', 'num_req': 'num_req', 'num_share': 'num_share', 'sup_link': 'support_link', 'w_group': 'w_group'}
        if key in key_map:
            temp_data[chat_id] = {'msg_id': msg_id, 'key': key_map[key]}
            user_states[chat_id] = 'set_abhi'
            _reset_btn_counter()
            cancel_kb = {'inline_keyboard': [[{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'cancel_abhi_edit', 'style': _rs()}]]}
            current_value = bot_settings.get(key_map[key], '')
            prompt_text = f'📝 Please send the new value for <code>{key_map[key]}</code>:'
            edit_message(chat_id, msg_id, render_body_text(prompt_text), reply_markup=cancel_kb)
            answer_callback(call['id'])
    elif data == 'add_cc_all' or data == 'rem_cc_all':
        session = user_active_sessions.get(chat_id)
        if not session or not session.get('nums'):
            answer_callback(call['id'], '❌ No active numbers found!', show_alert=True)
            return
        nums = session.get('nums', [])
        cc_codes = session.get('cc_codes', [])
        state = session.get('cc_state', [True] * len(nums))
        if len(state) < len(nums):
            state = list(state) + [True] * (len(nums) - len(state))
        want_add = data == 'add_cc_all'
        changed = False
        for i in range(len(nums)):
            cc = cc_codes[i] if i < len(cc_codes) else None
            if cc:
                new_state = want_add
                if state[i] != new_state:
                    state[i] = new_state
                    changed = True
        session['cc_state'] = state
        user_active_sessions[chat_id] = session
        kb = _rebuild_num_kb(chat_id)
        body = render_body_text(_build_num_text(chat_id))
        target_msg_id = session.get('msg_id', msg_id)
        try:
            edit_message(chat_id, target_msg_id, body, reply_markup={'inline_keyboard': kb})
        except Exception as e:
            logger.warning(f'Country-code toggle edit failed: {e}')
            answer_callback(call['id'], '❌ Could not update the numbers.', show_alert=True)
            return
        answer_callback(call['id'], '✅ Country code added.' if want_add else '✅ Country code removed.')
    elif data.startswith('g_s_'):
        service = data.split('g_s_')[1]
        local_cnts = set([b['country'] for b in number_batches.values() if b['service'] == service and b['numbers']])
        nexa_cnts = set(bot_settings.get('nexa_services', {}).get(service, {}).keys())
        voltx_cnts = set(bot_settings.get('voltx_services', {}).get(service, {}).keys())
        stex_cnts = set(bot_settings.get('stex_services', {}).get(service, {}).keys())
        all_countries = local_cnts.union(nexa_cnts).union(voltx_cnts).union(stex_cnts)
        c_msg = bot_settings['custom_messages'].get('select_country', {})
        raw_txt = c_msg.get('text', '📌 Select a country for {service}:').replace('{service}', service)
        txt = render_body_text(raw_txt)
        flags_db = bot_settings.get('premium_flags', {})
        _reset_btn_counter()
        kb = []
        DEFAULT_GLOBE = '5780471598922337683'
        for ci, c in enumerate(all_countries):
            emoji_id = _find_flag_emoji_id(c, flags_db)
            if emoji_id == DEFAULT_GLOBE and c in flags_db:
                emoji_id = flags_db[c].get('id', DEFAULT_GLOBE)
            if emoji_id == DEFAULT_GLOBE:
                for b_id, b_data in number_batches.items():
                    if b_data['service'] == service and b_data['country'] == c and b_data['numbers']:
                        first_num = b_data['numbers'][0]['num'].replace('+', '').replace(' ', '')
                        _, _, num_eid = get_flag_info_from_num(first_num)
                        if num_eid:
                            emoji_id = num_eid
                            break
            if emoji_id == DEFAULT_GLOBE:
                sorted_flag_codes = sorted(flags_db.keys(), key=len, reverse=True)
                for svc_ranges in [bot_settings.get('nexa_services', {}).get(service, {}), bot_settings.get('voltx_services', {}).get(service, {}), bot_settings.get('stex_services', {}).get(service, {})]:
                    if c not in svc_ranges:
                        continue
                    for rng in svc_ranges[c]:
                        rng_clean = rng.replace('X', '').replace('x', '')
                        for code in sorted_flag_codes:
                            if rng_clean.startswith(code) and 'id' in flags_db[code]:
                                emoji_id = flags_db[code]['id']
                                break
                        if emoji_id != DEFAULT_GLOBE:
                            break
                    if emoji_id != DEFAULT_GLOBE:
                        break
            _country_rate = _get_country_batch_rate(service, c)
            _flag_char = '🌍'
            _c_upper = str(c).upper()
            if c in flags_db:
                _fd = flags_db.get(c, {})
                _flag_char = _fd.get('char') or _unicode_flag(_fd.get('iso', '')) or '🌍'
            else:
                for _fd in flags_db.values():
                    _iso = str(_fd.get('iso', '')).upper()
                    _name = str(_fd.get('name', '')).upper()
                    if _c_upper == _iso or _c_upper == _name or _c_upper in _name or (_name in _c_upper):
                        _flag_char = _fd.get('char') or _unicode_flag(_iso) or '🌍'
                        break
            _country_text = f'{c}  {_format_rate(_country_rate)}৳' if _country_rate is not None else f'{c}'
            kb.append([{'text': _country_text, 'icon_custom_emoji_id': emoji_id, 'callback_data': f'g_c_{service}_{c}', 'style': _rs()}])
        _append_custom_btns(kb, c_msg)
        kb.append([{'text': 'Back', 'icon_custom_emoji_id': '5267490665117275176', 'callback_data': 'get_number_menu', 'style': _rs()}])
        edit_message(chat_id, msg_id, txt, reply_markup={'inline_keyboard': kb})
        answer_callback(call['id'])
    elif data == 'get_number_menu':
        all_services, txt, kb = _build_services_keyboard('get_number')
        if not all_services:
            answer_callback(call['id'], '❌ No services available!', show_alert=True)
            return
        edit_message(chat_id, msg_id, txt, reply_markup={'inline_keyboard': kb})
        answer_callback(call['id'])
    elif data.startswith('g_c_') or data.startswith('c_n_'):
        now = time.time()
        if now - user_cooldowns.get(chat_id, 0) < bot_settings['cooldown']:
            answer_callback(call['id'], f"⌛ Please wait {int(bot_settings['cooldown'] - (now - user_cooldowns.get(chat_id, 0)))}s.", show_alert=True)
            return
        user_cooldowns[chat_id] = now
        expire_previous_number(chat_id)
        if data.startswith('c_n_s_'):
            parts_s = data.split('_')
            query = parts_s[3]
            _svc = parts_s[4] if len(parts_s) > 4 else ''
            service_from_cb = _svc if _svc else None
            allowed_countries = bot_settings.get('nexa_search_countries', []) + bot_settings.get('voltx_search_countries', []) + bot_settings.get('stex_search_countries', [])
            if allowed_countries:
                clean_allowed = [c.replace('X', '').replace('x', '') for c in allowed_countries]
                if not any((query.startswith(c) or c.startswith(query) for c in clean_allowed if c)):
                    answer_callback(call['id'], '❌ This country code is not allowed for search!', show_alert=True)
                    return
            wait_msg_id = msg_id
            found_indices = _search_and_recycle_local(query, chat_id)
            fetched_nums = []
            if not found_indices:
                _api_num, _api_panel = _fetch_number_via_panels(query, chat_id)
                if _api_num:
                    fetched_nums.append(_api_num)
                    save_local_db()
                else:
                    answer_callback(call['id'], '❌ Number out of stock!', show_alert=True)
                    delete_message(chat_id, wait_msg_id)
                    return
            else:
                random.shuffle(found_indices)
                for b_id, idx in found_indices:
                    if len(fetched_nums) >= bot_settings.get('num_req', 1):
                        break
                    if b_id not in number_batches:
                        continue
                    nb = number_batches[b_id]['numbers']
                    if idx < 0 or idx >= len(nb):
                        continue
                    n_obj = nb[idx]
                    num_str = n_obj['num']
                    fetched_nums.append(num_str)
                    n_obj['shares'] += 1
                    n_obj['used_by'].append(chat_id)
                    with _stats_lock:
                        total_assigned_stats += 1
                    if n_obj['shares'] >= bot_settings.get('num_share', 1):
                        if num_str not in used_numbers_list:
                            used_numbers_list.append(num_str)
                save_local_db()
            user_active_sessions[chat_id] = {'msg_id': wait_msg_id, 'nums': fetched_nums, 'service': service_from_cb or '', 'country': '', 'ctx': 'search', 'query': query, 'cc_codes': _build_cc_codes(fetched_nums), 'cc_state': [True] * len(fetched_nums)}
            user_otp_delivery_active[chat_id] = True
            kb = _rebuild_num_kb(chat_id)
            num_text = render_body_text(_build_num_text(chat_id))
            try:
                edit_message(chat_id, wait_msg_id, num_text, reply_markup={'inline_keyboard': kb})
            except Exception:
                msg_res = send_message(chat_id, num_text, reply_markup={'inline_keyboard': kb})
                if msg_res and msg_res.get('ok') and msg_res.get('result'):
                    user_active_sessions[chat_id]['msg_id'] = msg_res['result']['message_id']
            try:
                answer_callback(call['id'])
            except Exception as e:
                logger.warning(f'Error: {e}')
            return
        _cb_sfx = data[4:]
        service, _, country = _cb_sfx.partition('_')
        if not service or not country:
            answer_callback(call['id'], '❌ Invalid selection!', show_alert=True)
            return
        available_indices = []
        for b_id, b_data in number_batches.items():
            if b_data['service'] == service and b_data['country'] == country:
                for idx, n_obj in enumerate(b_data['numbers']):
                    if chat_id not in n_obj.get('used_by', []):
                        available_indices.append((b_id, idx))
        if not available_indices:
            has_matching = False
            for b_id, b_data in number_batches.items():
                if b_data['service'] == service and b_data['country'] == country:
                    for n_obj in b_data['numbers']:
                        has_matching = True
                        n_obj['shares'] = 0
                        n_obj['used_by'] = []
            if has_matching:
                for b_id, b_data in number_batches.items():
                    if b_data['service'] == service and b_data['country'] == country:
                        for idx, n_obj in enumerate(b_data['numbers']):
                            available_indices.append((b_id, idx))
        fetched_nums = []

        # First use local stock, then keep requesting API numbers until NUM/REQ is reached.
        # The previous code stopped after the first API number, so NUM/REQ=3 still returned 1.
        target_count = max(1, int(bot_settings.get('num_req', 1) or 1))
        if available_indices:
            random.shuffle(available_indices)
            for b_id, idx in available_indices:
                if len(fetched_nums) >= target_count:
                    break
                if b_id not in number_batches:
                    continue
                nb = number_batches[b_id]['numbers']
                if idx < 0 or idx >= len(nb):
                    continue
                n_obj = nb[idx]
                fetched_nums.append(n_obj['num'])
                with _data_lock:
                    n_obj['shares'] += 1
                    n_obj['used_by'].append(chat_id)
                    if n_obj['shares'] >= bot_settings.get('num_share', 1):
                        if n_obj['num'] not in used_numbers_list:
                            used_numbers_list.append(n_obj['num'])
                with _stats_lock:
                    total_assigned_stats += 1

        # API/Auto Mode fills the remaining NUM/REQ slots.
        while len(fetched_nums) < target_count:
            _api_num = None
            if bot_settings.get('nexa_on', False):
                _ns = bot_settings.get('nexa_services', {}).get(service, {}).get(country, [])
                if _ns:
                    _rng = random.choice(_ns)
                    _api_num, _ = try_nexa_get_number(_rng, chat_id, allow_auto=True)
            if not _api_num and bot_settings.get('voltx_on', False):
                _vs = bot_settings.get('voltx_services', {}).get(service, {}).get(country, [])
                if _vs:
                    _rng = random.choice(_vs)
                    _api_num, _ = try_voltx_get_number(_rng.replace('X', '').replace('x', ''), chat_id, allow_auto=True)
            if not _api_num and bot_settings.get('stex_on', False):
                _ss = bot_settings.get('stex_services', {}).get(service, {}).get(country, [])
                if _ss:
                    _rng = random.choice(_ss)
                    _api_num, _ = try_stex_get_number(_rng.replace('X', '').replace('x', ''), chat_id, allow_auto=True)

            if not _api_num:
                _fallback_query = ''.join(ch for ch in str(country) if ch.isdigit())
                if not _fallback_query:
                    _cf = bot_settings.get('premium_flags', {})
                    _cl = str(country).strip().upper()
                    for _cc, _fd in _cf.items():
                        if _cl in {str(_cc).upper(), str(_fd.get('iso', '')).upper(), str(_fd.get('name', '')).upper()}:
                            _fallback_query = ''.join(ch for ch in str(_cc) if ch.isdigit())
                            break
                if _fallback_query:
                    _api_num, _api_panel = _fetch_number_via_panels(_fallback_query, chat_id, force_auto=True)

            if not _api_num:
                break
            if str(_api_num) not in [str(x) for x in fetched_nums]:
                fetched_nums.append(_api_num)
            else:
                # Avoid an infinite loop if an API keeps returning the same number.
                break

        save_local_db()
        if not fetched_nums:
            answer_callback(call['id'], '❌ Number out of stock or range missing!', show_alert=True)
            if data.startswith('c_n_'):
                delete_message(chat_id, msg_id)
            return

        _rate_by_num = {}
        # Rates/session are built from the complete NUM/REQ result set.
        _rate_by_num = {}
        for _n in fetched_nums:
            _clean_n = str(_n).replace('+', '').replace(' ', '').replace('-', '').strip()
            _rate_by_num[_clean_n] = _get_manual_batch_rate(_n)
        if _rate_by_num[_clean_n] in (None, 0, 0.0):
            _rate_by_num[_clean_n] = bot_settings.get('otp_reward', 0.0)
        _sess_reg = {'msg_id': msg_id, 'nums': fetched_nums, 'service': service, 'country': country, 'ctx': 'regular', 'rate_by_num': _rate_by_num, 'rates': [_rate_by_num.get(str(_n).replace('+', '').replace(' ', '').replace('-', '').strip(), 0.0) for _n in fetched_nums], 'cc_codes': _build_cc_codes(fetched_nums), 'cc_state': [True] * len(fetched_nums)}
        user_active_sessions[chat_id] = _sess_reg
        user_otp_delivery_active[chat_id] = True
        kb = _rebuild_num_kb(chat_id)
        text_numbers = render_body_text(_build_num_text(chat_id))
        try:
            edit_message(chat_id, msg_id, text_numbers, reply_markup={'inline_keyboard': kb})
        except Exception as e:
            msg_res = send_message(chat_id, text_numbers, reply_markup={'inline_keyboard': kb})
            if msg_res and msg_res.get('ok') and msg_res.get('result'):
                user_active_sessions[chat_id]['msg_id'] = msg_res['result']['message_id']
        try:
            answer_callback(call['id'])
        except Exception as e:
            logger.warning(f'Error: {e}')
    elif data.startswith('add_cc_') or data.startswith('rem_cc_'):
        session = user_active_sessions.get(chat_id, {})
        if not session:
            answer_callback(call['id'], '❌ Session expired. Please get a new number.', show_alert=True)
            return
        nums = session.get('nums', [])
        cc_state = list(session.get('cc_state', [True] * len(nums)))
        while len(cc_state) < len(nums):
            cc_state.append(True)
        suffix = data.split('_')[-1]
        if suffix == 'all':
            new_val = data.startswith('add_cc_')
            cc_state = [new_val] * len(cc_state)
        else:
            try:
                idx = int(suffix)
            except Exception:
                answer_callback(call['id'])
                return
            if data.startswith('add_cc_'):
                if idx < len(cc_state):
                    cc_state[idx] = True
            elif idx < len(cc_state):
                cc_state[idx] = False
        session['cc_state'] = cc_state
        user_active_sessions[chat_id] = session
        kb = _rebuild_num_kb(chat_id)
        num_text = render_body_text(_build_num_text(chat_id))
        try:
            edit_message(chat_id, session['msg_id'], num_text, reply_markup={'inline_keyboard': kb})
        except Exception as e:
            logger.warning(f'CC toggle edit error: {e}')
        try:
            answer_callback(call['id'])
        except Exception:
            pass
    elif data.startswith('dapp_') or data.startswith('drej_'):
        user_id_clicked = call.get('from', {}).get('id', 0)
        if not is_admin(user_id_clicked):
            answer_callback(call['id'], '🚫 Only Bot Admins can process deposits!', show_alert=True)
            return
        action = 'APPROVE' if data.startswith('dapp_') else 'REJECT'
        req_id = data.replace('dapp_', '').replace('drej_', '')
        if req_id not in pending_withdrawals:
            answer_callback(call['id'], '❌ Request already processed!', show_alert=True)
            return
        req_data = pending_withdrawals[req_id]
        u_id = req_data['user_id']
        amt = req_data['amount']
        txn_id = req_data.get('txn_id', '')
        full_name = req_data.get('full_name', u_id)
        status_text = 'APPROVED' if action == 'APPROVE' else 'REJECTED'
        emoji_icon_id = '6266967801580231067' if action == 'APPROVE' else '6267237615720731788'
        new_text = f"💰 <b>DEPOSIT {status_text}</b>\n\n👤 <b>USER:</b> <a href='tg://user?id={u_id}'>{full_name}</a>\n💵 <b>AMOUNT:</b> {amt:g}৳\n🆔 <b>TXN ID:</b> <code>{txn_id}</code>\n\n🧾 <b>REQ ID:</b> {req_id}\n👨‍⚖️ <b>PROCESSED BY ADMIN</b>"
        rendered_new_text = render_body_text(new_text)
        _reset_btn_counter()
        status_kb = {'inline_keyboard': [[{'text': status_text, 'icon_custom_emoji_id': emoji_icon_id, 'callback_data': 'ignore', 'style': 'success' if action == 'APPROVE' else 'danger'}]]}
        for sm in req_data.get('sent_messages', []):
            try:
                edit_message(sm['chat_id'], sm['message_id'], rendered_new_text, reply_markup=status_kb)
            except Exception as e:
                logger.warning(f'Deposit status edit error: {e}')
        try:
            edit_message(chat_id, msg_id, rendered_new_text, reply_markup=status_kb)
        except Exception as e:
            logger.warning(f'Deposit status edit error: {e}')
        safe_uid = int(u_id) if str(u_id).lstrip('-').isdigit() else u_id
        if action == 'APPROVE':
            update_balance(safe_uid, amt)
            try:
                send_message(safe_uid, render_body_text(f"{PEM['ok']} <b>Deposit Approved!</b>\n\n💵 <b>Amount:</b> {amt:g}৳\n💰 <b>New Balance:</b> {_get_local_user(safe_uid).get('balance', 0.0):g}৳\n\nThank you!"))
            except Exception as e:
                logger.warning(f'Deposit approve notify error: {e}')
        else:
            try:
                send_message(safe_uid, render_body_text(f"❌ <b>Deposit Rejected!</b>\n\n💵 <b>Amount:</b> {amt:g}৳\n🆔 <b>TXN ID:</b> <code>{txn_id}</code>\n\nIf this was a mistake, please contact support."))
            except Exception as e:
                logger.warning(f'Deposit reject notify error: {e}')
        _update_local_withdrawal(req_id, {'status': 'approved' if action == 'APPROVE' else 'rejected'})
        del pending_withdrawals[req_id]
            
    elif data.startswith('wapp_') or data.startswith('wrej_'):
        user_id_clicked = call.get('from', {}).get('id', 0)
        if not is_admin(user_id_clicked):
            answer_callback(call['id'], '🚫 Only Bot Admins can process withdrawals!', show_alert=True)
            return
        action = 'APPROVE' if data.startswith('wapp_') else 'REJECT'
        req_id = data.replace('wapp_', '').replace('wrej_', '')
        if req_id in pending_withdrawals:
            req_data = pending_withdrawals[req_id]
            u_id, amt = (req_data['user_id'], req_data['amount'])
            num = req_data['number']
            full_name = req_data.get('full_name', u_id)
            if action == 'APPROVE' and len(num) >= 7:
                masked_num = mask_number(num, user_id=u_id)
            else:
                masked_num = num
            status_text = 'APPROVED' if action == 'APPROVE' else 'REJECTED'
            emoji_icon_id = '6266967801580231067' if action == 'APPROVE' else '6267237615720731788'
            new_text = f"🎙 <b>WITHDRAWAL {status_text}</b>\n\n👤 <b>USER:</b> <a href='tg://user?id={u_id}'>{full_name}</a>\n💳 <b>WITHDRAWAL:</b> {amt}৳\n🍏 <b>NUMBER:</b> <code>{masked_num}</code>\n🏦 <b>METHOD:</b> {req_data['method']}\n\n🧾 <b>REQ ID:</b> {req_id}\n👨\u200d⚖️ <b>PROCESSED BY ADMIN</b>"
            rendered_new_text = render_body_text(new_text)
            _reset_btn_counter()
            status_kb = {'inline_keyboard': [[{'text': status_text, 'icon_custom_emoji_id': emoji_icon_id, 'callback_data': 'ignore', 'style': 'success' if action == 'APPROVE' else 'danger'}]]}
            for sm in req_data.get('sent_messages', []):
                try:
                    edit_message(sm['chat_id'], sm['message_id'], rendered_new_text, reply_markup=status_kb)
                except Exception as e:
                    logger.warning(f'Error: {e}')
            try:
                edit_message(chat_id, msg_id, rendered_new_text, reply_markup=status_kb)
            except Exception as e:
                logger.warning(f'Error: {e}')
            safe_uid = int(u_id) if str(u_id).lstrip('-').isdigit() else u_id
            if action == 'REJECT':
                update_balance(safe_uid, amt)
                try:
                    send_message(safe_uid, render_body_text(f'❌ Your {amt}৳ withdrawal request was rejected. Balance refunded.'))
                except Exception as _e:
                    logger.warning(f'Withdrawal reject notify failed for {u_id}: {_e}')
            else:
                try:
                    send_message(safe_uid, render_body_text(f"{PEM['ok']} Your {amt}৳ withdrawal request has been paid successfully!"))
                except Exception as _e:
                    logger.warning(f'Withdrawal approve notify failed for {u_id}: {_e}')
            _update_local_withdrawal(req_id, {'status': 'approved' if action == 'APPROVE' else 'rejected'})
            del pending_withdrawals[req_id]
        else:
            answer_callback(call['id'], '❌ Request already processed!', show_alert=True)

def poll_otp_with_status(number_id, num_str, owner_id, api_key):
    headers = {'X-API-Key': api_key}
    first_iter = True
    for _ in range(150):
        try:
            res = _nexa_session.get(f'{NEXA_BASE_URL}/api/v1/numbers/{number_id}/sms', headers=headers, timeout=10)
            try:
                data = res.json()
            except Exception:
                logger.warning(f'Nexa OTP poll: invalid JSON response — {res.text[:120]!r}')
                first_iter = False
                time.sleep(2)
                continue
            sms_list = []
            if data.get('success'):
                if data.get('otp'):
                    sms_list = [{'otp': data.get('otp'), 'message': data.get('message', ''), 'service': data.get('service', ''), 'app_name': data.get('app_name', '')}]
                elif isinstance(data.get('data'), list) and data['data']:
                    sms_list = data['data']
                elif isinstance(data.get('sms'), list) and data['sms']:
                    sms_list = data['sms']
            for sms_item in sms_list:
                otp = str(sms_item.get('otp') or sms_item.get('code') or '')
                msg_text = str(sms_item.get('message') or sms_item.get('sms') or sms_item.get('text') or f'Your code is {otp}')
                if not otp:
                    continue
                extracted_otp = extract_otp_code(msg_text)
                if extracted_otp and len(extracted_otp) > len(otp):
                    otp = extracted_otp
                app_name = sms_item.get('service') or sms_item.get('app_name') or sms_item.get('app') or 'Nexa Service'
                detected_app = detect_service(msg_text)
                if detected_app:
                    app_name = detected_app
                ts_str = str(sms_item.get('received_at') or sms_item.get('created_at') or sms_item.get('sms_time') or sms_item.get('date') or sms_item.get('timestamp') or sms_item.get('createdAt') or '')
                if ts_str and _is_stale_otp(ts_str):
                    continue
                unique_id = f'POLL_{number_id}_{otp}'
                if _is_processed(unique_id):
                    continue
                _add_to_processed(unique_id)
                if first_iter:
                    continue
                _record_and_deliver_otp(owner_id, num_str, app_name, msg_text, otp, num_str, 'poll_otp_nexa')
                break
        except Exception as e:
            logger.warning(f'poll_otp_with_status iteration error: {e}')
        first_iter = False
        time.sleep(2)

def _poll_mauthapi_otp_single(prefix, base_url, default_name, num_str, owner_id, api_key):
    """Shared per-number OTP poller for VoltX and Stex (same mauthapi platform).
    prefix: 'VX' for VoltX, 'STX' for Stex — used for processed_otps deduplication."""
    headers = {'mauthapi': api_key, 'User-Agent': 'Mozilla/5.0'}
    clean_target = str(num_str).replace('+', '').replace(' ', '').replace('-', '').strip()
    first_iter = False
    for _ in range(300):
        try:
            _ms2 = _voltx_session if base_url == VOLTX_BASE_URL else _stex_session
            res = _ms2.get(f'{base_url}/success-otp', headers=headers, timeout=6)
            try:
                data = res.json()
            except Exception:
                logger.warning(f'{prefix} OTP poll: invalid JSON — {res.text[:120]!r}')
                first_iter = False
                time.sleep(2)
                continue
            resp_data = data.get('data', {})
            if isinstance(resp_data, dict):
                otps_list = resp_data.get('otps', [])
            elif isinstance(resp_data, list):
                otps_list = resp_data
            else:
                otps_list = data if isinstance(data, list) else []
            if not isinstance(otps_list, list):
                first_iter = False
                time.sleep(2)
                continue
            for otp_entry in otps_list:
                entry_num = str(otp_entry.get('no_plus_number') or otp_entry.get('full_number') or otp_entry.get('phone_number') or otp_entry.get('number') or '').replace('+', '').replace(' ', '').replace('-', '').strip()
                if not entry_num:
                    continue
                if entry_num == clean_target or (len(entry_num) >= 8 and entry_num.endswith(clean_target[-8:])) or (len(clean_target) >= 8 and clean_target.endswith(entry_num[-8:])):
                    msg_text = otp_entry.get('message', otp_entry.get('sms', otp_entry.get('msg', '')))
                    if not msg_text:
                        continue
                    extracted_otp = extract_otp_code(msg_text)
                    if not extracted_otp:
                        continue
                    otp_id = otp_entry.get('otp_id', '')
                    ts_str = str(otp_entry.get('received_at') or otp_entry.get('created_at') or otp_entry.get('sms_time') or otp_entry.get('date') or otp_entry.get('timestamp') or otp_entry.get('createdAt') or '')
                    if ts_str and _is_stale_otp(ts_str):
                        continue
                    unique_id = f'{prefix}_{otp_id}' if otp_id else f'{prefix}_{clean_target}_{extracted_otp}'
                    if _is_processed(unique_id):
                        continue
                    _add_to_processed(unique_id)
                    if first_iter:
                        continue
                    app_name = detect_service(msg_text) or default_name
                    _record_and_deliver_otp(owner_id, num_str, app_name, msg_text, extracted_otp, clean_target, f'{prefix}_poll')
                    return
        except Exception as e:
            logger.warning(f'{prefix}_poll_otp iteration error: {e}')
        first_iter = False
        time.sleep(2)

def voltx_poll_otp(num_str, owner_id, api_key):
    """VoltX per-number OTP poller — thin wrapper around _poll_mauthapi_otp_single."""
    _poll_mauthapi_otp_single('VX', VOLTX_BASE_URL, 'VoltX SMS', num_str, owner_id, api_key)

def stex_poll_otp(num_str, owner_id, api_key):
    """Stex per-number OTP poller — thin wrapper around _poll_mauthapi_otp_single."""
    _poll_mauthapi_otp_single('STX', STEX_BASE_URL, 'Stex SMS', num_str, owner_id, api_key)

def _poll_mauthapi_otps(api_keys, base_url, prefix, default_name, first_run):
    """Shared helper for Stex and VoltX global SMS listeners.
    Both use the same mauthapi platform — same header, same response envelope.
    prefix: 'STX' for Stex, 'VX' for VoltX (used to deduplicate processed OTP IDs)."""
    for api_key in api_keys:
        try:
            headers = {'mauthapi': api_key, 'User-Agent': 'Mozilla/5.0'}
            _ms3 = _voltx_session if base_url == VOLTX_BASE_URL else _stex_session
            res = _ms3.get(f'{base_url}/success-otp', headers=headers, timeout=10)
            try:
                data = res.json()
            except Exception:
                logger.warning(f'global_sms {prefix}: invalid JSON — {res.text[:120]!r}')
                continue
            resp_data = data.get('data', {})
            if isinstance(resp_data, dict):
                otps_list = resp_data.get('otps', [])
            elif isinstance(resp_data, list):
                otps_list = resp_data
            else:
                otps_list = []
            for item in otps_list:
                num = str(item.get('no_plus_number') or item.get('full_number') or item.get('phone_number') or item.get('number') or '').replace('+', '')
                msg_text = str(item.get('message', item.get('sms', item.get('msg', ''))))
                app_name = detect_service(msg_text) or default_name
                otp = extract_otp_code(msg_text) or 'CODE'
                otp_id = item.get('otp_id', '')
                ts_str = str(item.get('received_at') or item.get('created_at') or item.get('sms_time') or item.get('date') or item.get('timestamp') or item.get('createdAt') or '')
                if ts_str and _is_stale_otp(ts_str):
                    continue
                if otp_id:
                    unique_id = f'{prefix}_{otp_id}'
                    dedup_window = 604800
                    warmup_id = None
                else:
                    unique_id = f'{prefix}_{num}_{otp}'
                    dedup_window = 10
                    warmup_id = f'WARMUP_{unique_id}'
                if warmup_id and _is_processed(warmup_id, window=90000):
                    continue
                if not _is_processed(unique_id, window=dedup_window) and num:
                    _add_to_processed(unique_id)
                    if first_run:
                        if warmup_id:
                            _add_to_processed(warmup_id)
                        continue
                    if warmup_id:
                        _add_to_processed(warmup_id)
                    clean_api_num = str(num).replace('+', '').replace(' ', '').replace('-', '').strip()
                    found_owners = _find_otp_owners(clean_api_num)
                    owner_id = found_owners[0] if found_owners else None
                    _record_and_deliver_otp(owner_id, num, app_name, msg_text, otp, clean_api_num, f'global_sms_{prefix}')
                    with _data_lock:
                        if len(otp_received_numbers) > _OTP_RECV_MAX:
                            keep = set(list(otp_received_numbers)[10000:])
                            otp_received_numbers.clear()
                            otp_received_numbers.update(keep)
        except Exception as e:
            logger.warning(f'global_sms {prefix} key loop error: {e}')
            continue

def _poll_nexa_global_otps(api_keys, warmup):
    """Nexa global SMS listener — same warmup/dedup/deliver shape as
    _poll_mauthapi_otps, ab isi jagah extract kiya hai taaki logic global_sms_listener
    ke andar dobara (duplicate) na likhna pade. Sirf Nexa ka response-shape/endpoint
    fallback (sms/latest → sms/recent) alag hai, baaki dedup/warmup/delivery pattern same hai."""
    for api_key in api_keys:
        try:
            headers = {'X-API-Key': api_key}
            try:
                res = _nexa_session.get(f'{NEXA_BASE_URL}/api/v1/sms/latest', headers=headers, timeout=10)
                data = res.json()
            except Exception as e:
                logger.warning(f'Nexa sms/latest fetch error: {e}')
                try:
                    res = _nexa_session.get(f'{NEXA_BASE_URL}/api/v1/sms/recent', headers=headers, timeout=10)
                    data = res.json()
                except Exception as e2:
                    logger.warning(f'Nexa sms/recent also failed: {e2}')
                    data = {}
            if not (data.get('success') and 'data' in data):
                continue
            raw_items = data['data']
            if isinstance(raw_items, dict):
                raw_items = list(raw_items.values()) if raw_items else []
            for item in raw_items if isinstance(raw_items, list) else []:
                num = str(item.get('number', '')).replace('+', '')
                msg_text = str(item.get('sms') or item.get('message') or item.get('text') or '')
                app_name = item.get('app_name', 'Unknown')
                detected_app = detect_service(msg_text)
                if detected_app:
                    app_name = detected_app
                otp = extract_otp_code(msg_text) or 'CODE'
                sms_id = item.get('id', '')
                ts_str = str(item.get('received_at') or item.get('created_at') or item.get('sms_time') or item.get('date') or item.get('timestamp') or item.get('createdAt') or '')
                if ts_str and _is_stale_otp(ts_str):
                    continue
                if sms_id:
                    unique_id = f'NEXA_{num}_{sms_id}'
                    dedup_window = 604800
                    warmup_id = None
                else:
                    unique_id = f'NEXA_{num}_{otp}'
                    dedup_window = 10
                    warmup_id = f'WARMUP_{unique_id}'
                if warmup_id and _is_processed(warmup_id, window=90000):
                    continue
                if not _is_processed(unique_id, window=dedup_window) and num:
                    _add_to_processed(unique_id)
                    if warmup:
                        if warmup_id:
                            _add_to_processed(warmup_id)
                        continue
                    if warmup_id:
                        _add_to_processed(warmup_id)
                    clean_api_num = str(num).replace('+', '').replace(' ', '').replace('-', '').strip()
                    found_owners = _find_otp_owners(clean_api_num)
                    owner_id = found_owners[0] if found_owners else None
                    _record_and_deliver_otp(owner_id, num, app_name, msg_text, otp, clean_api_num, 'global_sms_nexa')
                    with _data_lock:
                        if len(otp_received_numbers) > _OTP_RECV_MAX:
                            keep = set(list(otp_received_numbers)[10000:])
                            otp_received_numbers.clear()
                            otp_received_numbers.update(keep)
        except Exception as e:
            logger.warning(f'global_sms nexa key loop error: {e}')
            continue

def global_sms_listener():
    """External provider listener disabled; local bot features continue normally."""
    return


def flush_old_updates():
    """Skip all pending Telegram updates so old messages are not reprocessed on restart."""
    try:
        res = api_call('getUpdates?offset=-1&timeout=0')
        if res and res.get('ok') and res.get('result') and (len(res['result']) > 0):
            last_id = res['result'][-1].get('update_id', 0)
            if last_id:
                api_call(f'getUpdates?offset={last_id + 1}&timeout=0')
            logger.info(f'Flushed old Telegram updates (last_id={last_id})')
        else:
            logger.info('No pending Telegram updates to flush.')
    except Exception as e:
        logger.warning(f'Could not flush old updates: {e}')

def _panel_session_cleanup():
    """Background thread: close & remove stale panel_sessions every 10 minutes."""
    while True:
        time.sleep(600)
        try:
            active_indices = set(range(len(bot_settings.get('panels', []))))
            stale = [k for k in list(panel_sessions.keys()) if k not in active_indices]
            for k in stale:
                sess = panel_sessions.pop(k, None)
                if sess:
                    try:
                        sess.close()
                    except Exception as close_err:
                        logger.warning(f'panel_session close error for key {k}: {close_err}')
            if stale:
                logger.info(f'Cleaned {len(stale)} stale panel session(s).')
        except Exception as e:
            logger.warning(f'panel_session_cleanup error: {e}')

def main():
    global BOT_USERNAME
    res = api_call('getMe')
    if res.get('ok'):
        BOT_USERNAME = res['result']['username']
    logger.info(f'Bot is starting... @{BOT_USERNAME}')
    _load_processed_otps()
    flush_old_updates()
    threading.Thread(target=automatic_backup_loop, daemon=True).start()
    threading.Thread(target=panel_monitor_thread, daemon=True).start()
    threading.Thread(target=global_sms_listener, daemon=True).start()
    threading.Thread(target=_panel_session_cleanup, daemon=True).start()
    threading.Thread(target=_cleanup_loop, daemon=True).start()
    logger.info('Background APIs & Global SMS Listener Started!')
    sync_users_list()
    online_msg = '📢 <b>GOOD NEWS</b>\n➖➖➖➖➖➖➖➖\n✅ <b>THE BOT IS ONLINE</b>'
    for user_id in list(all_known_users):
        try:
            send_message(user_id, render_body_text(online_msg))
            time.sleep(0.05)
        except Exception as e:
            logger.warning(f'Online message failed for {user_id}: {e}')
    logger.info('Online broadcast sent to all known users.')
    executor = ThreadPoolExecutor(max_workers=50)
    offset = None
    while True:
        try:
            offset_param = f'&offset={offset}' if offset is not None else ''
            updates = api_call(f'getUpdates?timeout=30{offset_param}')
            if updates and updates.get('ok') and ('result' in updates) and isinstance(updates['result'], list):
                for update in updates['result']:
                    offset = update.get('update_id', (offset or 1) - 1) + 1
                    if 'message' in update:
                        try:
                            executor.submit(handle_message, update['message'])
                        except Exception as submit_err:
                            logger.warning(f'Executor submit error (message): {submit_err}')
                    elif 'callback_query' in update:
                        try:
                            executor.submit(handle_callback, update['callback_query'])
                        except Exception as submit_err:
                            logger.warning(f'Executor submit error (callback): {submit_err}')
            elif updates and (not updates.get('ok')):
                err_code = updates.get('error_code', 0)
                err_desc = updates.get('description', 'Unknown error')
                logger.warning(f'Telegram API error {err_code}: {err_desc}')
                if err_code == 409:
                    logger.error('CONFLICT: Another bot instance is running! Shutting down.')
                    break
                time.sleep(5)
        except Exception as e:
            logger.error(f'Main polling error: {e}')
            time.sleep(2)
if __name__ == '__main__':
    main()