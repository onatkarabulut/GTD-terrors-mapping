import pandas as pd
from translate import Translator
import folium
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QInputDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import psycopg2
from postgres import postgres_info as psg_info

csv_path = "data\\globalterrorismdb_0718dist.csv"

class pandas_points():
    @staticmethod
    def get_location(latitude, longitude):
        return {'latitude': latitude, 'longitude': longitude}

def map_creator():
    # csv_path = 'data\\globalterrorismdb_0718dist.csv'
    data_terrors = pd.read_csv(csv_path, encoding='ISO-8859-1', low_memory=False)
    terrors = data_terrors[data_terrors["iyear"] <= 2013]

    latest_attacks = terrors.groupby('gname').agg({'iyear': 'max', 'imonth': 'max', 'iday': 'max', 'latitude': 'max', 'longitude': 'max', 'nkill': 'sum', 'nwound': 'sum', 'targtype1_txt': 'max', 'weaptype1': 'max','eventid':'max'})
    latest_attacks.columns = ['year', 'month', 'day', 'latitude', 'longitude', 'nkill', 'nwound', 'targtype1_txt', 'weaptype1','eventid']
    latest_attacks.reset_index(inplace=True)

    latest_attacks['location'] = latest_attacks.apply(lambda row: pandas_points.get_location(row['latitude'], row['longitude']), axis=1)
    latest_attacks[['latitude', 'longitude']] = latest_attacks['location'].apply(pd.Series)
    latest_attacks_pd = latest_attacks[['gname', 'latitude', 'longitude', 'year', 'targtype1_txt', 'weaptype1', 'nkill', 'nwound','eventid']].copy()

    terrorist_locations_3d = pd.DataFrame(columns=['gname', 'latitude', 'longitude', 'year', 'nkill', 'nwound','eventid'])
    for _, row in latest_attacks_pd.iterrows():
        gname = row['gname']
        latitude = row['latitude']
        longitude = row['longitude']
        year = row['year']
        targtype1_txt = row['targtype1_txt']
        nkill = row['nkill']
        nwound = row['nwound']
        eventid = row['eventid']
        summary = f"EventID: {eventid}<br><br>Örgüt: {gname}<br>Yıl: {year}<br>Hedef: {targtype1_txt}<br>Ölü Sayısı: {nkill}<br>Yaralı Sayısı: {nwound}"

        terrorist_locations_3d = terrorist_locations_3d._append({'gname': gname, 'latitude': latitude, 'longitude': longitude, 'year': year, 'targtype1_txt': targtype1_txt, 'nkill': nkill, 'nwound': nwound, 'summary': summary, 'eventid': eventid}, ignore_index=True) #type: ignore

    m = folium.Map(location=[latitude, longitude], zoom_start=0) #type:ignore

    for _, location in terrorist_locations_3d.iterrows():
        latitude = location['latitude']
        longitude = location['longitude']
        gname = location['gname']
        year = location['year']
        targtype1_txt = location['targtype1_txt']
        nkill = location['nkill']
        nwound = location['nwound']
        summary = location['summary']
        eventid = location['eventid']
        if pd.notna(latitude) and pd.notna(longitude):  # NaN değerleri için uygulanan bir işlem
            tooltip_text = f"{summary}"
            folium.CircleMarker(
                location=[latitude, longitude],
                radius=10,
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.4,
                tooltip=tooltip_text
            ).add_to(m)

    map_file_path = '\\map.html'
    m.save(map_file_path)
    return map_file_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Terrorist Attacks Map")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)

        self.webview = QWebEngineView(self)
        main_layout.addWidget(self.webview)

        map_button = QPushButton("Haritayı Yenile", self)
        map_button.clicked.connect(self.show_map)
        main_layout.addWidget(map_button)

        button_frame = QHBoxLayout()  # rectangle2 için yeni bir QHBoxLayout oluşturuldu

        button1 = QPushButton("Veri Gir", self)
        button1.clicked.connect(self.button1_clicked)
        button_frame.addWidget(button1)

        button2 = QPushButton("Detaylı Veri", self)
        button2.clicked.connect(self.button2_clicked)
        button_frame.addWidget(button2)

        button3 = QPushButton("Veriyi Çek", self)
        button3.clicked.connect(self.button3_clicked)
        button_frame.addWidget(button3)

        main_layout.addLayout(button_frame)  # button_frame düzenlemesi ana layouta eklendi

    def button1_clicked(self):
        # QMessageBox.information(self, "Pop-up", "Button 1'e tıklandı!")

        inputs = [
            ('Örgütü girin:', str),
            ('Enlemi girin:', float),
            ('Boylamı girin:', float),
            ('Yılı girin:', int),
            ('Hedefi girin:', str),
            ('Ölü sayısını girin:', int),
            ('Yaralı sayısını girin:', int)
        ]

        data = {}
        for prompt, data_type in inputs:
            value, ok = QInputDialog.getText(self, 'Veri Girişi', prompt)
            if not ok:
                return
            try:
                data[prompt] = data_type(value)
            except ValueError:
                QMessageBox.warning(self, 'Pop-up', f'Hatalı veri girişi: {value}')
                return

        terrors = pd.read_csv('data\\copy.csv')
        eventid = terrors['eventid'].max() + 1 if 'eventid' in terrors else 1
        new_row = {'gname': data['Örgütü girin:'], 'latitude': data['Enlemi girin:'], 'longitude': data['Boylamı girin:'],
                'year': data['Yılı girin:'], 'targtype1_txt': data['Hedefi girin:'], 'nkill': data['Ölü sayısını girin:'],
                'nwound': data['Yaralı sayısını girin:'], 'eventid': eventid}
        terrors = terrors._append(new_row, ignore_index=True) # type: ignore
        terrors.to_csv('data\\copy.csv', index=False)

        
    def button2_clicked(self):
        # QMessageBox.information(self, "Pop-up", "Button 2'ye tıklandı!")
        
        csv_path = 'data\\globalterrorismdb_0718dist.csv'
        data_terrors = pd.read_csv(csv_path, low_memory=False)
        terrors = data_terrors[data_terrors['iyear'] <= 2013]
        
        eventids = terrors['eventid'].astype(str).tolist()  # Event ID'leri dizeye dönüştürerek bir liste oluşturun
        
        item, ok = QInputDialog.getItem(self, 'Detaylı Veri', 'Event ID\'yi girin:', eventids, editable=False)
        
        if ok:
            eventid = int(item)  # Seçilen öğeyi tam sayıya dönüştürün
            
            event = terrors[terrors['eventid'] == eventid]

            if not event.empty:
                country = event['country_txt'].values[0]
                year = event['iyear'].values[0]
                summary = event['summary'].values[0]
                target = event['targtype1_txt'].values[0]
                gname = event['gname'].values[0]
                try:
                    translator = Translator(to_lang='tr')
                    translated_summary = translator.translate(summary)
                except TypeError:
                    translated_summary = ''

                message_box_info = f"""
                Event ID: {eventid}
                Ülke: {country}
                Yıl: {year}
                Açıklama: {translated_summary}
                Hedef: {target}
                Örgüt: {gname}
                """
                QMessageBox.information(self, 'Pop-up', message_box_info)
            else:
                QMessageBox.warning(self, 'Pop-up', 'Event ID not found!')

    def button3_clicked(self):
        # QMessageBox.information(self, "Pop-up", "Button 3'e tıklandı!")
        csv_path = 'data\\globalterrorismdb_0718dist.csv'
        data_terrors = pd.read_csv(csv_path, low_memory=False)
        terrors = data_terrors[data_terrors['iyear'] <= 2013]

        eventids = terrors['eventid'].astype(str).tolist()  # Event ID'leri dizeye dönüştürerek bir liste oluşturun

        selected_eventid, ok = QInputDialog.getItem(self, "Veri Çekme", "Event ID'yi seçin:", eventids, editable=False)
        if not ok:
            return

        eventid = int(selected_eventid)

        # PostgreSQL veritabanına bağlantı
        conn = psycopg2.connect(host= psg_info.host_ip, user=psg_info.user_name,
                            password=psg_info.password,
                            dbname=psg_info.database_name, port=psg_info.host_port)

        # Veritabanı sorgusu
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM terrors WHERE eventid = {eventid}")
        rows = cursor.fetchall()

        if rows:
            # Sorgu sonuçlarını TXT dosyasına yazdırma
            output_file = f"data\\event_{eventid}_summary.txt"
            with open(output_file, 'w') as file:
                for row in rows:
                    eventid, gname, latitude, longitude, year, targtype1_txt, nkill, nwound, *_ = row
                    #eventid,iyear,imonth,iday,approxdate,extended,resolution,country,country_txt,region,region_txt,provstate,city,latitude,longitude,specificity,vicinity,location,summary,crit1,crit2,crit3,doubtterr,alternative,alternative_txt,multiple,success,suicide,attacktype1,attacktype1_txt,attacktype2,attacktype2_txt,attacktype3,attacktype3_txt,targtype1,targtype1_txt,targsubtype1,targsubtype1_txt,corp1,target1,natlty1,natlty1_txt,targtype2,targtype2_txt,targsubtype2,targsubtype2_txt,corp2,target2,natlty2,natlty2_txt,targtype3,targtype3_txt,targsubtype3,targsubtype3_txt,corp3,target3,natlty3,natlty3_txt,gname,gsubname,gname2,gsubname2,gname3,gsubname3,motive,guncertain1,guncertain2,guncertain3,individual,nperps,nperpcap,claimed,claimmode,claimmode_txt,claim2,claimmode2,claimmode2_txt,claim3,claimmode3,claimmode3_txt,compclaim,weaptype1,weaptype1_txt,weapsubtype1,weapsubtype1_txt,weaptype2,weaptype2_txt,weapsubtype2,weapsubtype2_txt,weaptype3,weaptype3_txt,weapsubtype3,weapsubtype3_txt,weaptype4,weaptype4_txt,weapsubtype4,weapsubtype4_txt,weapdetail,nkill,nkillus,nkillter,nwound,nwoundus,nwoundte,property,propextent,propextent_txt,propvalue,propcomment,ishostkid,nhostkid,nhostkidus,nhours,ndays,divert,kidhijcountry,ransom,ransomamt,ransomamtus,ransompaid,ransompaidus,ransomnote,hostkidoutcome,hostkidoutcome_txt,nreleased,addnotes,scite1,scite2,scite3,dbsource,INT_LOG,INT_IDEO,INT_MISC,INT_ANY,related,year,month,day 
                    summary = f"EventID: {eventid}\n\nÖrgüt: {gname}\nYıl: {year}\nHedef: {targtype1_txt}\nÖlü Sayısı: {nkill}\nYaralı Sayısı: {nwound}\nKordinat X: {latitude}\nKordinat Y: {longitude}\n"
                    file.write(summary + "\n\n")

            QMessageBox.information(self, "Pop-up", f"Event ID {eventid} için özet dosyası oluşturuldu: {output_file}")
        else:
            QMessageBox.warning(self, "Pop-up", "Event ID not found!")

        # Veritabanı bağlantısını kapatma
        cursor.close()
        conn.close()





    def show_map(self):
        self.webview.load(QUrl.fromLocalFile(map_creator()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
