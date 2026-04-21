

import re
import time

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

URL = "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGK&QO_fu146_anzr=b0-gvzr"

SELECTED_FIELDS= [
    "Year",
    "Month",
    "FlightDate",
    "Marketing_Airline_Network",
    "Flight_Number_Marketing_Airline",
    "Origin",
    "Dest",
    "CRSDepTime",
    "DepTime",
    "DepDelay",
    "CRSArrTime",
    "ArrTime",
    "ArrDelay",
    "Cancelled",
    "CancellationCode",
    "Diverted",
    "AirTime",
    "Distance",
    "CarrierDelay",
    "WeatherDelay",
    "NASDelay",
    "SecurityDelay",
    "LateAircraftDelay",
]

# Based on the current page options.
YEARS = list(range(2018, 2026))
MONTHS = [("January", "01"),("February", "02"),("March", "03"),
    ("April", "04"), ("May", "05"),("June", "06"), ("July", "07"),
    ("August", "08"), ("September", "09"), ("October", "10"), ("November", "11"),
    ("December", "12")]

DOWNLOAD_DIR = r"yourDownloadDirectoryHere"  # <-- UPDATE THIS PATH
HEADLESS = False
DOWNLOAD_TIMEOUT_MS = 180_000


def print(msg ):
    print(msg, flush=True)


def safe_filename(name):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")

def click_by_text(page, text,exact=True, timeout=15000) -> None:

    candidates = [
        page.get_by_text(text, exact=exact),
        page.locator(f"text={'\"' + text + '\"' if exact else text}"),
        page.locator("a, button, label, span, div").filter(has_text=text),
    ]

    last_error = None
    for locator in candidates:
        try:
            locator.first.wait_for(state="visible", timeout=timeout)
            locator.first.click(timeout=timeout)
            return
        except Exception as e:
            last_error = e

    raise RuntimeError(f"Could not click text '{text}': {last_error}")


def uncheck_select_all_fields_if_needed(page):
    try:
        checkbox = page.locator("input[type='checkbox']").filter(has=page.locator("xpath=..")).first
        select_all_label = page.get_by_text("Select all fields", exact=False)
        if select_all_label.count() > 0:
            label_box = select_all_label.first.bounding_box()
            if label_box:
                try:
                    select_all_label.first.click(timeout=3000)
                except Exception:
                    pass
    except Exception:
        pass


def clear_selected_fields(page):
    try:
        checked = page.locator("input[type='checkbox']:checked")
        count = checked.count()
        for i in range(count):
            try:
                checked.nth(i).uncheck(timeout=2000)
            except Exception:
                pass
    except Exception:
        pass


def select_field(page, field_name):
    row = page.locator("tr").filter(has_text=field_name)
    if row.count() == 0:
        raise RuntimeError(f"Field row not found for '{field_name}'")

    checkbox = row.first.locator("input[type='checkbox']")
    if checkbox.count() == 0:
        raise RuntimeError(f"Checkbox not found for field '{field_name}'")

    try:
        checkbox.first.check(timeout=5000)
    except Exception:
        checkbox.first.click(timeout=5000)


def select_fields(page, fields):
    clear_selected_fields(page)
    uncheck_select_all_fields_if_needed(page)

    missing = []
    for field in fields:
        try:
            select_field(page, field)
        except Exception:
            missing.append(field)

    if missing:
        raise RuntimeError(f"These fields could not be selected: {missing}")


def click_filter_value(page, value_text):
    click_by_text(page, value_text, exact=True)


def click_download(page):
    candidates = [
        page.get_by_role("button", name=re.compile(r"download", re.I)),
        page.get_by_role("link", name=re.compile(r"download", re.I)),
        page.get_by_text("Download", exact=True),
        page.locator("input[type='submit'][value*='Download' i]"),
        page.locator("button:has-text('Download')"),
        page.locator("a:has-text('Download')"),
    ]

    last_error = None
    for locator in candidates:
        try:
            if locator.count() > 0:
                locator.first.click(timeout=10000)
                return
        except Exception as e:
            last_error = e

    raise RuntimeError(f"Could not find/click Download control: {last_error}")


def wait_until_page_ready(page):
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_load_state("networkidle")


def save_download(download, target_dir, year, month_num):
    target_dir.mkdir(parents=True, exist_ok=True)

    suggested = download.suggested_filename
    if suggested:
        filename = safe_filename(suggested)
    else:
        filename = f"transtats_{year}_{month_num}.csv"

    if not Path(filename).suffix:
        filename += ".csv"

    output_path = target_dir / filename
    download.save_as(str(output_path))
    return output_path


def download_one(page, year, month_name,month_num):
    print(f"Processing {year}-{month_num} ({month_name})")

    page.goto(URL, wait_until="domcontentloaded")
    wait_until_page_ready(page)
    click_filter_value(page, str(year))
    page.wait_for_timeout(1000)

    click_filter_value(page, month_name)
    page.wait_for_timeout(1000)

    select_fields(page, SELECTED_FIELDS)
    page.wait_for_timeout(500)


    target_dir = DOWNLOAD_DIR / f"year={year}" / f"month={month_num}"

    with page.expect_download(timeout=DOWNLOAD_TIMEOUT_MS) as dl_info:
        click_download(page)

    download = dl_info.value
    output_path = save_download(download, target_dir, year, month_num)
    print(f"Saved: {output_path}")
    return output_path


def main():
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        successes = []
        failures = []

        for year in YEARS:
            for month_name, month_num in MONTHS:
                try:
                    saved = download_one(page, year, month_name, month_num)
                    successes.append(str(saved))
                except PlaywrightTimeoutError as e:
                    failures.append((year, month_num, f"Timeout: {e}"))
                    print(f"FAILED {year}-{month_num}: timeout")
                except Exception as e:
                    failures.append((year, month_num, str(e)))
                    print(f"FAILED {year}-{month_num}: {e}")

                # Be polite to the server
                time.sleep(2)

        browser.close()


    print(f"Successful downloads: {len(successes)}")
    print(f"Failed downloads: {len(failures)}")

    if failures:
        print("\nFailures:")
        for year, month_num, err in failures:
            print(f"  {year}-{month_num}: {err}")


if __name__ == "__main__":
    main()