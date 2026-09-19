# ============================================================================
#  ORANGE CARRIER CALL MONITOR
# ----------------------------------------------------------------------------
#  Monitors live calls on OrangeCarrier dashboard, downloads call recordings,
#  converts them to MP3, and forwards them to a Telegram group in real time.
#
#  Author  : NOYON018641
#  Version : 3.0.1 (Codespaces Optimized Edition)
#  License : Private / Unauthorized redistribution prohibited
# ============================================================================

import os
import re
import time
import logging
import subprocess
from datetime import datetime
from pathlib import Path

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

# ============================================================================
#  CONFIGURATION — EDIT THESE VALUES
# ============================================================================
ORANGE_USER  = "bknoyon303@gmail.com"        # ← আপনার OrangeCarrier ইমেইল
ORANGE_PASS  = "@NOYONNN"                    # ← আপনার OrangeCarrier পাসওয়ার্ড
BOT_TOKEN    = "8620616310:AAEobi-Df10n6_9Wg2lVqog4jXdAWhMUVXo" # ← Bot Token
CHAT_ID      = "-1003248114503"              # ← Telegram গ্রুপের Chat ID

DEVELOPER    = "NOYON018641"                 # ← আপনার Telegram username
NUMBER_URL   = "https://t.me/TrafficJunction999"  # ← নম্বর চ্যানেলের লিংক
REFRESH_MIN  = 30                            # ← কত মিনিট পরপর পেজ রিফ্রেশ

# ============================================================================
#  VALIDATION
# ============================================================================
_missing = []
if not ORANGE_USER:  _missing.append("ORANGE_USER")
if not ORANGE_PASS or ORANGE_PASS.startswith("YOUR-"):  _missing.append("ORANGE_PASS")
if not BOT_TOKEN   or BOT_TOKEN.startswith("YOUR-"):    _missing.append("BOT_TOKEN")
if not CHAT_ID:    _missing.append("CHAT_ID")

if _missing:
    raise SystemExit(
        f"\n❌ Please fill in the following values in bot.py:\n   "
        + ", ".join(_missing)
        + "\n\n"
    )

BASE_DIR = Path(__file__).resolve().parent

# ============================================================================
#  COUNTRY DATA — name → ISO code, ISO code → flag emoji
# ============================================================================
COUNTRY_NAME_TO_CODE = {
    "BANGLADESH": "BD", "INDIA": "IN", "PAKISTAN": "PK", "NEPAL": "NP",
    "SRI LANKA": "LK", "UNITED STATES": "US", "UNITED KINGDOM": "GB",
    "CANADA": "CA", "AUSTRALIA": "AU", "GERMANY": "DE", "FRANCE": "FR",
    "ITALY": "IT", "SPAIN": "ES", "SAUDI ARABIA": "SA",
    "UNITED ARAB EMIRATES": "AE", "QATAR": "QA", "KUWAIT": "KW",
    "OMAN": "OM", "BAHRAIN": "BH", "MALAYSIA": "MY", "SINGAPORE": "SG",
    "INDONESIA": "ID", "THAILAND": "TH", "VIETNAM": "VN",
    "PHILIPPINES": "PH", "CHINA": "CN", "JAPAN": "JP",
    "SOUTH KOREA": "KR", "TURKEY": "TR", "RUSSIA": "RU",
    "SOUTH AFRICA": "ZA", "NIGERIA": "NG", "EGYPT": "EG",
    "BRAZIL": "BR", "MEXICO": "MX", "ARGENTINA": "AR",
}

COUNTRY_FLAGS = {
    "BD": "🇧🇩", "IN": "🇮🇳", "PK": "🇵🇰", "NP": "🇳🇵", "LK": "🇱🇰",
    "US": "🇺🇸", "GB": "🇬🇧", "CA": "🇨🇦", "AU": "🇦🇺",
    "DE": "🇩🇪", "FR": "🇫🇷", "IT": "🇮🇹", "ES": "🇪🇸",
    "SA": "🇸🇦", "AE": "🇦🇪", "QA": "🇶🇦", "KW": "🇰🇼",
    "OM": "🇴🇲", "BH": "🇧🇭", "MY": "🇲🇾", "SG": "🇸🇬",
    "ID": "🇮🇩", "TH": "🇹🇭", "VN": "🇻🇳", "PH": "🇵🇭",
    "CN": "🇨🇳", "JP": "🇯🇵", "KR": "🇰🇷", "TR": "🇹🇷",
    "RU": "🇷🇺", "ZA": "🇿🇦", "NG": "🇳🇬", "EG": "🇪🇬",
    "BR": "🇧🇷", "MX": "🇲🇽", "AR": "🇦🇷",
}

# ============================================================================
#  LOGGING — console + file
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(BASE_DIR / "bot_log.txt", encoding="utf-8"),
    ],
)
log = logging.getLogger("orangebot")

# ============================================================================
#  TELEGRAM BOT
# ============================================================================
bot = Bot(token=BOT_TOKEN)

# ============================================================================
#  HELPER FUNCTIONS
# ============================================================================
def get_country_flag(country_name: str) -> str:
    """Return flag emoji for a given country name."""
    code = COUNTRY_NAME_TO_CODE.get(country_name.strip().upper())
    return COUNTRY_FLAGS.get(code, "🌍")


def mask_number(number) -> str:
    """Mask a phone number — keep prefix and last 4 digits."""
    s = str(number).strip()
    if len(s) <= 7:
        return s
    prefix_len = 4 if s.startswith("+") else 3
    return f"{s[:prefix_len]}***{s[-4:]}"


def extract_country(text: str) -> str:
    """Extract country name from a termination string."""
    parts = text.split()
    country_parts = []
    for p in parts:
        if p.upper() in ("MOBILE", "FIXED") or any(ch.isdigit() for ch in p):
            break
        country_parts.append(p)
    return " ".join(country_parts) if country_parts else text


def format_caption(country, number, cli, duration) -> str:
    """Build Telegram caption for a call recording."""
    flag = get_country_flag(country)
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    caption = (
        f"🔥 NEW {flag} <b>{country.upper()} CALL RECEIVED</b> ✨\n\n"
        f"🕒 <b>Time:</b> {time_str}\n"
        f"🌍 <b>Country:</b> {country}\n"
        f"☎️ <b>Number:</b> {mask_number(number)}\n"
    )
    if duration:
        caption += f"⏱ <b>Duration:</b> {duration}s\n"

    caption += f'\n<b>Powered by <a href="https://t.me/{DEVELOPER}">SHAYAN</a></b>'
    return caption


def send_audio(caption: str, mp3_path: Path) -> bool:
    """Upload MP3 to Telegram with inline buttons."""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🤖 Bot Developer", url=f"https://t.me/{DEVELOPER}"),
            InlineKeyboardButton("📞 Number", url=NUMBER_URL),
        ]
    ])
    try:
        with open(mp3_path, "rb") as f:
            bot.send_audio(
                chat_id=CHAT_ID,
                audio=f,
                caption=caption,
                parse_mode="HTML",
                reply_markup=keyboard,
                timeout=60,
            )
        log.info("✅ Audio sent to Telegram.")
        return True
    except Exception as e:
        log.error(f"❌ send_audio failed: {e}")
        return False


def send_call_alert(number):
    """Send a text alert when a new call is detected."""
    text = f"☎️ New call detected from {mask_number(number)}. Waiting for the call to end."
    try:
        msg = bot.send_message(chat_id=CHAT_ID, text=text, timeout=30)
        log.info(f"🔔 Alert sent (message_id={msg.message_id}).")
        return msg.message_id
    except Exception as e:
        log.error(f"❌ send_call_alert failed: {e}")
        return None


def delete_message(message_id) -> None:
    """Delete a Telegram message by ID."""
    if not message_id:
        return
    try:
        bot.delete_message(chat_id=CHAT_ID, message_id=message_id)
        log.info(f"🗑️ Alert {message_id} deleted.")
    except Exception as e:
        log.error(f"❌ delete_message failed: {e}")


def convert_wav_to_mp3(wav_path: Path, mp3_path: Path) -> None:
    """Convert a WAV file to MP3 using ffmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-i", str(wav_path),
        "-codec:a", "libmp3lame",
        "-q:a", "4",
        str(mp3_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


# ============================================================================
#  SELENIUM DRIVER (CODESPACES OPTIMIZED)
# ============================================================================
def start_driver() -> webdriver.Chrome:
    """Create and configure a headless Chrome driver for Codespaces."""
    opts = Options()
    
    # কোডস্পেসে Chrome চালানোর জন্য আবশ্যক আর্গুমেন্ট
    opts.add_argument("--headless=new")             # নতুন হেডলেস মোড
    opts.add_argument("--no-sandbox")               # স্যান্ডবক্স পারমিশন এড়াতে
    opts.add_argument("--disable-dev-shm-usage")    # মেমোরি (RAM) সমস্যা এড়াতে
    opts.add_argument("--disable-gpu")              # জিপিইউ বন্ধ
    opts.add_argument("--remote-debugging-port=9222") # ক্র্যাশ কমাতে
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument(
        "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    # Webdriver Manager দিয়ে Driver অটো-ইনস্টল এবং সার্ভিস তৈরি
    service = Service(ChromeDriverManager().install())
    
    # ড্রাইভার চালু
    driver = webdriver.Chrome(service=service, options=opts)
    driver.set_page_load_timeout(60)
    return driver


def login(driver: webdriver.Chrome) -> None:
    """Log into OrangeCarrier and navigate to the Live Calls page."""
    log.info("🌐 Opening login page...")
    driver.get("https://www.orangecarrier.com/login")
    wait = WebDriverWait(driver, 30)

    email_field = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR,
         'input[type="email"], input[name*="email" i], input[id*="email" i]')
    ))
    email_field.clear()
    email_field.send_keys(ORANGE_USER)

    pwd_field = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
    pwd_field.clear()
    pwd_field.send_keys(ORANGE_PASS)

    log.info("👉 Submitting login form...")
    btn = driver.find_element(
        By.CSS_SELECTOR, 'button[type="submit"], input[type="submit"]'
    )
    btn.click()

    time.sleep(12) # কোডস্পেসে লগইন হতে সময় লাগতে পারে, তাই সময় বাড়ানো হলো
    if "orangecarrier.com" not in driver.current_url:
        raise RuntimeError("Login failed — not on orangecarrier domain.")

    log.info("🎉 Login successful. Opening Live Calls page...")
    driver.get("https://www.orangecarrier.com/live/calls")
    time.sleep(5)


# ============================================================================
#  CALL PROCESSOR
# ============================================================================
def process_call(driver, country, number, cli, duration, did, uuid, alert_id) -> None:
    """Download the recording, convert to MP3, send it, and clean up."""
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    cli_safe = re.sub(r"\D", "", str(cli))[-6:] or "000000"
    base = f"call_{ts}_{cli_safe}"
    wav_path = BASE_DIR / f"{base}.wav"
    mp3_path = BASE_DIR / f"{base}.mp3"
    audio_url = (
        f"https://www.orangecarrier.com/live/calls/sound?did={did}&uuid={uuid}"
    )

    try:
        session = requests.Session()
        for c in driver.get_cookies():
            session.cookies.set(c["name"], c["value"], domain=c.get("domain"))

        log.info(f"🎧 Downloading recording: {base}.wav")
        r = session.get(audio_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        r.raise_for_status()
        wav_path.write_bytes(r.content)
        log.info(f"✅ Recording saved: {wav_path.name}")

        log.info("🔄 Converting WAV → MP3...")
        convert_wav_to_mp3(wav_path, mp3_path)
        log.info(f"✅ MP3 ready: {mp3_path.name}")

        caption = format_caption(country, number, cli, duration)
        if send_audio(caption, mp3_path):
            delete_message(alert_id)

    except Exception as e:
        log.error(f"❌ process_call error for {cli}: {e}")
    finally:
        for p in (wav_path, mp3_path):
            try:
                if p.exists():
                    p.unlink()
            except Exception:
                pass
        log.info("🗑️ Temporary files cleaned.")


# ============================================================================
#  MONITOR LOOP
# ============================================================================
def monitor() -> None:
    """Main monitoring loop — scans the Live Calls table for new entries."""
    driver = start_driver()
    login(driver)

    processed = set()
    last_refresh = time.time()
    refresh_sec = REFRESH_MIN * 60

    log.info("🚀 Monitoring started...")

    while True:
        try:
            # --- Periodic page refresh ---
            if time.time() - last_refresh > refresh_sec:
                log.info(f"🕒 Refreshing page (every {REFRESH_MIN} min)...")
                try:
                    driver.get("https://www.orangecarrier.com/live/calls")
                    time.sleep(3)
                except Exception as e:
                    log.error(f"🔴 Refresh failed: {e}")
                last_refresh = time.time()

            # --- Scan call rows ---
            rows = driver.find_elements(
                By.CSS_SELECTOR,
                "#LiveCalls tr, #last-activity tbody.lastdata tr",
            )
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) < 3:
                    continue

                cli = cols[2].text.strip()
                if not cli:
                    continue

                play_btn = None
                try:
                    play_btn = row.find_element(
                        By.CSS_SELECTOR, "button[onclick*='Play']"
                    )
                except Exception:
                    pass
                if not play_btn:
                    continue

                onclick = play_btn.get_attribute("onclick") or ""
                m = re.search(
                    r"Play\(['\"]([^'\"]+)['\"],\s*['\"]([^'\"]+)['\"]\)",
                    onclick,
                )
                if not m:
                    continue

                did, uuid = m.group(1), m.group(2)
                call_id = f"{cli}_{uuid}"
                if call_id in processed:
                    continue

                processed.add(call_id)
                if len(processed) > 5000:
                    processed.pop()

                country = extract_country(cols[0].text.strip())
                number = cols[1].text.strip()
                duration = cols[3].text.strip() if len(cols) > 3 else ""

                log.info(f"📞 New call detected: {cli} | {country} | {duration}s")

                alert_id = send_call_alert(number)
                log.info("⏳ Waiting 20 seconds for call to end...")
                time.sleep(20)

                process_call(
                    driver, country, number, cli, duration,
                    did, uuid, alert_id,
                )

            time.sleep(0.2)

        except KeyboardInterrupt:
            log.info("⏹️ Monitoring stopped by user.")
            break
        except Exception as e:
            log.error(f"🔴 Loop error: {e}")
            time.sleep(15)

    try:
        driver.quit()
    except Exception:
        pass


# ============================================================================
#  ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    try:
        monitor()
    except Exception as e:
        log.critical(f"💥 Fatal error: {e}")