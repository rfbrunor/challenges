# This is a sample Python script.
import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# import folium
import pricehandle as ph
import datahandle as dh
import visualdata as vd

#config pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

if __name__ == '__main__':
    print("Starting processing...")
    details_itapema_file = "data/Details_Data.csv"
    price_file_origin = "data/Price_AV_Itapema-001.csv"
    vivareal_data_seller = "data/VivaReal_Itapema.csv"

    path_filtered_price_file = "data/Price_AV_Itapema_filtered.csv"
    path_property_profile = "data/Property_profile.csv"
    path_map_most_revenue = "data/mapa_itapema.html"

    #number items to list
    number_items_rented = 5000
    number_filter = 30
    begin_date = pd.to_datetime('2023-01-01')
    end_date = pd.to_datetime('2023-12-31')

    #generate file Price_AV_Itapema_filtered
    ph.generate_filtered_price_file(price_file_origin, path_filtered_price_file)

    #get dataframe with mais alugados, average price and others
    df_profile = dh.list_airbnb_most_rented(path_filtered_price_file, details_itapema_file, path_property_profile, number_items_rented, True)

    #mount graphic prices
    vd.price_graphic(df_profile)

    #create map file in data directory
    vd.generate_map(df_profile, path_map_most_revenue,number_filter)

    #average bedroom and bathroom
    dh.show_data_more_rented(df_profile, number_filter)

    # path_filtered_price_file
    df_profile_year_date = dh.list_airbnb_most_rented(path_filtered_price_file, details_itapema_file, path_property_profile, number_items_rented, False, begin_date, end_date)
    dh.average_higher_revenues(df_profile_year_date,number_filter)

    print("Finished processing")



















