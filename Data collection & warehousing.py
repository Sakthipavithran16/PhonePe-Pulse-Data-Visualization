# Importing thr necessary libraries
import os
import pandas as pd
import json
import mysql.connector


# Cleaning the data 
def cleaning_data(df):
    df['States'] = df['States'].str.replace('-', ' ')
    df['States'] = df['States'].str.title()
    df['States'] = df['States'].str.replace('Andaman & Nicobar Islands', 'Andaman & Nicobar')
    df['States'] = df['States'].str.replace('Dadra & Nagar Haveli & Daman & Diu','Dadra and Nagar Haveli and Daman and Diu')

    return df


# Aggregated Insurance data collection
def agg_ins_collect():
    agg_ins_path = "D:/PhonePe_Project/pulse/data/aggregated/insurance/country/india/state"

    # os.listdir is used to get the list of all files and directories in the specified directory.
    agg_ins_states = os.listdir(agg_ins_path)  

    agg_ins_columns = {"States" :[], "Year":[], "Quater":[], "Transaction_type":[], "Transaction_count":[],"Transaction_amount":[] }

    for state in agg_ins_states:
        state_path = agg_ins_path + "/" + state 
        agg_ins_year = os.listdir(state_path)
        
        for year in agg_ins_year:
            year_path = state_path + "/" + year 
            agg_ins_quaters = os.listdir(year_path)

            for quater in agg_ins_quaters:
                quater_path = year_path + "/" + quater
                file = open(quater_path,'r')
                ins_data = json.load(file)

                try:
                    name = ins_data['data']['transactionData'][0]['name']
                    count = ins_data['data']['transactionData'][0]['paymentInstruments'][0]['count']
                    amount = ins_data['data']['transactionData'][0]['paymentInstruments'][0]['amount']
                    
                    agg_ins_columns["Transaction_type"].append(name)
                    agg_ins_columns["Transaction_count"].append(count)
                    agg_ins_columns["Transaction_amount"].append(amount)

                    agg_ins_columns["States"].append(state)
                    agg_ins_columns["Year"].append(year)
                    agg_ins_columns["Quater"].append(int(quater.strip(".json")))

                except:
                    pass

    agg_ins_data = pd.DataFrame(agg_ins_columns)

    final_df = cleaning_data(agg_ins_data)

    return final_df


agg_ins_data = agg_ins_collect()



# Aggregated Transaction data collection
def agg_trans_collect():
    agg_trans_path = "D:/PhonePe_Project/pulse/data/aggregated/transaction/country/india/state"
    agg_trans_states = os.listdir(agg_trans_path)

    agg_trans_columns = {"States" :[], "Year":[], "Quater":[], "Transaction_type":[], "Transaction_count":[],"Transaction_amount":[] }

    for state in agg_trans_states:
        state_path = agg_trans_path + "/" + state 
        agg_trans_year = os.listdir(state_path)
        
        for year in agg_trans_year:
            year_path = state_path + "/" + year 
            agg_trans_quaters = os.listdir(year_path)

            for quater in agg_trans_quaters:
                quater_path = year_path + "/" + quater
                file = open(quater_path,'r')
                trans_data = json.load(file)

                name = trans_data['data']['transactionData'][0]['name']
                count = trans_data['data']['transactionData'][0]['paymentInstruments'][0]['count']
                amount = trans_data['data']['transactionData'][0]['paymentInstruments'][0]['amount']

                agg_trans_columns["Transaction_type"].append(name)
                agg_trans_columns["Transaction_count"].append(count)
                agg_trans_columns["Transaction_amount"].append(amount)

                agg_trans_columns["States"].append(state)
                agg_trans_columns["Year"].append(year)
                agg_trans_columns["Quater"].append(int(quater.strip(".json")))

    agg_trans_data = pd.DataFrame(agg_trans_columns)

    final_df = cleaning_data(agg_trans_data)

    return final_df


agg_trans_data = agg_trans_collect()



# Aggregated User data collection
def agg_user_collect():
    agg_user_path = "D:/PhonePe_Project/pulse/data/aggregated/user/country/india/state/"
    agg_user_states = os.listdir(agg_user_path)

    agg_user_columns = {"States" :[], "Year":[], "Quater":[], "Transaction_device":[], "Transaction_count":[],"Transaction_percentage":[] }

    for state in agg_user_states:
        state_path = agg_user_path + "/" + state 
        agg_user_year = os.listdir(state_path)

        for year in agg_user_year:
            year_path = state_path + "/" + year 
            agg_user_quaters = os.listdir(year_path)

            for quater in agg_user_quaters:
                quater_path = year_path + "/" + quater
                file = open(quater_path,'r')
                user_data = json.load(file)
                
                try:
                    for info in user_data['data']['usersByDevice']:
                        brand = info['brand']
                        count = info['count']
                        per = info['percentage']
                    
                        agg_user_columns['Transaction_device'].append(brand)
                        agg_user_columns['Transaction_count'].append(count)
                        agg_user_columns['Transaction_percentage'].append(per)

                        agg_user_columns["States"].append(state)
                        agg_user_columns["Year"].append(year)
                        agg_user_columns["Quater"].append(int(quater.strip(".json")))
                
                except:
                    pass

    agg_user_data = pd.DataFrame(agg_user_columns)

    final_df = cleaning_data(agg_user_data)

    return final_df


agg_user_data = agg_user_collect()



# Map Insurance data collection
def map_ins_collect():
    map_ins_path = "D:/PhonePe_Project/pulse/data/map/insurance/hover/country/india/state"
    map_ins_states = os.listdir(map_ins_path)

    map_ins_columns = {"States" :[], "Year":[], "Quater":[], "District_name":[], "Insurance_count":[],"Insurance_amount":[] }

    for state in map_ins_states:
        state_path = map_ins_path + "/" + state 
        map_ins_year = os.listdir(state_path)
        
        for year in map_ins_year:
            year_path = state_path + "/" + year 
            map_ins_quaters = os.listdir(year_path)

            for quater in map_ins_quaters:
                quater_path = year_path + "/" + quater
                file = open(quater_path,'r')
                m_ins_data = json.load(file)

                details = m_ins_data['data']['hoverDataList']

                for info in range(0,len(details)):
                    name = details[info]['name']
                    count = details[info]['metric'][0]['count']
                    amount = details[info]['metric'][0]['amount']
                    
                    map_ins_columns["District_name"].append(name)
                    map_ins_columns["Insurance_count"].append(count)
                    map_ins_columns["Insurance_amount"].append(amount)

                    map_ins_columns["States"].append(state)
                    map_ins_columns["Year"].append(year)
                    map_ins_columns["Quater"].append(int(quater.strip(".json")))

    map_ins_data = pd.DataFrame(map_ins_columns)

    final_df = cleaning_data(map_ins_data)

    return final_df


map_ins_data = map_ins_collect()



# Map Transactions data collection
def map_trans_collect():
    map_trans_path = "D:/PhonePe_Project/pulse/data/map/transaction/hover/country/india/state/"
    map_trans_states = os.listdir(map_trans_path)

    map_trans_columns = {"States" :[], "Year":[], "Quater":[], "District_name":[], "Transaction_count":[],"Transaction_amount":[] }

    for state in map_trans_states:
        state_path = map_trans_path + "/" + state 
        map_trans_year = os.listdir(state_path)
        
        for year in map_trans_year:
            year_path = state_path + "/" + year 
            map_trans_quaters = os.listdir(year_path)

            for quater in map_trans_quaters:
                quater_path = year_path + "/" + quater
                file = open(quater_path,'r')
                mtrans_data = json.load(file)

                details = mtrans_data['data']['hoverDataList']

                for info in range(0,len(details)):
                    name = details[info]['name']
                    
                    count = details[info]['metric'][0]['count']
                    amount = details[info]['metric'][0]['amount']

                    map_trans_columns["District_name"].append(name)
                    map_trans_columns["Transaction_count"].append(count)
                    map_trans_columns["Transaction_amount"].append(amount)

                    map_trans_columns["States"].append(state)
                    map_trans_columns["Year"].append(year)
                    map_trans_columns["Quater"].append(int(quater.strip(".json")))

    map_trans_data = pd.DataFrame(map_trans_columns)

    final_df = cleaning_data(map_trans_data)

    return final_df


map_trans_data = map_trans_collect()



# Map User data collection
def map_user_collect():
    map_user_path = "D:/PhonePe_Project/pulse/data/map/user/hover/country/india/state/"
    map_user_states = os.listdir(map_user_path)

    map_user_columns = {"States" :[], "Year":[], "Quater":[], "District_name":[], "Registered_users":[],"App_opens":[] }

    for state in map_user_states:
        state_path = map_user_path + "/" + state 
        map_user_year = os.listdir(state_path)
        
        for year in map_user_year:
            year_path = state_path + "/" + year 
            map_user_quaters = os.listdir(year_path)

            for quater in map_user_quaters:
                quater_path = year_path + "/" + quater
                file = open(quater_path,'r')
                muser_data = json.load(file)
                
                try:
                    lst =[]
                    details = muser_data['data']['hoverData']
                    for info in details.items():
                        lst.append(info[0])
                        
                    for district in lst:
                            reg_user = details[district]['registeredUsers']
                            app_opens = details[district]['appOpens']
                    
                            map_user_columns['District_name'].append(district)
                            map_user_columns['Registered_users'].append(reg_user)
                            map_user_columns['App_opens'].append(app_opens)

                            map_user_columns["States"].append(state)
                            map_user_columns["Year"].append(year)
                            map_user_columns["Quater"].append(int(quater.strip(".json")))
                
                except:
                    pass

    map_user_data = pd.DataFrame(map_user_columns)

    final_df = cleaning_data(map_user_data)

    return final_df


map_user_data = map_user_collect()



# Top Insurance data collection
def top_ins_collect():
    top_ins_path = "D:/PhonePe_Project/pulse/data/top/insurance/country/india/state"
    top_ins_states = os.listdir(top_ins_path)

    top_ins_columns = {"States" :[], "Year":[], "Quater":[], "Pincodes":[], "Insurance_count":[],"Insurance_amount":[] }

    for state in top_ins_states:
        state_path = top_ins_path + "/" + state 
        top_ins_year = os.listdir(state_path)
        
        for year in top_ins_year:
            year_path = state_path + "/" + year 
            top_ins_quaters = os.listdir(year_path)

            for quater in top_ins_quaters:
                quater_path = year_path + "/" + quater
                file = open(quater_path,'r')
                t_ins_data = json.load(file)

                details = t_ins_data['data']['pincodes']

                for info in range(0,len(details)):

                    name = details[info]['entityName']
                    count = details[info]['metric']['count']
                    amount = details[info]['metric']['amount']
                    
                    top_ins_columns["Pincodes"].append(name)
                    top_ins_columns["Insurance_count"].append(count)
                    top_ins_columns["Insurance_amount"].append(amount)

                    top_ins_columns["States"].append(state)
                    top_ins_columns["Year"].append(year)
                    top_ins_columns["Quater"].append(int(quater.strip(".json")))

    top_ins_data = pd.DataFrame(top_ins_columns)

    final_df = cleaning_data(top_ins_data)

    return final_df


top_ins_data = top_ins_collect()



# Top transactions data collection
def top_trans_collect():
    top_trans_path = "D:/PhonePe_Project/pulse/data/top/transaction/country/india/state"
    top_trans_states = os.listdir(top_trans_path)

    top_trans_columns = {"States" :[], "Year":[], "Quater":[], "Pincodes":[], "Transaction_count":[],"Transaction_amount":[] }

    for state in top_trans_states:
        state_path = top_trans_path + "/" + state 
        top_trans_year = os.listdir(state_path)
        
        for year in top_trans_year:
            year_path = state_path + "/" + year 
            top_trans_quaters = os.listdir(year_path)

            for quater in top_trans_quaters:
                quater_path = year_path + "/" + quater
                file = open(quater_path,'r')
                ttrans_data = json.load(file)

                details = ttrans_data['data']['pincodes']

                for info in range(0,len(details)):
                    name = details[info]['entityName']
                    count = details[info]['metric']['count']
                    amount = details[info]['metric']['amount']

                    top_trans_columns["Pincodes"].append(name)
                    top_trans_columns["Transaction_count"].append(count)
                    top_trans_columns["Transaction_amount"].append(amount)

                    top_trans_columns["States"].append(state)
                    top_trans_columns["Year"].append(year)
                    top_trans_columns["Quater"].append(int(quater.strip(".json")))

    top_trans_data = pd.DataFrame(top_trans_columns)

    final_df = cleaning_data(top_trans_data)

    return final_df


top_trans_data = top_trans_collect()


# Top User data collection
def top_user_collect():
    top_user_path = "D:/PhonePe_Project/pulse/data/top/user/country/india/state/"
    top_user_states = os.listdir(top_user_path)

    top_user_columns = {"States" :[], "Year":[], "Quater":[], "Pincodes":[], "Registered_users":[]}

    for state in top_user_states:
        state_path = top_user_path + "/" + state 
        top_user_year = os.listdir(state_path)
        
        for year in top_user_year:
            year_path = state_path + "/" + year 
            top_user_quaters = os.listdir(year_path)

            for quater in top_user_quaters:
                quater_path = year_path + "/" + quater
                file = open(quater_path,'r')
                tuser_data = json.load(file)

                details = tuser_data['data']['pincodes']

                for info in range(0,len(details)):
                    name = details[info]['name']
                    reg_user = details[info]['registeredUsers']
            
                    top_user_columns['Pincodes'].append(name)
                    top_user_columns['Registered_users'].append(reg_user)

                    top_user_columns["States"].append(state)
                    top_user_columns["Year"].append(year)
                    top_user_columns["Quater"].append(int(quater.strip(".json")))

    top_user_data = pd.DataFrame(top_user_columns)

    final_df = cleaning_data(top_user_data)

    return final_df


top_user_data = top_user_collect()



# Data Warehousing 

mydb = mysql.connector.connect(host="localhost", user="root", password="sakthi", auth_plugin='mysql_native_password')

mycursor = mydb.cursor()

mycursor.execute("CREATE database IF NOT EXISTS PhonePe")

mycursor.execute("USE PhonePe")

# Aggegrated Insurance
def agg_ins_to_db(data):
    
    mycursor.execute('''CREATE table IF NOT EXISTS Aggregated_Insurance (
                            States varchar(255),
                            Year int,
                            Quater int,
                            Transaction_type varchar(255),
                            Transaction_count bigint,
                            Transaction_amount bigint
                            )''')

    sql = ''' INSERT INTO Aggregated_Insurance (States, Year, Quater, Transaction_type, Transaction_count, Transaction_amount)
                                                values(%s, %s, %s, %s, %s, %s)'''

    val = data.values.tolist()

    mycursor.executemany(sql,val)

    mydb.commit()


# Aggregated Transaction
def agg_trans_to_db(data):
    
    mycursor.execute('''CREATE table IF NOT EXISTS Aggregated_Transaction (
                            States varchar(255),
                            Year int,
                            Quater int,
                            Transaction_type varchar(255),
                            Transaction_count bigint,
                            Transaction_amount bigint
                            )''')

    sql = ''' INSERT INTO Aggregated_Transaction (States, Year, Quater, Transaction_type, Transaction_count, Transaction_amount)
                                                values(%s, %s, %s, %s, %s, %s)'''

    val = data.values.tolist()

    mycursor.executemany(sql,val)

    mydb.commit()


# Aggregated User
def agg_user_to_db(data):
    
    mycursor.execute('''CREATE table IF NOT EXISTS Aggregated_User (
                            States varchar(255),
                            Year int,
                            Quater int,
                            Transaction_device varchar(255),
                            Transaction_count bigint,
                            Transaction_percentage float
                            )''')

    sql = ''' INSERT INTO Aggregated_User (States, Year, Quater, Transaction_device, Transaction_count, Transaction_percentage)
                                                values(%s, %s, %s, %s, %s, %s)'''

    val = data.values.tolist()

    mycursor.executemany(sql,val)

    mydb.commit()


# Map Insurance
def map_ins_to_db(data):
    
    mycursor.execute('''CREATE table IF NOT EXISTS Map_Insurance (
                            States varchar(255),
                            Year int,
                            Quater int,
                            District_name varchar(255),
                            Insurance_count bigint,
                            Insurance_amount bigint
                            )''')

    sql = ''' INSERT INTO Map_Insurance (States, Year, Quater, District_name, Insurance_count, Insurance_amount)
                                                values(%s, %s, %s, %s, %s, %s)'''

    val = data.values.tolist()

    mycursor.executemany(sql,val)

    mydb.commit()


# Map Transaction
def map_trans_to_db(data):
    
    mycursor.execute('''CREATE table IF NOT EXISTS Map_Transaction (
                            States varchar(255),
                            Year int,
                            Quater int,
                            District_name varchar(255),
                            Transaction_count bigint,
                            Transaction_amount bigint
                            )''')

    sql = ''' INSERT INTO Map_Transaction (States, Year, Quater, District_name, Transaction_count, Transaction_amount)
                                                values(%s, %s, %s, %s, %s, %s)'''

    val = data.values.tolist()

    mycursor.executemany(sql,val)

    mydb.commit()   


# Map User
def map_user_to_db(data):
    
    mycursor.execute('''CREATE table IF NOT EXISTS Map_User (
                            States varchar(255),
                            Year int,
                            Quater int,
                            District_name varchar(255),
                            Registered_users bigint,
                            App_opens bigint
                            )''')

    sql = ''' INSERT INTO Map_User (States, Year, Quater, District_name, Registered_users, App_opens)
                                                values(%s, %s, %s, %s, %s, %s)'''

    val = data.values.tolist()

    mycursor.executemany(sql,val)

    mydb.commit()


# Top Insurance
def top_ins_to_db(data):
    
    mycursor.execute('''CREATE table IF NOT EXISTS Top_Insurance (
                            States varchar(255),
                            Year int,
                            Quater int,
                            Pincodes varchar(255),
                            Insurance_count bigint,
                            Insurance_amount bigint
                            )''')

    sql = ''' INSERT INTO Top_Insurance (States, Year, Quater, Pincodes, Insurance_count, Insurance_amount)
                                                values(%s, %s, %s, %s, %s, %s)'''

    val = data.values.tolist()

    mycursor.executemany(sql,val)

    mydb.commit()


# Top Transaction
def top_trans_to_db(data):
    
    mycursor.execute('''CREATE table IF NOT EXISTS Top_Transaction (
                            States varchar(255),
                            Year int,
                            Quater int,
                            Pincodes varchar(255),
                            Transaction_count bigint,
                            Transaction_amount bigint
                            )''')

    sql = ''' INSERT INTO Top_Transaction (States, Year, Quater, Pincodes, Transaction_count, Transaction_amount)
                                                values(%s, %s, %s, %s, %s, %s)'''

    val = data.values.tolist()

    mycursor.executemany(sql,val)

    mydb.commit()


# Top User
def top_user_to_db(data):
    
    mycursor.execute('''CREATE table IF NOT EXISTS Top_User (
                            States varchar(255),
                            Year int,
                            Quater int,
                            Pincodes varchar(255),
                            Registered_users int
                            )''')

    sql = ''' INSERT INTO Top_User (States, Year, Quater, Pincodes, Registered_users)
                                                values(%s, %s, %s, %s, %s)'''

    val = data.values.tolist()

    mycursor.executemany(sql,val)

    mydb.commit()


agg_ins_to_db(agg_ins_data)
agg_trans_to_db(agg_trans_data)
agg_user_to_db(agg_user_data)

map_ins_to_db(map_ins_data)
map_trans_to_db(map_trans_data)
map_user_to_db(map_user_data)

top_ins_to_db(top_ins_data)
top_trans_to_db(top_trans_data)
top_user_to_db(top_user_data)