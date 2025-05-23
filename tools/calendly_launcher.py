import subprocess

def launch_calendly_popup(base_url):
    # base_url = "https://calendly.com/maheshs-first-insight/30min"
    
    calendly_url = f"{base_url}?embed_domain=localhost&embed_type=PopupWidget&redirect_url=http://localhost:5000/success"

    subprocess.Popen([
        "chrome",
        f"--app={calendly_url}",
        "--window-size=300,400",
        "--disable-extensions",
        "--incognito",
        "--disable-translate",
        "--no-default-browser-check",
        "--no-first-run"
    ])

