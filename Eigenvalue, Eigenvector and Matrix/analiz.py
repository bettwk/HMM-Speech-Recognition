import numpy as np

# 1. REFERANS ALINAN MANTIĞIN YENİDEN UYGULANMASI (Polinom Aritmetiği)

def poly_add(p1, p2, sub=1):
    """İki polinomu toplar veya çıkarır. 
    İndeks i, x^i'nin katsayısını temsil eder."""
    max_len = max(len(p1), len(p2))
    res = [0] * max_len
    for i in range(max_len):
        val1 = p1[i] if i < len(p1) else 0
        val2 = p2[i] if i < len(p2) else 0
        res[i] = val1 + (sub * val2)
    return res

def poly_mul(p1, p2):
    """İki polinomu çarpar."""
    if not p1 or not p2:
        return []
    res = [0] * (len(p1) + len(p2) - 1)
    for i in range(len(p1)):
        for j in range(len(p2)):
            res[i+j] += p1[i] * p2[j]
    return res

def get_minor(matrix, row, col):
    """Matrisin belirtilen satır ve sütunu çıkarılarak minörünü oluşturur."""
    return [[matrix[i][j] for j in range(len(matrix[0])) if j != col] 
            for i in range(len(matrix)) if i != row]

def determinant_poly(matrix):
    """Elemanları polinom olan bir matrisin determinantını özyineli (recursive) olarak hesaplar."""
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        # 2x2 matris için: (a*d) - (b*c)
        ad = poly_mul(matrix[0][0], matrix[1][1])
        bc = poly_mul(matrix[0][1], matrix[1][0])
        return poly_add(ad, bc, sub=-1)
    
    det = [0]
    for c in range(n):
        minor = get_minor(matrix, 0, c)
        minor_det = determinant_poly(minor)
        term = poly_mul(matrix[0][c], minor_det)
        
        # Kofaktör işareti (+, -, +, - ...)
        if c % 2 == 1:
            det = poly_add(det, term, sub=-1)
        else:
            det = poly_add(det, term, sub=1)
    return det

def custom_find_eigenvalues(matrix):
    """A - lambda*I işlemini uygulayarak karakteristik denklemi çıkarır ve özdeğerleri bulur."""
    n = len(matrix)
    # A - lambda*I matrisini oluştur
    # Her eleman bir polinom listesi olacak: [sabit_terim, lambda_katsayısı]
    poly_matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append([matrix[i][j], -1.0])  # Köşegen: A[i][i] - 1.0 * lambda
            else:
                row.append([matrix[i][j]])        # Diğer: A[i][j] + 0 * lambda
        poly_matrix.append(row)
    
    # Karakteristik polinomu hesapla
    char_eq = determinant_poly(poly_matrix)
    
    # np.roots katsayıları en yüksek dereceden en düşüğe doğru beklediği için listeyi ters çeviriyoruz ([::-1])
    roots = np.roots(char_eq[::-1])
    return roots


# 2. AYNI MATRİS ÜZERİNDE SONUÇLARIN KARŞILAŞTIRILMASI

if __name__ == "__main__":
    # Repoda kullanılan test matrisi
    A = [[6, 1, -1],
         [0, 7,  0],
         [3, -1, 2]]
    
    # Kendi implementasyonumuzla sonuç (np.linalg.eig KULLANILMADAN)
    custom_eigenvalues = custom_find_eigenvalues(A)
    
    # Numpy'ın hazır fonksiyonu ile sonuç
    numpy_eigenvalues, numpy_eigenvectors = np.linalg.eig(A)
    
    print("="*50)
    print("Özel Fonksiyon Sonucu (Custom):")
    print(np.sort(custom_eigenvalues)) # Sıralayarak gösterelim ki kıyaslaması kolay olsun
    
    print("\nNumpy 'eig' Fonksiyonu Sonucu:")
    print(np.sort(numpy_eigenvalues))
    print("="*50)