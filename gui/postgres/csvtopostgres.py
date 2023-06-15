import pandas as pd
from sqlalchemy import create_engine
from postgres import postgres_info as psg_info

# CSV dosyasını oku
df = pd.read_csv('data\\globalterrorismdb_0718dist.csv')

# Veritabanına bağlan
database_name = psg_info.database_name
user_name = psg_info.user_name
password = psg_info.password
host_ip = psg_info.host_ip
host_port = psg_info.host_port

# Veritabanı bağlantısını oluştur
engine = create_engine(f'postgresql://{user_name}:{password}@{host_ip}:{host_port}/{database_name}')

# Veriyi PostgreSQLe aktar
df.to_sql('terrors', engine, if_exists='replace')

# Sütun isimlerini al
column_names = df.columns.tolist()

# Sütun tiplerini al
column_types = df.dtypes.tolist()

# Sütun isimleri ve tiplerini eşleştir
column_info = list(zip(column_names, column_types))

# Sütun isimleri ve tiplerini yazdır
for column in column_info:
    print(f"Sütun Adı: {column[0]}, Sütun Tipi: {column[1]}")
