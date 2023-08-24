# GTD-terrors-mapping

- Bu proje tamamen eğitim amaçlıdır ve yaşanan terör olaylarıyla ilgili bir bağıntı bulunmamaktadır. Bu projede kullanılan veriler yasal olarak bir suç teşkil etmemesi adına 2013 yılına kadar sınırlandırılmıştır. Orjinal verilere internet üzerinden rahatlıkla erişilebilmektedir.

### Dikkat Edilmesi ve Yapılması Gerekenler :

- data klasörü içerisinde bulunan dataset.md, kullanmakta olduğumuz GTD verisindeki sütunların isimlerini ve anlamlarını açıklamaktadır.
- data klasörü içerisinde bulunan "event..." ile başlayan veri, uygulama içerisindeki çekilen veriyi göstermektedir.
- 'example_data.csv' verisi örnek bir veri teşkil etmektedir, bir gerçekliği olmamaktadır. 

- 'gui_app.py' içerisinde bulunan 'csv_path' değişkenlerine gerekli dosya yollarını doğru bir şekilde girdiğinizden emin olunuz.
- Bu proje içerisinde bulunan Folium kütüphanesi Ubuntu üzerinde xorg ile uyumsuz çalışmaktadır. (Windows üzerinde başarılı bir şekilde çalıştırabilirsiniz.)
- 'gui' klasöründe içerisinde bulunan postgres klasöründeki 'csvtopostgres.py', '.csv' halinde bulunan veriyi postgresql veritabanına aktarmanıza olanak sağlar. Ayrıca içerisinde bulunan df değişkenine verilen dosya yolu doğu bir şekilde girilmelidir.  
- Aynı klasör içerisinde yer alan 'postgrestocsv.py' ise postgresql veritabanına aktarmış olduğumuz veriyi '.csv' dosya türüne çekmemizi sağlar. Burada da 'output_file' değişkenine verilen dosya yoluna dikkat edilmelidir.
- Veritabanı ile uygulama arasındaki bağlantısının başarılı olması için postgres_info.py dosyasında bulunan değişkenlere gerekli bilgiler girilmelidir.

- notebooks klasörü içerisinde ise verilerle ilgili analizler yapılmıştır ve tamamen eğitim amaçlıdır.

