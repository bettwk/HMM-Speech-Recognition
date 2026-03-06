Hidden Markov Model (HMM) ile Kelime Tanıma
Bu proje, belirli ses özelliklerini (High/Low) temsil eden gözlem dizilerini kullanarak kelimeleri ayırt edebilen bir sınıflandırma sistemidir. Projede MultinomialHMM kullanılarak olasılıksal modeller oluşturulmuştur.

Proje Mantığı
Sistem, her kelime için ayrı bir HMM modeli oluşturur. Test aşamasında, yeni bir veri dizisi (test verisi) her iki modele de sunulur. Hangi model bu dizinin oluşma olasılığı için daha yüksek bir log-likelihood (log-olabilirlik) skoru verirse, sistem o kelimeyi tahmin olarak seçer.

Model Yapılandırması
EV Modeli: 2 gizli durumdan oluşur (Örn: /e/ ve /v/ sesleri).

OKUL Modeli: 4 gizli durumdan oluşur (Örn: /o/, /k/, /u/, /l/ sesleri).

Gözlemler: Veriler iki kategoriden oluşur:

[1, 0]: Yüksek frekanslı (High) ses sinyali.

[0, 1]: Düşük frekanslı (Low) ses sinyali.

Teknik Detaylar
1. Durum Geçiş Matrisleri (Transition Matrix)
Modeller, bir ses biriminden diğerine geçme olasılığını tanımlayan transmat_ matrislerine sahiptir. Örneğin, "EV" modelinde /e/ sesinden /v/ sesine geçiş olasılığı 0.4 olarak tanımlanmıştır.

2. Emisyon Olasılıkları (Emission Probability)
Her gizli durumun hangi gözlemi (High/Low) üretme olasılığı olduğunu belirler. emissionprob_ matrisi ile tanımlanır.

3. Eğitim (Fitting)
Modeller, fit metodu kullanılarak sağlanan eğitim dizileri ve uzunlukları (lengths) ile optimize edilir. Bu aşamada Baum-Welch algoritması benzeri bir mantıkla model parametreleri güncellenir.

Kurulum ve Çalıştırma
Gereksinimler
Projenin çalışması için Python ve aşağıdaki kütüphanelerin yüklü olması gerekir:

numpy

hmmlearn

Yüklemek için:

Bash
pip install numpy hmmlearn
Kullanım
Kodu çalıştırdığınızda sistem şu adımları izler:

"EV" ve "OKUL" modellerini parametrelerle ilklendirir.

Sağlanan eğitim verileriyle modelleri eğitir.

test_data değişkenindeki veriyi her iki modelde test eder.

Skorları karşılaştırarak en yüksek olasılığa sahip kelimeyi ekrana yazdırır.

Örnek Çıktı Analizi
Test verisi [[1, 0], [0, 1], [0, 1]] (High, Low, Low) olarak verildiğinde:

EV Modeli Skoru: Bu dizinin "EV" kelimesine ait olma olasılığının logaritması.

OKUL Modeli Skoru: Bu dizinin "OKUL" kelimesine ait olma olasılığının logaritması.

Sonuç: Skoru -0.0'a daha yakın (daha büyük) olan kelime kazanan olarak belirlenir.