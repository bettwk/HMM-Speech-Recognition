from hmmlearn import hmm
import numpy as np


model_ev = hmm.MultinomialHMM(n_components=2, n_trials=1, n_iter=100, init_params="")


model_ev.startprob_ = np.array([1.0, 0.0])


model_ev.transmat_ = np.array([
    [0.6, 0.4],   
    [0.2, 0.8]   
])


model_ev.emissionprob_ = np.array([
    [0.7, 0.3],  
    [0.1, 0.9]   
])

ev_egitim = np.array([
    [1, 0], [0, 1],          
    [1, 0], [0, 1],          
    [1, 0], [1, 0], [0, 1],  
    [1, 0], [0, 1], [0, 1]  
])
ev_egitim_uzunluk = [2, 2, 3, 3]


model_ev.fit(ev_egitim, ev_egitim_uzunluk)


model_okul = hmm.MultinomialHMM(n_components=4, n_trials=1, n_iter=100, init_params="")

model_okul.startprob_ = np.array([1.0, 0.0, 0.0, 0.0])


model_okul.transmat_ = np.array([
    [0.7, 0.3, 0.0, 0.0],   
    [0.0, 0.6, 0.4, 0.0],  
    [0.0, 0.0, 0.5, 0.5],   
    [0.0, 0.0, 0.0, 1.0]   
])


model_okul.emissionprob_ = np.array([
    [0.9, 0.1],  
    [0.4, 0.6],   
    [0.8, 0.2],  
    [0.1, 0.9]   
])


okul_egitim = np.array([
    [1, 0], [0, 1], [1, 0], [0, 1],         
    [1, 0], [0, 1], [1, 0], [0, 1],         
    [1, 0], [1, 0], [0, 1], [1, 0], [0, 1], 
    [1, 0], [0, 1], [1, 0], [0, 1], [0, 1]
])
okul_egitim_uzunluk = [4, 4, 5, 5]


model_okul.fit(okul_egitim, okul_egitim_uzunluk)


kelime_modelleri = {
    "EV"  : model_ev,
    "OKUL": model_okul
}


test_data = np.array([[1, 0], [0, 1], [0, 1]])  
en_yuksek_skor       = float("-inf")
tahmin_edilen_kelime = ""

print("Skorlar Hesaplanıyor...\n" + "-" * 25)

for kelime_adi, model in kelime_modelleri.items():
    
    skor = model.score(test_data)
    print(f"{kelime_adi} modeli skoru: {skor:.4f}")

   
    if skor > en_yuksek_skor:
        en_yuksek_skor       = skor
        tahmin_edilen_kelime = kelime_adi

print("-" * 25)
print(f"\nSonuç: Duyulan kelime → '{tahmin_edilen_kelime}'")