#!/usr/bin/env python3
"""KDP Browser Helper - reads and interacts with KDP pages via Marionette"""
import sys
from marionette_driver.marionette import Marionette

def connect():
    m = Marionette(host='localhost', port=2828)
    m.start_session()
    return m

def get_page_info(m):
    url = m.get_url()
    title = m.title
    print(f"URL: {url}")
    print(f"Title: {title}")

    # Get page text
    text = m.execute_script("return document.body.innerText.substring(0, 5000);")
    print("--- PAGE TEXT ---")
    print(text)

def get_forms(m):
    # Get select elements
    selects = m.execute_script("""
        var results = [];
        document.querySelectorAll('select').forEach(function(s) {
            var opts = [];
            for (var i = 0; i < s.options.length; i++) {
                opts.push(s.options[i].value + ':' + s.options[i].text);
            }
            results.push({name: s.name || s.id, value: s.value, options: opts});
        });
        return JSON.stringify(results);
    """)
    print("SELECTS:", selects)

    # Get inputs
    inputs = m.execute_script("""
        var results = [];
        document.querySelectorAll('input').forEach(function(i) {
            if (i.type !== 'hidden') {
                results.push({type: i.type, name: i.name || i.id, value: i.value, checked: i.checked});
            }
        });
        return JSON.stringify(results);
    """)
    print("INPUTS:", inputs)

def screenshot(m, filename="kdp_screenshot.png"):
    data = m.screenshot()
    import base64
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(data))
    print(f"Screenshot saved: {filename}")

def click_element(m, selector):
    from marionette_driver.by import By
    el = m.find_element(By.CSS_SELECTOR, selector)
    el.click()
    print(f"Clicked: {selector}")

def select_option(m, select_selector, value):
    m.execute_script(f"""
        var sel = document.querySelector('{select_selector}');
        sel.value = '{value}';
        sel.dispatchEvent(new Event('change', {{bubbles: true}}));
    """)
    print(f"Selected {value} in {select_selector}")

def navigate(m, url):
    m.navigate(url)
    print(f"Navigated to: {m.get_url()}")
    print(f"Title: {m.title}")

if __name__ == "__main__":
    m = connect()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "info"

    if cmd == "info":
        get_page_info(m)
    elif cmd == "forms":
        get_forms(m)
    elif cmd == "screenshot":
        fn = sys.argv[2] if len(sys.argv) > 2 else "kdp_screenshot.png"
        screenshot(m, fn)
    elif cmd == "click":
        click_element(m, sys.argv[2])
    elif cmd == "select":
        select_option(m, sys.argv[2], sys.argv[3])
    elif cmd == "nav":
        navigate(m, sys.argv[2])
    elif cmd == "all":
        get_page_info(m)
        print("\n--- FORMS ---")
        get_forms(m)
