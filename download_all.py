import os, glob
import urllib
import requests
from bs4 import BeautifulSoup
import zipfile
import pandas as pd

BASE_URL = "https://transtats.bts.gov/PREZIP/"
OUTPUT_DIR ="" 
OUTPUT_FILE=os.path.join(OUTPUT_DIR ,"On_Time_Marketing_Carrier_On_Time_Performance_merged.parquet")

FIELD_LIST=["FlightDate", "Operating_Airline ","DOT_ID_Operating_Airline","OriginAirportID",
"Origin","OriginCityName"	,"OriginStateFips","OriginStateName",
"DestAirportID","Dest","DestCityName","DestStateFips","DestStateName",
"DepTime"	,"DepDelay","DepDelayMinutes","DepDel15","ArrTime","ArrDelay","ArrDelayMinutes",
"ArrDel15","Cancelled","CancellationCode","Diverted","AirTime","Distance",
"CarrierDelay","WeatherDelay","NASDelay","SecurityDelay",
"LateAircraftDelay","FirstDepTime"]

FILE_NAME_PATTERN="On_Time_Performance_Beginning_January_2018"

YEARS = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]

def get_data_urls(base_url, name_pattern, years):
    #get page
    response = requests.get(base_url)
    ## parse the page
    soup = BeautifulSoup(response.text, "html.parser")
    # get all list of zip folders
    url_list = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        text = a.get_text(" ", strip=True)
        url_list.append(text)
    ## get only required folders
    url_list = [f for f in url_list if name_pattern  in f and any(year in f for year in years)]
    print(f"There are {len(url_list)} url found")
    return url_list
    
def download_data(base_url, url_list, output_dir):
    
    not_run_zip=[]
    for i in url_list:
        try:
            url=os.path.join(base_url, i)
            outfile=url.split('/')[-1]
            outfile=os.path.join(output_dir , outfile)
            if not os.path.exists(outfile):
                urllib.request.urlretrieve(url, outfile)
                with zipfile.ZipFile(outfile, 'r') as zip_ref:
                    zip_ref.extractall(output_dir)
        except:
            not_run_zip.append(i)

    print("These url did not process:")
    print(not_run_zip)


def merge_files(output_dir, field_list, output_file):
    merged_df=pd.DataFrame()
    csv_files =glob.glob(os.path.join(output_dir ,"*.csv"))
    csv_files=(i for i in csv_files)
    for i in csv_files:
        df_temp =pd.read_csv(i, encoding='latin-1', encoding_errors='ignore' , on_bad_lines='skip',engine="python")
        df_temp =df_temp [field_list]
        merged_df=pd.concat([merged_df,df_temp], ignore_index=True) 

    print(f"Final count:{merged_df.shape[0]}")
    output_file=os.path.join(output_dir,output_file)
    merged_df.to_parquet(output_file, index=False)

def main():
    file_names = get_data_urls(BASE_URL,FILE_NAME_PATTERN,YEARS)
    download_data(BASE_URL, file_names, OUTPUT_DIR)
    merge_files(OUTPUT_DIR, FIELD_LIST, OUTPUT_FILE)

if __name__ == "__main__":
    main()