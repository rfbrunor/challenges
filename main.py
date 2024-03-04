import pricehandle as ph
import datahandle as dh
import pandas as pd
import visualdata as vd
import machinedataprevious as mdp


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
    path_data_predict_price = "data/Predict_Price.csv"

    #number items to list
    number_items_rented = 5000
    number_filter = 30
    begin_date = pd.to_datetime('2023-01-01')
    end_date = pd.to_datetime('2023-12-31')

    ids_airbnb = ph.get_ids(details_itapema_file)
    ph.gen_filtered_price_file_chunk(price_file_origin, path_filtered_price_file, ids_airbnb)

    #get dataframe with more rented, average price and others
    df_profile = dh.list_airbnb_most_rented(path_filtered_price_file, details_itapema_file, path_property_profile, number_items_rented, True)

    property_profile = df_profile.listing_type.value_counts().head(5)
    print("\nProperty profile - TOP 5: ")
    print(property_profile)

    property_sum = df_profile.listing_type.value_counts().head(5).sum()
    print("\n\nProperty profile percentual - TOP 5: ")
    for i in range(len(property_profile)):
        print("{}\t{:.2f}%".format(property_profile.index[i], 100*property_profile.iloc[i]/property_sum))

    property_profile = df_profile.listing_type.value_counts()
    print("\nNOVO:Property profile - TOP 5: ")
    print(property_profile)

    #check nullable datas
    print('\n Nullable percentual by attributes')
    dh.print_nullables(df_profile)

    #mount graphic prices
    vd.price_graphic(df_profile)

    #create map file in data directory
    vd.generate_map(df_profile, path_map_most_revenue,number_filter)

    #average bedroom and bathroom
    print('\n')
    dh.show_data_more_rented(df_profile, number_filter)

    # path_filtered_price_file
    df_profile_year_date = dh.list_airbnb_most_rented(path_filtered_price_file, details_itapema_file, path_property_profile, number_items_rented, False, begin_date, end_date)
    dh.average_higher_revenues(df_profile_year_date,number_filter)

    # remove faulting data star_rating, response_rate_shown, guest_satisfaction_overall, picture_count
    columns_list = ['ad_id', 'number_of_bathrooms', 'number_of_bedrooms', 'number_of_beds',
                    'listing_type', 'number_rented', 'revenue', 'latitude', 'longitude',
                    'is_superhost', 'number_of_reviews']

    df_profile = dh.fill_nan_values(['number_of_bedrooms', 'number_of_bathrooms', 'number_of_beds'], df_profile_year_date)

    #removing outliers by amount listing type
    df_profile = df_profile.groupby('listing_type').filter(lambda x: len(x) >= 30)

    #run baseline metrics
    mdp.run_ml_previous_data_regression(df_profile, columns_list, 'average_price')

    #another model with better behavior
    mdp.validation_ml_random_forest_model(df_profile, columns_list, 'average_price')


    #Adjusting code to not repeat - Refactor
    df_profile['2023_price'] = df_profile['average_price']
    predict_2023 = mdp.run_ml_random_forest_model(df_profile, columns_list, '2023_price')
    df_profile['2023_predict_price'] = predict_2023

    df_profile['2024_price'] = df_profile['2023_price'] * (1 + 3.81/100)
    predict_2024 = mdp.run_ml_random_forest_model(df_profile, columns_list, '2024_price')
    df_profile['2024_predict_price'] = predict_2024

    df_profile['2025_price'] = df_profile['2024_price'] * (1 + 3.99/100)
    predict_2025 = mdp.run_ml_random_forest_model(df_profile, columns_list, '2025_price')
    df_profile['2025_predict_price'] = predict_2025

    df_profile['2026_price'] = df_profile['2025_price'] * (1 + 4.0/100)
    predict_2026 = mdp.run_ml_random_forest_model(df_profile, columns_list, '2026_price')
    df_profile['2026_predict_price'] = predict_2026

    columns_list_save = ['ad_id', 'number_of_bathrooms', 'number_of_bedrooms', 'number_of_beds',
                    'listing_type', 'number_rented', 'revenue', 'latitude', 'longitude',
                    'is_superhost', 'number_of_reviews', '2023_price', '2023_predict_price', '2024_price',
                         '2024_predict_price', '2025_price', '2025_predict_price', '2026_price', '2026_predict_price']

    df_profile_save = df_profile[columns_list_save]
    df_profile_save.to_csv(path_data_predict_price, index=False, encoding='utf-8', float_format='%.2f')

    print("comparing average real x predict")
    columns_list_price = ['2023_price', '2024_price', '2025_price', '2026_price']
    columns_list_predict = ['2023_predict_price', '2024_predict_price', '2025_predict_price', '2026_predict_price']

    for i in range(len(columns_list_price)):
        print(columns_list_price[i] + ' = ' + format(df_profile_save[columns_list_price[i]].mean(), '.2f'))
        print(columns_list_predict[i] + ' = ' + format(df_profile_save[columns_list_predict[i]].mean(),  '.2f'))

    print("\nFinished processing")