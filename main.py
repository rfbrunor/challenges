# This is a sample Python script.
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import folium


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.

def generate_filtered_price_file(path_price_origin, path_price_filtered):
    price_file = path_price_origin
    if os.path.exists(path_price_filtered):
        price_file = path_price_filtered
        print("Found filtered price file")
    else:
        df_price_file = pd.read_csv(price_file, low_memory=False)

        #configuration
        df_price_file['aquisition_date'] = pd.to_datetime(df_price_file['aquisition_date'])
        df_price_file['date'] = pd.to_datetime(df_price_file['date'])
        df_price_file["available"] = df_price_file["available"].astype(int)
        df_price_file = df_price_file.drop_duplicates()

        print("numero de elementos antes do filtro: " + str(len(df_price_file)))
        df_price_file_filter = df_price_file[df_price_file['available'] == 0]
        print("numero de elementos apos o filtro: " + str(len(df_price_file_filter)))

        airbnb_ids = pd.unique(df_price_file_filter['airbnb_listing_id'])
        print("numero de airbnb_ids: " + str(len(airbnb_ids)))
        df_price_not_repeat_date = pd.DataFrame()
        for id in airbnb_ids:
            sub_data_frame_by_id = df_price_file_filter.loc[df_price_file_filter['airbnb_listing_id'] == id]
            sub_data_frame_by_id = sub_data_frame_by_id.sort_values(by=['aquisition_date', 'date'], ascending=[True, True])
            sub_data_frame_by_id_distinct = sub_data_frame_by_id.drop_duplicates(subset=['date'], keep='first')
            df_price_not_repeat_date = pd.concat([df_price_not_repeat_date, sub_data_frame_by_id_distinct], ignore_index=True)

        price_outlier_limit = 3000
        df_price_not_repeat_date = df_price_not_repeat_date.loc[df_price_not_repeat_date['price'] < price_outlier_limit]
        print("tamanho do dataframe final: " + str(len(df_price_not_repeat_date)))
        df_price_not_repeat_date.to_csv(path_price_filtered, index=False, encoding='latin-1', float_format='%.2f')


def list_airbnb_most_rented(path_filtered_price_file, details_itapema_file, file, number_items_rented = 30, save = False, begin_date = None, end_date = None):
    if os.path.exists(path_filtered_price_file):
        df_price_file = pd.read_csv(path_filtered_price_file, low_memory=False)
        df_price_file['date'] = pd.to_datetime(df_price_file['date'])

        if (begin_date is not None) and (end_date is not None):
            df_price_file = df_price_file.loc[(df_price_file['date'] >= begin_date) & (df_price_file['date'] <= end_date)]

        df_count_by_listing_id = df_price_file.groupby('airbnb_listing_id').agg({'price': ['mean', 'count']})
        df_count_by_listing_id.columns = ['average_price', 'number_rented']
        df_count_by_listing_id = df_count_by_listing_id.sort_values(by='number_rented', ascending=False)

        df_details_data = pd.read_csv(details_itapema_file)
        df_details_data = df_details_data.drop_duplicates(subset=['ad_id'], keep='first')

        if number_items_rented > len(df_count_by_listing_id):
            number_items_rented = len(df_count_by_listing_id)

        df_most_rented = df_count_by_listing_id[:][:number_items_rented]
        df_most_types_rented_cp = df_details_data[df_details_data['ad_id'].isin(df_most_rented.index)].copy()

        custom_order = pd.Categorical(df_most_types_rented_cp['ad_id'], categories=df_most_rented.index, ordered=True)
        df_most_types_rented_cp['custom_order'] = custom_order

        df_ordered_most_rented = df_most_types_rented_cp.sort_values(by='custom_order')
        df_ordered_most_rented['average_price'] = df_most_rented['average_price'].values
        df_ordered_most_rented['number_rented'] = df_most_rented['number_rented'].values
        df_ordered_most_rented['revenue'] = df_most_rented['average_price'].values * df_most_rented['number_rented'].values

        df_ordered_most_rented = df_ordered_most_rented.sort_values(by='revenue', ascending=False)
        df_filtered_to_save = df_ordered_most_rented.loc[:, ['ad_id', 'ad_name', 'ad_description', 'number_of_bathrooms', 'number_of_bedrooms','number_of_beds','listing_type', 'average_price','number_rented', 'revenue', 'latitude', 'longitude']]
        df_filtered_to_save['ad_name'] = df_filtered_to_save['ad_name'].astype(str).apply(lambda s: s.strip()).apply(lambda s: s.replace("\n", " "))
        df_filtered_to_save['ad_description'] = df_filtered_to_save['ad_description'].astype(str).apply(lambda s: s.strip()).apply(lambda s: s.replace("\n", " "))

        if save:
            df_filtered_to_save.to_csv(file, index=False, encoding='utf-8', float_format='%.2f')
        return df_filtered_to_save

def price_graphic(dataframe):
    eixo_x = np.arange(len(dataframe['average_price']))

    # interpolation
    tck = np.polyfit(eixo_x, dataframe['average_price'],
                     deg=4)  # Usando um polinômio de grau 3 (ajuste aos seus dados)
    y_interp = np.polyval(tck, eixo_x)

    # Plotando a curva suave
    plt.figure(figsize=(10, 6))
    plt.plot(eixo_x, dataframe['average_price'], 'o', label='Pricing points')
    plt.plot(eixo_x, y_interp, '-', label='Curve')

    plt.xlabel('Index')
    plt.ylabel('Price')
    plt.title('Curve')
    plt.legend()
    plt.show()

def show_location_in_map(dataframe, path_save, number_filter):
    df_ordered_most_rented = dataframe.sort_values(by='revenue', ascending=False)[:][:number_filter]

    longitude_array = df_ordered_most_rented['longitude'].to_numpy()
    latitude_array = df_ordered_most_rented['latitude'].to_numpy()
    id_array = df_ordered_most_rented['ad_id'].to_numpy()

    # central Itapema
    latitude_central = -27.086
    longitude_central = -48.611

    map_itapema = folium.Map(location=[latitude_central, longitude_central], zoom_start=13)

    markers = [(latitude, longitude, id) for latitude, longitude, id in
                  zip(latitude_array, longitude_array, id_array)]

    for mark in markers:
        folium.Marker(location=[mark[0], mark[1]], popup=mark[2]).add_to(map_itapema)

    map_itapema.save(path_save)

def show_data_more_rented(dataframe, number_filter):
    df_ordered_most_rented = dataframe.sort_values(by='revenue', ascending=False)[:][:number_filter]
    n_bathrooms = str(round(df_ordered_most_rented['number_of_bathrooms'].mean(), 2))
    n_bedrooms = str(round(df_ordered_most_rented['number_of_bedrooms'].mean(), 2))
    print("The most profitable apartments have 3 to 4 bedrooms and bathrooms")
    print("Average bathrooms: " + n_bathrooms)
    print("Average bedrooms: " + n_bedrooms)

def average_higher_revenues(dataframe, number_filter):
    df_ordered_most_rented = dataframe.sort_values(by='revenue', ascending=False)[:][:number_filter]
    average_price = round(df_ordered_most_rented['average_price'].mean(), 2)
    average_rented = round(df_ordered_most_rented['number_rented'].mean(), 2)
    print("average price database: " + str(average_price))
    print("average rented database: " + str(average_rented))

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
    generate_filtered_price_file(price_file_origin, path_filtered_price_file)

    #get dataframe with mais alugados, average price and others
    df_profile = list_airbnb_most_rented(path_filtered_price_file, details_itapema_file, path_property_profile, number_items_rented, True)

    #mount graphic prices
    price_graphic(df_profile)

    #create map
    show_location_in_map(df_profile, path_map_most_revenue,number_filter)

    #average bedroom and bathroom
    show_data_more_rented(df_profile, number_filter)

    #average price and average rentals ERRADO
    # path_filtered_price_file
    df_profile_year_date = list_airbnb_most_rented(path_filtered_price_file, details_itapema_file, path_property_profile, number_items_rented, False, begin_date, end_date)

    average_higher_revenues(df_profile_year_date,number_filter)

    print("Finished processing")



















