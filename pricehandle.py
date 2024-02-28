import os
import pandas as pd

def generate_filtered_price_file(path_price_origin, path_price_filtered):
    if os.path.exists(path_price_filtered):
        print("Found filtered price file")
    else:
        df_price_file = pd.read_csv(path_price_origin, low_memory=False)

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

