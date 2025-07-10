import os
import time
import random
import base64
from io import BytesIO
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import pytesseract
from playwright.sync_api import sync_playwright

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def human_wait(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))

def base64_to_image(base64_str):
    if ',' in base64_str:
        base64_str = base64_str.split(',')[1]
    return Image.open(BytesIO(base64.b64decode(base64_str)))

def preprocess_variants(img):
    img = img.convert("L")
    yield img
    yield ImageEnhance.Contrast(img).enhance(2)
    yield ImageOps.invert(img).filter(ImageFilter.SHARPEN)
    yield img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
    yield img.point(lambda x: 0 if x < 140 else 255)

def extract_digits_with_confidence(img):
    config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    best_text = ""
    best_conf = 0
    for variant in preprocess_variants(img):
        data = pytesseract.image_to_data(variant, config=config, output_type=pytesseract.Output.DICT)
        for text, conf in zip(data['text'], data['conf']):
            text = text.strip()
            if text.isdigit() and len(text) == 3:
                try:
                    conf = int(conf)
                    if conf > best_conf:
                        best_conf = conf
                        best_text = text
                except:
                    continue
    return (best_text if best_conf >= 10 else None), best_conf

def is_captcha_limit_reached(page):
    return page.evaluate('''() => {
        return document.body.innerText.includes("You have reached the maximum number of allowed captcha submissions");
    }''')

def return_to_login(page):
    print("🔄 Going back to login page...")
    page.goto("https://algeria.blsspainglobal.com/DZA/account/login", wait_until="domcontentloaded")
    human_wait(2, 4)
    try:
        login_input = page.evaluate_handle('''() => {
            return Array.from(document.querySelectorAll('input[type="text"]')).find(el => el.offsetParent !== null);
        }''').as_element()
        if login_input:
            login_input.fill("user268923@gmail.com")
            page.click('button[type="submit"]')
            print("✅ Re-submitted login.")
            human_wait(2, 4)
    except Exception as e:
        print("❌ Error while logging in again:", e)

def click_book_now(page):
    try:
        button = page.query_selector('a[href="/DZA/appointment/newappointment"]')
        if button:
            button.click()
            print("📅 Clicked 'Book Now' button.")
            human_wait(2, 3)
    except Exception as e:
        print("❌ Error clicking 'Book Now':", e)

# === MAIN SCRIPT ===
with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context("user_data", headless=False)
    page = browser.new_page()
    page.goto("https://algeria.blsspainglobal.com/DZA/account/login", wait_until="domcontentloaded")
    human_wait(2, 4)

    while True:
        try:
            if is_captcha_limit_reached(page):
                print("🚫 Captcha limit reached. Restarting...")
                return_to_login(page)
                continue

            current_url = page.url

            if "account/login" in current_url:
                print("🔐 Login page detected.")
                try:
                    login_input = page.evaluate_handle('''() => {
                        return Array.from(document.querySelectorAll('input[type="text"]')).find(el => el.offsetParent !== null);
                    }''').as_element()
                    if login_input:
                        login_input.fill("user268923@gmail.com")
                        page.click('button[type="submit"]')
                        print("✅ Submitted login.")
                        human_wait(2, 4)
                        continue
                except Exception as e:
                    print("❌ Login failed:", e)
                    continue

            # Always check for captcha and password field
            visible_password_handle = page.evaluate_handle('''() => {
                return Array.from(document.querySelectorAll('input[type="password"]')).find(el => {
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    return (
                        rect.width > 0 &&
                        rect.height > 0 &&
                        style.display !== 'none' &&
                        style.visibility !== 'hidden' &&
                        parseFloat(style.opacity) !== 0
                    );
                });
            }''')
            password_input = visible_password_handle.as_element()
            if password_input:
                password_input.fill("Khaled@1616")
                print("🔑 Password filled.")
                human_wait(1, 2)

            # ✅ Check and click "Book Now" if available
            click_book_now(page)

            # === CAPTCHA Handling ===
            target_number = page.evaluate('''() => {
                const visible = Array.from(document.querySelectorAll('div.box-label')).find(div => {
                    const rect = div.getBoundingClientRect();
                    const style = window.getComputedStyle(div);
                    if (
                        rect.width === 0 ||
                        rect.height === 0 ||
                        style.display === 'none' ||
                        style.visibility === 'hidden' ||
                        parseFloat(style.opacity) === 0
                    ) return false;
                    const elAtPoint = document.elementFromPoint(rect.left + 1, rect.top + 1);
                    return elAtPoint === div || div.contains(elAtPoint);
                });
                return visible ? visible.textContent.match(/\d{3}/)?.[0] : null;
            }''')

            if not target_number:
                print("⏳ No captcha.")
                time.sleep(3)
                continue

            print(f"🎯 Captcha target: {target_number}")

            visible_imgs_handle = page.evaluate_handle('''() => {
                return Array.from(document.querySelectorAll('img.captcha-img')).filter(img => {
                    const rect = img.getBoundingClientRect();
                    const style = window.getComputedStyle(img);
                    if (
                        rect.width === 0 ||
                        rect.height === 0 ||
                        style.display === 'none' ||
                        style.visibility === 'hidden' ||
                        parseFloat(style.opacity) === 0
                    ) return false;
                    const elAtPoint = document.elementFromPoint(rect.left + 1, rect.top + 1);
                    return elAtPoint === img || img.contains(elAtPoint);
                });
            }''')

            visible_imgs = []
            for prop in visible_imgs_handle.get_properties().values():
                el = prop.as_element()
                if el:
                    visible_imgs.append(el)

            if not visible_imgs:
                print("⚠️ No visible captcha images.")
                time.sleep(3)
                continue

            matched = 0
            for idx, img in enumerate(visible_imgs, start=1):
                src = img.get_attribute('src')
                if src and src.startswith("data:image"):
                    pil_img = base64_to_image(src)
                    result, conf = extract_digits_with_confidence(pil_img)
                    if result:
                        print(f"🟢 Image {idx}: OCR → {result} (Conf: {conf}%)")
                        if result == target_number:
                            try:
                                img.click()
                                matched += 1
                                print(f"✅ Clicked image {idx}")
                            except Exception as e:
                                print(f"❌ Click error: {e}")
                    else:
                        print(f"🔴 Image {idx}: No valid result.")

            print(f"🔢 Total clicked: {matched}")
            human_wait(1, 2)

            try:
                page.click('#btnVerify')
                print("🚀 Clicked Submit.")
            except Exception as e:
                print("❌ Submit click failed:", e)

            time.sleep(6)

        except KeyboardInterrupt:
            print("🛑 Stopped by user.")
            break
        except Exception as e:
            print("❌ Loop error:", e)
            time.sleep(5)

    print("✅ Script finished.")
