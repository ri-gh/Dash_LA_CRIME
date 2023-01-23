import pandas as pd

url='https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD'


df = pd.read_csv(url)

#We are going to add a column 'Type of crime' to categorize each crime description given by key word
#We instanciate a list of key word for crime
vandalism = ['VANDALISM']
list_of_crime_sex =['SEX','RAPE','INCEST','INDECENT','HUMAN','PANDERING','BIGAMY','LEWD','PIMPING','ORAL COPULATION']
list_of_crime_theft = ['THEFT','ROBBERY','BURGLARY','STOLEN','VEHICLE','PICKPOCKET','DRIVING WITHOUT OWNER CONSENT (DWOC)','SNATCH','SHOPLIFTING','EXTORTION']
simple_assault = ['SIMPLE ASSAULT']
aggravated_assault = ['AGGRAVATED ASSAULT']

#here s a list for the remaining crime:
crime_categoy_desc_list = vandalism + list_of_crime_sex+ list_of_crime_theft+ simple_assault+aggravated_assault

#we create several df where crime description contains the listed key word
df_vandalism = df[df['Crm Cd Desc'].str.contains('{}'.format('|'.join(vandalism)))]
df_vandalism['Type of crime'] = 'Vandalism'

df_sex_crime = df[df['Crm Cd Desc'].str.contains('{}'.format('|'.join(list_of_crime_sex)))]
df_sex_crime['Type of crime'] = 'Sex crime'

df_theft_crime = df[df['Crm Cd Desc'].str.contains('{}'.format('|'.join(list_of_crime_theft)))]
df_theft_crime['Type of crime'] = 'Theft'

df_simple_assault = df[df['Crm Cd Desc'].str.contains('{}'.format('|'.join(simple_assault)))]
df_simple_assault['Type of crime'] = 'Simple assault'

df_aggravated_assault = df[df['Crm Cd Desc'].str.contains('{}'.format('|'.join(aggravated_assault)))]
df_aggravated_assault['Type of crime'] = 'Aggravated assault'

#the columns not containing one of the crime description keyword listed upper will be tagged as type 'other'
df_other_crime = df[~df['Crm Cd Desc'].str.contains('{}'.format('|'.join(crime_categoy_desc_list)))]
df_other_crime['Type of crime'] = 'other'

#we'll append the full df with the new column 'Type of crime' & comments added inside
df_to_append = [df_sex_crime ,df_theft_crime , df_simple_assault, df_aggravated_assault,df_vandalism]

df_global = df_other_crime.append(df_to_append)
df_global = df_global.reset_index(drop=True)

#to show %age of null values bor each column
percentage_null_value =df_global.isnull().sum()/df_global.shape[0]*100
percentage_null_value.sort_values(ascending=False)

#we'll remove columns we more than 50% of missing values
col_to_remove = []
for i in range (len(percentage_null_value)):
    if percentage_null_value.values[i] > 50:
        col_to_remove.append(percentage_null_value.index[i])


df = df_global.drop(labels = col_to_remove, axis=1)

df = df.fillna("unkown")

#reformating the date data:

df['Date Rptd'] = df['Date Rptd'].str.split(' ',expand=True)[0]
df['DATE OCC'] = df['DATE OCC'].str.split(' ',expand=True)[0]
df['DATE OCC'] = pd.to_datetime(df['DATE OCC'])
df['Date Rptd'] = pd.to_datetime(df['Date Rptd'])

df['TIME OCC'] = pd.to_datetime(df['TIME OCC'].astype(str).str.zfill(4), format='%H%M')

#to get unique values count for each column to remove the uninteristing ones:
pd.DataFrame(df.nunique())

#we remove the below columns with too much useless data(redundancy, not signifiant data):
df = df.drop(labels=['DR_NO','Part 1-2','AREA','Crm Cd','Crm Cd 1','Premis Cd','Status','Mocodes'],axis=1)


#create & extract year / month/ day / day-name / hour from existing date columns
df['year']= df['DATE OCC'].dt.year
df['month']= df['DATE OCC'].dt.month
df['month_name']= df['DATE OCC'].dt.month_name()
df['day']= df['DATE OCC'].dt.day
df['day_name']= df['DATE OCC'].dt.day_name()
df['hour'] = df['TIME OCC'].dt.hour

df['TIME OCC'] = df['TIME OCC'].astype(str).str.split(' ' , expand=True)[1]

#to save the cleaned file to csv
df.to_csv("LA_Crime_clean.csv")
