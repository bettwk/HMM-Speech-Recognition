import numpy as np
import matplotlib.pyplot as plt
import emcee
import corner

true_mu=150.0
true_sigma=10.0
n_obs=50

np.random.seed(42)
data = true_mu + true_sigma * np.random.randn(n_obs)

def log_likelihood(theta, data):
    mu, sigma= theta
    if sigma<=0 : return -np.inf
    return -0.5 * np.sum (((data - mu) / sigma)**2 + np.log(2*np.pi*sigma**2))

def log_prior(theta):
    mu, sigma= theta
    if 0<mu<300 and 0<sigma<50:
      return 0.0
    return -np.inf

def log_probability(theta, data):
    lp= log_prior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta, data)



initial = [140, 5]
n_walkers=32
pos=initial + 1e-4 * np.random.randn(n_walkers, 2)

sampler = emcee.EnsembleSampler(n_walkers, 2, log_probability, args=(data,))
sampler.run_mcmc(pos, 2000, progress=True)

flat_samples = sampler.get_chain(discard=500, thin=15, flat=True)


fig = corner.corner(
    flat_samples, labels=["$\mu$ (Parlaklık)", "$\sigma$ (Hata)"],
    truths= [true_mu, true_sigma]
)

labels = ["mu (Parlaklik)", "sigma (Hata Payi)"]

for i in range(2):
    mcmc = np.percentile(flat_samples[:, i], [16, 50, 84])
    median = mcmc[1]
    alt_sinir = mcmc[0]
    ust_sinir = mcmc[2]
    
    print(f"{labels[i]}:")
    print(f"  Median      : {median:.3f}")
    print(f"  Alt Sinir   : {alt_sinir:.3f}")
    print(f"  Ust Sinir   : {ust_sinir:.3f}")
    print("-" * 30)



plt.show()