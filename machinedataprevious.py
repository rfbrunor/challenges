from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

def run_ml_previous_data_regression(dataframe, colum_list, price_col_name):
    X = dataframe[colum_list]
    y = dataframe[price_col_name]

    X_enc = X.copy()
    le = LabelEncoder()

    le.fit(X['listing_type'])
    X_enc['listing_type'] = le.transform(X['listing_type'])

    reg = LinearRegression()
    reg.fit(X_enc, y)

    y_pred_train = reg.predict(X_enc)

    print(f'\nTraining data prediction Linear Regression:')
    print('-----------------------------------------------------')
    print(f'Mean Squared Error: {mean_squared_error(dataframe.average_price, y_pred_train)}')
    print(f'Mean Absolute Error: {mean_absolute_error(dataframe.average_price, y_pred_train)}')
    print(f'R2 score: {r2_score(dataframe.average_price, y_pred_train)}\n')

    return y_pred_train


def validation_ml_random_forest_model(dataframe, columns_list, price_col_name):
    seed = 1
    df_train_val = dataframe

    X = df_train_val[columns_list]
    y = df_train_val[price_col_name]
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=seed)

    X_train_enc = X_train.copy()
    X_val_enc = X_val.copy()

    le = LabelEncoder()

    # training data
    le.fit(X_train['listing_type'])

    X_train_enc['listing_type'] = le.transform(X_train['listing_type'])
    X_val_enc['listing_type'] = le.transform(X_val_enc['listing_type'])

    rf = RandomForestRegressor(n_estimators=1000)
    rf.fit(X_train_enc, y_train)

    y_pred_train = rf.predict(X_train_enc)
    y_pred_val = rf.predict(X_val_enc)
    #
    print(f'\nTraining data prediction Random Forest:')
    print('-----------------------------------------------------')
    print(f'Mean Squared Error: {mean_squared_error(y_train, y_pred_train)}')
    print(f'Mean Absolute Error: {mean_absolute_error(y_train, y_pred_train)}')
    print(f'R2 score: {r2_score(y_train, y_pred_train)}\n')

    print(f'Validation data prediction Random Forest:')
    print('-----------------------------------------------------')
    print(f'Mean Squared Error: {mean_squared_error(y_val, y_pred_val)}')
    print(f'Mean Absolute Error: {mean_absolute_error(y_val, y_pred_val)}')
    print(f'R2 score: {r2_score(y_val, y_pred_val)}')

def run_ml_random_forest_model(dataframe, columns_list, price_col_name):
    df_train_val = dataframe

    X = df_train_val[columns_list]
    y = df_train_val[price_col_name]

    X_train_enc = X.copy()

    le = LabelEncoder()

    # training data
    le.fit(X['listing_type'])

    X_train_enc['listing_type'] = le.transform(X['listing_type'])

    rf = RandomForestRegressor(n_estimators=1000)
    rf.fit(X_train_enc, y)

    y_pred_train = rf.predict(X_train_enc)
    #
    print(f'\nTraining data prediction Random Forest ' + price_col_name + ' :')
    print('-----------------------------------------------------')
    print(f'Mean Squared Error: {mean_squared_error(y, y_pred_train)}')
    print(f'Mean Absolute Error: {mean_absolute_error(y, y_pred_train)}')
    print(f'R2 score: {r2_score(y, y_pred_train)}\n')

    return y_pred_train
