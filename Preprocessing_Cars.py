import pandas as pd
import re


def preprocessing(cars_data):
    
    # 10 Data teratas
    cars_data.head(10)
    
    # Statistik dari tiap kolom
    cars_data.describe(include = 'all')
    
    # Tipe data dari tiap kolom
    cars_data.info()
    
    # Persentase nilai null
    (cars_data.isnull().sum()) / (len(cars_data) * 100)
    
    # mengubah nama kolom
    new_columns = cars_data.columns.tolist()
    for index,columns_name in enumerate(new_columns):
      if columns_name == 'dateCreated':
        new_columns[index] = 'ad_created'
      elif columns_name == 'monthOfRegistration':
        new_columns[index] = 'registration_month'
      elif columns_name == 'notRepairedDamage':
        new_columns[index] = 'unrepaired_damage'
      elif columns_name == 'nrOfPictures':
        new_columns[index] = "num_of_pictures"
      elif columns_name == "powerPS": 
        new_columns[index] = "power_ps"
      elif columns_name == "yearOfRegistration": 
        new_columns[index] = "registration_year"
      else:
        new_columns[index] = re.sub(r'(?<!^)(?=[A-Z])', '_', columns_name).lower()
    
    cars_data.rename(columns = dict(zip(cars_data.columns.tolist(),new_columns)),inplace = True)
    
    # data cleaning    
    cars_data['odometer'] = cars_data['odometer'].str.replace(",","",regex = False).str.replace("km","",regex = False).astype('int64')
    cars_data['price'] = cars_data['price'].str.replace("$","",regex = False).str.replace(",","",regex = False).astype('int64')
    
    # drop kolom
    for column_name in cars_data.columns:
      # apabila kolom bukan tipe waktu dan banyaknya nilai unik lebih dari 10% 
      if (cars_data[column_name].dtypes != '<M8[ns]') and ((len(cars_data[column_name].value_counts()) / len(cars_data)) * 100 >= 10):
       print('kolom', column_name, cars_data[column_name].dtypes)
       cars_data.drop(columns = [column_name],inplace = True)
      # apabila kolom string memiliki perbandingan hanya 2 data dan nilai kolom pertama lebih dari 60%, drop kolom
      elif (cars_data[column_name].dtypes == 'O') and (len(cars_data[column_name].value_counts()) == 2) and ((cars_data[column_name].value_counts()[0] / cars_data[column_name].value_counts().sum() * 100) >= 60):
        print('kolom',column_name, cars_data[column_name].dtypes)
        cars_data.drop(columns = [column_name],inplace = True)
      # apabila integer dan banyaknya nilai unik hanya 1 saja
      elif ((cars_data[column_name].dtypes == 'int64') and (len(cars_data[column_name].value_counts()) == 1)):
        print('kolom',column_name, cars_data[column_name].dtypes)
        cars_data.drop(columns = [column_name], inplace = True)
    
    # drop outliers
    cars_data = cars_data.loc[(cars_data['price'] >= 500) & (cars_data['price'] <= 40000)]
    print(cars_data['price'].sort_values())
    
    # imputation
    for column_name in cars_data.columns:
      if (cars_data[column_name].dtypes == 'O') :
        mode_value = cars_data[column_name].mode()[0]
        cars_data[column_name].fillna(value = mode_value, inplace = True)
      elif ((cars_data[column_name].dtypes == 'int64') or (cars_data[column_name].dtypes == 'float64')):
        mean_value = cars_data[column_name].mean()
        cars_data[column_name].fillna(value = mean_value, inplace = True)
    
    # normalisasi dengan min-max scaler
    for column_name in cars_data.columns:
      if (cars_data[column_name].dtypes == 'int64') & (column_name not in ['registration_year','registration_month']):
        print(column_name)
        cars_data[column_name] = ((cars_data[column_name]-cars_data[column_name].min())/(cars_data[column_name].max()-cars_data[column_name].min()))
    
    
   # encoding dengan dummies
    columns_to_encode = []
    for columns in cars_data.columns:
      if cars_data[columns].dtypes in ['object','int64']:
        columns_to_encode.append(columns)
    
    cars_data = pd.get_dummies(data = cars_data, columns = columns_to_encode)
    return cars_data

data = pd.read_csv('Data/autos.csv',encoding = 'unicode_escape')
preprocessing(data)