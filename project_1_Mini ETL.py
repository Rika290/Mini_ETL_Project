from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

def extract():
        url = 'https://randomuser.me/api/?results=100'
        resp=requests.get(url)
        data=resp.json()['results']
        df = pd.json_normalize(data)
        df.to_csv('/mnt/c/Users/RAJASEKARAN IPS/Downloads/Mini_Project/api_data.csv',index=False)

def transform():
        df=pd.read_csv('/mnt/c/Users/RAJASEKARAN IPS/Downloads/Mini_Project/api_data.csv')
        print('No.of rows and columns:',df.shape)
        print('No.of missing values:',df.isnull().sum())
        print('Columns:',df.columns)
        df=df.drop(columns=['cell', 'nat','id.name', 'id.value', 'picture.large','picture.medium','picture.thumbnail' , 
        'registered.age', 'login.password', 'login.salt','login.md5', 'login.sha1','login.sha256', 'dob.date',
        'location.coordinates.latitude','location.coordinates.longitude', 'location.timezone.offset',
        'location.timezone.description', 'login.uuid','location.street.number','location.street.name',
        'location.city','location.state','location.postcode'])
        print('No.of rows and columns after dropping:',df.shape)
        df=df.rename(columns={'name.title':'title', 'name.first':'first_name', 'name.last':'last_name',
        'location.country':'country', 'login.username':'username', 'dob.age':'age', 
        'registered.date':'date_registered'}) # renaming columns
        df['date_registered']=pd.to_datetime(df['date_registered']) # converting to a datetime
        df['name']=df['first_name']+' '+df['last_name']  # joining 2 columns
        df=df.drop(columns=['first_name', 'last_name'])  # removing columns
        df=df[['name','gender', 'email', 'phone', 'title', 'country', 'username', 'age','date_registered']] # re ordering columns
        df['gender']=df['gender'].str.title() # 
        print('After transformation:',df.head()) 
        # saving the transformed 
        df.to_csv('/mnt/c/Users/RAJASEKARAN IPS/Downloads/Mini_Project/transformed_api_data.csv',index=False)

def load():
        df=pd.read_csv('/mnt/c/Users/RAJASEKARAN IPS/Downloads/Mini_Project/transformed_api_data.csv')

        hook=SnowflakeHook(snowflake_conn_id='snowflake_conn')
        conn=hook.get_conn()
        cursor=conn.cursor()
        
        cursor.execute("""
        create table if not exists info_table(
        name STRING,
        gender STRING,
        email STRING,
        phone STRING,
        title STRING,
        country STRING, 
        username STRING,
        age INTEGER,
        date_registered TIMESTAMP                                                                       
        )
        """)

        for _,row in df.iterrows():
                cursor.execute("""
            INSERT INTO info_table (name, gender, email, phone, title, country, username, age, date_registered)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, tuple(row))
        
        conn.commit()
        cursor.close()
        conn.close()
       
with DAG(dag_id='mini_ETL_project',start_date=datetime(2025,7,18),
    schedule_interval=None,catchup=False) as dag:
        
        ext=PythonOperator(
            task_id='extract_data_api',
            python_callable=extract
        )

        tran=PythonOperator(
                task_id='transform_data_api',
                python_callable=transform
        )

        loa=PythonOperator(
                task_id='load_to_snowflake',
                python_callable=load
        )

ext >> tran >> loa 
    
    

