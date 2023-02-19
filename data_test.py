import json
import pandas as pd



def clean_zillow_json(string_dict):
    if type(string_dict) == str:
        good_string = string_dict.replace("'", '"').replace("True", 'true').replace("False", 'false')
        good_dict = json.loads(good_string)
        return good_dict
    else:
        if type(string_dict)  != float:
            return string_dict['homeInfo']
    return None


def get_rent_zestimate(string_dict):
    good_dict = clean_zillow_json(string_dict)
    try:
        value = good_dict['rentZestimate']
    except:
        return None
    return value


def get_price(string_dict):
    good_dict = clean_zillow_json(string_dict)
    try:
        value = good_dict['price']
    except:
        return None
    return value


def get_zestimate_price(string_dict):
    good_dict = clean_zillow_json(string_dict)
    try:
        value = good_dict['zestimate']
    except:
        return None
    return value




def clean_data(dataframe):
    drop_columns = ['priceLabel', 'latLong', 'statusType', 'isFavorite', 'isUserClaimingOwner',
                    'isUserConfirmedClaim', 'listingType', 'pgapt', 'sgapt', 'hasVideo', 'isHomeRec',
                    'hasAdditionalAttributions',
                    'isFeaturedListing', 'availabilityDate', 'minBeds', 'minBaths', 'minArea', 'isBuilding',
                    'badgeInfo', 'canSaveBuilding', 'hasImage', 'visited', 'has3DModel', 'buildingId', 'lotId', ]
    df = dataframe
    value = df.loc[0, "hdpData"]
    print('Data Received')
    df = df.drop(columns=drop_columns)
    print('Dropping Columns')
    return df

if __name__ == '__main__':
    data_input = pd.DataFrame(pd.read_json('response.json')['cat1']['searchResults']['mapResults'])
    df = clean_data(data_input)
    df['clean_rent'] = df.apply(lambda row: get_rent_zestimate(row['hdpData']), axis=1)
    df['clean_price'] = df.apply(lambda row: get_price(row['hdpData']), axis=1)
    df['zestimate'] = df.apply(lambda row: get_zestimate_price(row['hdpData']), axis=1)
    # df['1% Rule'] = df['clean_rent'] / df['clean_price'] * 100
    df['address'] = "zillow.com" + df['detailUrl']
    df.to_csv('new_home_list.csv', index=False, mode='a')
    print('Data Written to new_home_list.csv')







