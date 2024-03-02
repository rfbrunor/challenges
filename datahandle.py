import os
import pandas as pd
import numpy as np

def print_nullables(dataframe):
    df = pd.DataFrame({'nullable values': np.round(dataframe.isnull().mean(), 2),
                  'data_type': dataframe.dtypes,
                  'unique_values': dataframe.nunique()})
    print(df)

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