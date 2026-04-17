# YZM212 Makine Öğrenmesi - 4. Laboratuvar Ödevi
## Uzak Bir Galaksinin Parlaklık Analizi (Bayesyen Çıkarım)

Bu proje, astronomi projelerinde altın standart olarak kabul edilen **Bayesian Inference (Bayesyen Çıkarım)** yöntemini kullanarak, gürültülü gözlem verilerinden bir gök cisminin gerçek parlaklığını ve veri setindeki belirsizliği (standart sapma) tahmin etmeyi amaçlamaktadır.

---

### 1. Problem Tanımı
Astronomik gözlemler genellikle kozmik tozlar, atmosferik dalgalanmalar ve teleskop sensörlerindeki ısıl gürültüler nedeniyle yüksek oranda belirsizlik (hata) içerir. Geleneksel (frekansçı) istatistiğin aksine Bayesyen yaklaşım, bu belirsizlikleri yönetmek ve önceki bilgilerimizi (prior) modele dahil etmek için daha esnek bir yapı sunar. Bu çalışmanın temel problemi, sentetik olarak oluşturulmuş ve gürültü eklenmiş gözlem verilerini kullanarak, arka plandaki gerçek fiziksel değerleri (parlaklık ve hata payı) Markov Chain Monte Carlo (MCMC) simülasyonu ile geri elde etmektir.

### 2. Veri
Bu çalışmada dışarıdan bir veri seti kullanılmamış; "evrenin işleyişini" taklit etmek amacıyla Python'un `numpy` kütüphanesi kullanılarak sentetik gözlem verileri üretilmiştir:
* **Gerçek Parlaklık (true_mu):** 150.0 (Gök cisminin saf parlaklığı)
* **Gözlem Hatası (true_sigma):** 10.0 (Sensör/Ortam gürültüsü)
* **Gözlem Sayısı (n_obs):** 50 (Teleskoptan alınan ölçüm sayısı)

### 3. Yöntem
Model parametrelerini tahmin etmek için Bayes Teoremi kullanılmıştır:
$P(\theta|D) = \frac{P(D|\theta)P(\theta)}{P(D)}$

Uygulama aşamasında aşağıdaki adımlar izlenmiştir:
1. **Log-Likelihood:** Verinin modele uygunluğunu ölçen fonksiyon tanımlandı.
2. **Log-Prior:** Parametreler hakkındaki ön bilgilerimiz (örneğin parlaklığın negatif olamayacağı) geniş (non-informative) sınırlar ile belirlendi.
3. **MCMC Örneklemesi:** `emcee` kütüphanesi kullanılarak 32 yürüyüşçü (walker) ile 2000 adımlık bir simülasyon gerçekleştirildi.
4. **Görselleştirme:** Parametrelerin posterior dağılımları ve güven aralıkları `corner` kütüphanesi ile analiz edildi.

### 4. Sonuçlar
MCMC simülasyonu sonucunda elde edilen parametre tahminleri ve %95 güven aralıkları aşağıdaki tabloda özetlenmiştir:

| Değişken | Gerçek Değer | Tahmin Edilen (Median) | Alt Sınır (%16) | Üst Sınır (%84) | Mutlak Hata |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **$\mu$ (Parlaklık)** | 150.0 | 147.786 | 146.426 | 149.072 | %1.476 |
| **$\sigma$ (Hata Payı)**| 10.0 | 9.492 | 8.554 | 10.531 | %5.08 |

*(Not: Eklenen Corner Plot grafiği proje dosyaları içerisinde `[Grafik Dosyasının Adı.pdf/png]` adıyla bulunabilir.)*

### 5. Yorum ve Tartışma

* **Merkezi Eğilim ve Doğruluk (Accuracy):** Verilerdeki %6-7 oranındaki gürültüye rağmen, model gerçek 150.0 değerine [Mutlak Hata Değeriniz] gibi çok düşük bir hata payı ile yaklaşmayı başarmıştır. Bu durum Bayesyen yöntemin gürültü filtreleme konusundaki başarısını kanıtlar.
* **Tahmin Hassasiyeti (Precision):** Tabloda görüldüğü üzere, ortalama parlaklığın ($\mu$) güven aralığı, ölçüm hassasiyetine ($\sigma$) göre daha dardır. İstatistiksel olarak birinci moment olan ortalamayı bulmak, ikinci moment olan varyansı hesaplamaktan daha kesin (precise) sonuçlar verir. 50 adetlik veri kümesi $\mu$ değerini sabitlemek için yeterli olsa da, $\sigma$'yı kusursuz tahmin etmek için nispeten küçük kalmıştır.
* **Olasılıksal Korelasyon:** Corner Plot üzerindeki elipsin dik/yatay hizalanması, $\mu$ ve $\sigma$ parametreleri arasında olasılıksal bir bağımlılık (korelasyon) olmadığını, MCMC algoritmasının bu iki fiziksel özelliği birbirinden bağımsız olarak optimize ettiğini göstermektedir.
* **Prior ve Veri Sayısı Etkisi:** * Eğer parlaklık için 100-110 gibi çok dar ve yanlış bir prior seçilseydi, Likelihood (veri) 150'yi işaret etse bile model 110 sınırına takılacak ve yanlış sonuç verecekti. Bu, "Prior Bias" riskini gösterir.
  * Veri sayısı (n_obs) 5'e düşürüldüğünde ise posterior dağılımı ciddi şekilde genişlemiş ve belirsizlik (hata payı) artmıştır.

### 6. Kullanılan Teknolojiler
* Python 3.x
* NumPy (Matematiksel işlemler ve veri üretimi)
* Matplotlib (Grafiksel çizimler)
* emcee (MCMC simülasyonu)
* corner (Posterior dağılım analizi)