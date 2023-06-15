import pandas as pd
import psycopg2
from postgres import postgres_info as psg_info

# Veritabanına bağlan
database_name = psg_info.database_name
user_name = psg_info.user_name
password = psg_info.password
host_ip = psg_info.host_ip  
host_port = psg_info.host_port 


# PostgreSQL bağlantısı oluştur
conn = psycopg2.connect(host=host_ip, port=host_port, dbname=database_name, user=user_name, password=password)

# Veriyi sorgula
query = "SELECT * FROM terrors;"  # terrors tablosundaki tüm verileri al
df = pd.read_sql(query, conn)

# CSV dosyasına yaz
output_file = "data\\terrors_export.csv"
df.to_csv(output_file, index=False)

# PostgreSQL bağlantısını kapat
conn.close()

print(f"Veri PostgreSQL'den CSV'ye yazıldı: {output_file}")
