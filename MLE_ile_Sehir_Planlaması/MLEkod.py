# ==========================================
# 2025–2026 Bahar Dönemi
# YZM212 Makine Öğrenmesi Dersi - 2. Laboratuvar Ödevi
# Konu: Maximum Likelihood Estimation (MLE) ile Akıllı Şehir Planlaması
# ==========================================

import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
from scipy.stats import poisson

# -----------------------------
# Bölüm 2: Negatif Log-Likelihood Fonksiyonu
# -----------------------------

# Gözlemlenen Trafik Verisi (1 dakikada geçen araç sayısı)
traffic_data = np.array([12, 15, 10, 8, 14, 11, 13, 16, 9, 12, 11, 14, 10, 15])

def negative_log_likelihood(lam, data):
    """
    Poisson dağılımı için Negatif Log-Likelihood hesaplar.
    log(k!) terimi optimizasyon açısından sabittir, bu yüzden ihmal edilir.
    """
    lam = lam[0]  # scipy.optimize minimize fonksiyonu parametreyi array olarak geçirir
    # L(λ) = Π e^-λ * λ^k / k!
    # log L(λ) = Σ ( k*log(λ) - λ - log(k!) )
    nll = -np.sum(data * np.log(lam) - lam)  # -log(Lambda) → minimize ediyoruz
    return nll

# -----------------------------
# Bölüm 2: Sayısal MLE Hesabı
# -----------------------------

initial_guess = [1.0]

result = opt.minimize(
    negative_log_likelihood,
    initial_guess,
    args=(traffic_data,),
    bounds=[(0.001, None)]
)

lambda_mle_numerical = result.x[0]
lambda_mle_analytic = np.mean(traffic_data)

print(f"Sayısal Tahmin (MLE λ): {lambda_mle_numerical:.4f}")
print(f"Analitik Tahmin (Ortalama λ): {lambda_mle_analytic:.4f}")

# -----------------------------
# Bölüm 3: Model Görselleştirme
# -----------------------------

# PMF (Poisson dağılımı) ve Histogram
k_values = np.arange(min(traffic_data), max(traffic_data) + 1)
pmf_values = poisson.pmf(k_values, mu=lambda_mle_numerical)

plt.figure(figsize=(8,5))
plt.hist(traffic_data, bins=np.arange(8, 18)-0.5, density=True, alpha=0.6, color='skyblue', label='Gerçek Veri')
plt.plot(k_values, pmf_values, 'o-', color='crimson', label=f'Poisson PMF (λ={lambda_mle_numerical:.2f})')

plt.title("Poisson Dağılımı ile Trafik Yoğunluğu Modeli")
plt.xlabel("Bir Dakikada Geçen Araç Sayısı (k)")
plt.ylabel("Olasılık Yoğunluğu")
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# -----------------------------
# Bölüm 4: Outlier (Aykırı Değer) Analizi
# -----------------------------

# Outlier içeren veri
traffic_data_outlier = np.append(traffic_data, 200)
lambda_outlier = np.mean(traffic_data_outlier)

print("\n--- Outlier Analizi ---")
print(f"Orijinal λ: {lambda_mle_analytic:.2f}")
print(f"Outlier (200 araç) eklenmiş veri λ: {lambda_outlier:.2f}")

plt.figure(figsize=(8,5))
plt.bar(['Orijinal Veri', 'Outlier Eklenmiş Veri'], [lambda_mle_analytic, lambda_outlier],
        color=['green', 'red'])
plt.ylabel("λ (ortalama araç sayısı)")
plt.title("Aykırı Değerin MLE Parametresine Etkisi")
plt.show()

# -----------------------------
# Yorum:
# -----------------------------
# Outlier (200) eklendiğinde ortalama λ değeri aşırı artar.
# MLE, Poisson dağılımında λ = veri ortalaması olduğundan,
# tek bir hatalı gözlem bile trafik yoğunluğu tahminini ciddi biçimde bozar.
# Bu durumda belediye, gerçekte gerekmediği halde yol genişletme veya altyapı yatırımı kararı alabilir.
