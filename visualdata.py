import numpy as np
import folium
import matplotlib.pyplot as plt
def generate_map(dataframe, path_save, number_filter):
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

