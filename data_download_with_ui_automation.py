import re
import time
import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

URL = "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGK&QO_fu146_anzr=b0-gvzr"

download_dir=r"" ## specify your download directory here

fields =["FlightDate", "Operating_Airline ","DOT_ID_Operating_Airline","OriginAirportID",
"Origin","OriginCityName"	,"OriginStateFips","OriginStateName",
"DestAirportID","Dest","DestCityName","DestStateFips","DestStateName",
"DepTime"	,"DepDelay","DepDelayMinutes","DepDel15","ArrTime","ArrDelay","ArrDelayMinutes",
"ArrDel15","Cancelled","CancellationCode","Diverted","AirTime","Distance",
"CarrierDelay","WeatherDelay","NASDelay","SecurityDelay",
"LateAircraftDelay","FirstDepTime"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=200000)
    # select all years
    year_select = page.locator('select[name="cboYear"]')
    years = year_select.locator("option").all_text_contents()
    # loop trough years
    for year in years:
        year_select.select_option(value=str(year))
        # select all months
        month_select = page.locator('select[name="cboPeriod"]')
        months = month_select.locator("option").all_text_contents()
        ## loop trough months
        for month in months:
            month_select.select_option(value=str(month))
            
            ## select fields
            rows = page.locator("tbody tr")
            # Wait until at least one row is present
            rows.first.wait_for(state="visible")
            for i in range(rows.count()):
                row = rows.nth(i)
                checkbox = row.locator('input[type="checkbox"]').first
                cells = row.locator("td")
                if checkbox.count() == 0 or cells.count() < 1:
                    continue
                label = cells.nth(0).inner_text().strip()
                if label in fields:
                    checkbox.check()
                else:
                    checkbox.uncheck()
            download_btn = page.locator('input[value="Download"]')
            with page.expect_download() as download_info:
                download_btn.click()
                download = download_info.value
                zip_path = os.path.join(download_dir, download.suggested_filename)
                download.save_as(zip_path)
                print(f"Downloaded for {year} {month}: {download.suggested_filename}")