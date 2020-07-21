import requests
import datetime
import time
import random
from pyquery import PyQuery as pq
from selenium import webdriver
import urllib.parse
import numpy as np
import pandas as pd
from multiprocessing import Pool

def get_dates(start_date = datetime.date(2019, 1, 3), 
              end_date = datetime.date(2019, 1, 17) , 
              day_delta = datetime.timedelta(days=1)):
    '''
    Get the date strings from start_date to end_date, with step day_delta.
    start_date: datetime.date(2019, 1, 1)
    end_date: datetime.date(2019, 1, 31)
    day_delta: datetime.timedelta(days=1)
    '''
    dates_str_list = [(start_date + i*day_delta).isoformat() for i in range((end_date - start_date).days + 1)]
    return dates_str_list

def get_cwb_weather_info(base_url:str, date:str) -> dict:
    '''
    Return the presure(hPa), temperature(Celsius), relative humidity(%) of the date.
    base_url: str
    date: str, eg. 2020-01-31 (YYYY-MM-DD)
    '''
    url = f"{base_url}{date}"
    pres_hpa_css = "tr:nth-child(22) td:nth-child(2)"
    temp_cels_css = "tr:nth-child(22) td:nth-child(4)"
    rh_percent_css = "tr:nth-child(22) td:nth-child(6)"
    
    html_doc = pq(url)
    try:
        pres_hpa = float(html_doc(pres_hpa_css).text())
    except Exception as ex:
        print(ex, "at pres_hpa")
        pres_hpa = None
    try:
        temp_cels = float(html_doc(temp_cels_css).text())
    except Exception as ex:
        print(ex, "at temp_cels")
        temp_cels = None
    try:
        rh_percent = float(html_doc(rh_percent_css).text())
    except Exception as ex:
        print(ex, "at rh_percent")
        rh_percent = None
    
    print("xxxxxxxxxxxxxxxx")
    return (pres_hpa, temp_cels, rh_percent)

def main():
    time_start = datetime.datetime.now()
    print("time_start: ", time_start)

    weather_info_dict = dict()
    cwb_base_url = f"https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C0A9F0&stname=%25E5%2585%25A7%25E6%25B9%2596&datepicker="
    
    for d in get_dates():
        print("retrieving", d, "...")
        weather_info = get_cwb_weather_info(cwb_base_url, d)
        sleep_secs = random.randint(1, 4)
        time.sleep(sleep_secs)
        weather_info_dict[d] = weather_info

    time_rtrv_end = datetime.datetime.now()
    print("time_rtrv_end: ", time_rtrv_end)

    # reading and exporting the retrieved weather info
    df = pd.DataFrame.from_dict(weather_info_dict, orient='index', columns=['pres_hpa', 'temp_cels', 'rh_percent'])
    print(df.head())

    # formatting the file name with date & time su
    fmt = "%Y%m%dT%H%M%S"
    t = time.localtime()
    df.to_csv(f'../output/weather_info_2020_rtrv{time.strftime(fmt, t)}.csv', index=True,) 

    time_savefile_end = datetime.datetime.now()
    print("time_savefile_end: ", time_savefile_end)

    # # if you'd like to export zip file containing that csv
    # compression_opts = dict(method='zip',
    #                         archive_name='out.csv')  

    # df.to_csv('../output/weather_info.zip', index=False,
    #           compression=compression_opts) 
    print("===============")
    print("data retrieval:", (time_rtrv_end - time_start))
    print("file saving:", (time_savefile_end - time_rtrv_end))
    print("total time:", (time_savefile_end - time_start))

if __name__ == '__main__':
    main()