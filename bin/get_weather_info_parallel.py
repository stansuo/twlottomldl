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
from itertools import product

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

def main(obs_name = "Neihu", obs_year = "test"):
    
    time_start = datetime.datetime.now()
    print("time_start: ", time_start)
    
    base_urls = {
    "Neihu" : "https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C0A9F0&stname=%25E5%2585%25A7%25E6%25B9%2596&datepicker=",
    "Songshan": "https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C0AH70&stname=%25E6%259D%25BE%25E5%25B1%25B1&datepicker=",
    "Dazhi": "https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C0A9A0&stname=%25E5%25A4%25A7%25E7%259B%25B4&datepicker=",
    "Wenshan": "https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C0AC80&stname=%25E6%2596%2587%25E5%25B1%25B1&datepicker=",
    "Xizhi": "https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C0AH00&stname=%25E6%25B1%2590%25E6%25AD%25A2&datepicker=",
    "Shihding": "https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C0A640&stname=%25E7%259F%25B3%25E7%25A2%2587&datepicker=",
    "Shenkeng": "https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C0AH80&stname=%25E6%25B7%25B1%25E5%259D%2591&datepicker=",
    } 
    
    date_periods = {
    "2016": (datetime.date(2016, 1, 1), datetime.date(2016, 12, 31)),
    "2017": (datetime.date(2017, 1, 1), datetime.date(2017, 12, 31)),
    "2018": (datetime.date(2018, 1, 1), datetime.date(2018, 12, 31)),
    "2019": (datetime.date(2019, 1, 1), datetime.date(2019, 12, 31)),
    "2020": (datetime.date(2020, 1, 1), datetime.date(2020, 12, 31)),
    "2021": (datetime.date(2021, 1, 1), datetime.date(2021, 1, 31)),
    }
    
    weather_info_dict = dict()
    base_url = base_urls[obs_name]
    start_date = date_periods[obs_year][0]
    end_date = date_periods[obs_year][1]

    for d in get_dates(start_date = start_date,
                       end_date = end_date):
        print("retrieving", d, "...")
        
        weather_info = get_cwb_weather_info(base_url, d)
        sleep_secs = random.randint(1, 4)
        time.sleep(sleep_secs)
        weather_info_dict[d] = weather_info

    time_rtrv_end = datetime.datetime.now()
    print("time_rtrv_end: ", time_rtrv_end)
    print("===============")

    # reading and exporting the retrieved weather info
    df = pd.DataFrame.from_dict(weather_info_dict, orient='index', columns=['pres_hpa', 'temp_cels', 'rh_percent'])
    print(df.head())
    print("===============")

    # formatting the file name with date & time su
    fmt = "%Y%m%dT%H%M%S"
    t = time.localtime()
    df.to_csv(f'../output/parallel/weather_info_{obs_name}_{obs_year}_rtrv{time.strftime(fmt, t)}.csv', index=True,)

    time_savefile_end = datetime.datetime.now()
    print(f'{obs_name}_{obs_year} file saved')
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

if __name__ == "__main__":
    obs_names = ["Neihu", "Songshan", "Dazhi", "Wenshan","Xizhi", "Shihding", "Shenkeng"]
    obs_years = ["2016", "2017", "2018", "2019", "2020", "2021"]

    with Pool(12) as p:
        p.starmap(main, product(obs_names, obs_years))