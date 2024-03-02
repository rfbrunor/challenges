import os
import pandas as pd
import time


def get_ids(path_details_data):
    airbnb_ids = None
    if os.path.exists(path_details_data):
        df_details_data = pd.read_csv(path_details_data, usecols=['ad_id'])
        df_details_data.drop_duplicates()
        airbnb_ids = df_details_data['ad_id'].unique()

    return airbnb_ids


def __filter_data_price(airbnb_ids, df_price_data):
    df_subset_result = pd.DataFrame()
    for data_id in airbnb_ids:
        if data_id in df_price_data['airbnb_listing_id'].values:
            df_subset_by_id = df_price_data.loc[df_price_data['airbnb_listing_id'] == data_id]
            df_subset_by_id = df_subset_by_id.sort_values(by=['aquisition_date', 'date'],
                                                          ascending=[True, True])
            df_subset_by_id = df_subset_by_id.drop_duplicates(subset=['date'], keep='first')
            df_subset_result = pd.concat([df_subset_result, df_subset_by_id],
                                         ignore_index=True)
    return df_subset_result

"""
Loads the entire file into memory requiring at least 20gb of ram in this case
"""
def gen_filtered_price_file(path_price_origin, path_price_filtered, airbnb_ids, price_outlier=3000):
    if os.path.exists(path_price_filtered):
        print("Found filtered price file")
    else:
        print("Creating filtered price file")
        selected_columns = ['airbnb_listing_id', 'date', 'aquisition_date', 'available', 'price']
        df_price_file = pd.read_csv(path_price_origin, low_memory=False, memory_map=True, usecols=selected_columns)

        df_price_file['aquisition_date'] = pd.to_datetime(df_price_file['aquisition_date'])
        df_price_file['date'] = pd.to_datetime(df_price_file['date'])
        df_price_file["available"] = df_price_file["available"].astype(int)
        df_price_file = df_price_file.drop_duplicates()

        # filter only available false, i.e. renters
        df_price_file_filter = df_price_file[df_price_file['available'] == 0]
        df_price_not_repeat_date = __filter_data_price(airbnb_ids, df_price_file_filter)
        df_price_not_repeat_date = df_price_not_repeat_date.loc[df_price_not_repeat_date['price'] < price_outlier]
        df_price_not_repeat_date.to_csv(path_price_filtered, index=False, encoding='latin-1', float_format='%.2f')
        print("File with filtered prices was created")

"""
select the file in parts and search by identifier, 
improving data memory control, since the amount of data loaded is fixed.
Memory use around 4GB
"""
def gen_filtered_price_file_chunk(path_price_origin, path_price_filtered, airbnb_ids, price_outlier=3000):
    if os.path.exists(path_price_filtered):
        print("Found filtered price file")
    else:
        print("Creating filtered price file")
        selected_columns = ['airbnb_listing_id', 'date', 'aquisition_date', 'available', 'price']
        df_price_file_reader = pd.read_csv(path_price_origin, low_memory=False, memory_map=True,
                                           usecols=selected_columns,
                                           chunksize=10000000)

        df_price_not_repeat_date = pd.DataFrame()
        for chunk in df_price_file_reader:
            chunk['aquisition_date'] = pd.to_datetime(chunk['aquisition_date'])
            chunk['date'] = pd.to_datetime(chunk['date'])
            chunk["available"] = chunk["available"].astype(int)
            chunk = chunk[chunk['available'] == 0]
            df_price_not_repeat_date = pd.concat([df_price_not_repeat_date, __filter_data_price(airbnb_ids, chunk)],
                                                 ignore_index=True)

        df_price_not_repeat_date = __filter_data_price(airbnb_ids, df_price_not_repeat_date)
        df_price_not_repeat_date = df_price_not_repeat_date.loc[
            df_price_not_repeat_date['price'] < price_outlier]
        df_price_not_repeat_date.to_csv(path_price_filtered, index=False, encoding='latin-1', float_format='%.2f')
        print("File with filtered prices was created")

