# Bibliotecas utilizadas
import pandas as pd
import vector
import numpy as np
import matplotlib.pyplot as plt
import math
import csv
from scipy.optimize import curve_fit
import os

import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator

# Arquivo csv contendo as informações de cada partícula (4 leptons)
pasta_csv = r"C:\Users\venut\Desktop\CSV"
# Lista para armazenar os caminhos completos de todos os arquivos CSV na pasta
arquivos_csv = []
# envia os arquivos da pasta para a lista criada
for arquivo in os.listdir(pasta_csv):
    arquivos_csv.append(os.path.join(pasta_csv, arquivo))
# junta os arquivos em 1 só
df = pd.concat((pd.read_csv(file_path) for file_path in arquivos_csv), axis=0)


# Definição da função que faz as condições de combinação e encontra a massa invariante de Z1
def compute_mass1(row):
    v1 = vector.obj(px=row['px1'], py=row['py1'], pz=row['pz1'], E=row['E1'])
    v2 = vector.obj(px=row['px2'], py=row['py2'], pz=row['pz2'], E=row['E2'])
    v3 = vector.obj(px=row['px3'], py=row['py3'], pz=row['pz3'], E=row['E3'])
    v4 = vector.obj(px=row['px4'], py=row['py4'], pz=row['pz4'], E=row['E4'])
    ideal = row['mZ1']
    a = abs(ideal - (v1 + v2).mass)
    b = abs(ideal - (v1 + v3).mass)
    c = abs(ideal - (v1 + v4).mass)
    lista1 = [a, b]
    lista2 = [a, c]
    lista3 = [b, c]
    menor1 = min(lista1)
    menor2 = min(lista2)
    menor3 = min(lista3)

    if abs(row['PID1']) == abs(row['PID3']) and abs(row['PID1']) == abs(row['PID4']) and row['Q1'] == row['Q2']:
        if b == menor3 and (v1 + v3).mass < 110:
            return (v1 + v3).mass
        else:
            return (v1 + v4).mass

    if abs(row['PID1']) == abs(row['PID2']) and abs(row['PID1']) == abs(row['PID3']) and row['Q1'] != row['Q2'] and row['Q1'] == row['Q4']:
        if a == menor1 and (v1 + v2).mass < 110:
            return (v1 + v2).mass
        else:
            return (v1 + v3).mass

    if abs(row['PID1']) == abs(row['PID2']) and abs(row['PID1']) == abs(row['PID4']) and row['Q1'] != row['Q2'] and row['Q1'] == row['Q3']:
        if a == menor2 and (v1 + v2).mass < 110:
            return (v1 + v2).mass
        else:
            return (v1 + v4).mass

    if row['Q1'] != row['Q2'] and abs(row['PID1']) == abs(row['PID2']) and abs(row['PID1']) != abs(row['PID3']):
        return (v1 + v2).mass


df['massa1'] = df.apply(compute_mass1, axis=1)

# Definição da função que faz as condições de combinação e encontra a massa invariante de Z2
def compute_mass2(row):
    v1 = vector.obj(px=row['px1'], py=row['py1'], pz=row['pz1'], E=row['E1'])
    v2 = vector.obj(px=row['px2'], py=row['py2'], pz=row['pz2'], E=row['E2'])
    v3 = vector.obj(px=row['px3'], py=row['py3'], pz=row['pz3'], E=row['E3'])
    v4 = vector.obj(px=row['px4'], py=row['py4'], pz=row['pz4'], E=row['E4'])
    ideal = row['mZ2']
    a = abs(ideal - (v3 + v4).mass)
    b = abs(ideal - (v2 + v3).mass)
    c = abs(ideal - (v2 + v4).mass)
    lista1 = [a, b]
    lista2 = [a, c]
    lista3 = [b, c]
    menor1 = min(lista1)
    menor2 = min(lista2)
    menor3 = min(lista3)

    if abs(row['PID3']) == abs(row['PID4']) and abs(row['PID3']) == abs(row['PID2']) and row['Q3'] == row['Q4']:
        if b == menor3 and (v3 + v2).mass < 110:
            return (v3 + v2).mass
        else:
            return (v4 + v2).mass

    if abs(row['PID3']) == abs(row['PID4']) and abs(row['PID4']) == abs(row['PID2']) and row['Q3'] != row['Q4'] and row['Q3'] == row['Q2']:
        if a == menor2 and (v3 + v4).mass < 110:
            return (v3 + v4).mass
        else:
            return (v4 + v2).mass

    if abs(row['PID3']) == abs(row['PID4']) and abs(row['PID3']) == abs(row['PID2']) and row['Q3'] != row['Q4'] and row['Q4'] == row['Q2']:
        if a == menor1 and (v3 + v4).mass < 110:
            return (v3 + v4).mass
        else:
            return (v3 + v2).mass

    if row['Q3'] != row['Q4'] and abs(row['PID3']) == abs(row['PID4']) and abs(row['PID3']) != abs(row['PID2']):
        return (v3 + v4).mass


df['massa2'] = df.apply(compute_mass2, axis=1)

# passando os dados obtidos para um array para fazer o plot dos dados
x1data = np.array(df['massa1'])
x2data = np.array(df['massa2'])
x3data = np.hstack((x1data, x2data))
x4data = np.array(df['mZ1'])
x5data = np.array(df['mZ2'])
x6data = np.hstack((x4data, x5data))

hist,bins=np.histogram(x6data,bins=38)
x1= (bins[:-1] + bins[1:]) / 2 
y=histhist,bins=np.histogram(x6data,bins=38)

x1= (bins[:-1] + bins[1:]) / 2 
y=hist


def gaussian(x, A, mu, sigma):
    return A * np.exp(-((x - mu)**2 )/ (2 * sigma**2))
# Ajuste de gaussiana
params, covariance = curve_fit(gaussian, x1, y, p0=[max(y), np.mean(x1), np.std(x1)])  # Chute inicial p0=[A, mu, sigma]
A_fit, mu_fit, sigma_fit = params

x_fit1 = np.linspace(90.332005,100, 500)  # Aumente o número de pontos
#                      amplitude, centro, abertura
y_fit1 = gaussian(x_fit1, 1.1*A_fit, mu_fit, sigma_fit)



def exponential_func(x, a, b, c):
    return a * np.exp(b * (x - 80)) + c

# Filtrar os dados para o intervalo de 80 a 90
mask = (x1 >= 80) & (x1 <= 88)
x_filtered = x1[mask]
y_filtered = y[mask]

# Realizar o ajuste da função exponencial
params, covariance = curve_fit(exponential_func, x_filtered, y_filtered)

# Parâmetros ajustados
a, b, c = params

# Gerar pontos para a curva ajustada
x_fit2 = np.linspace(80, 87.65, 500)
y_fit2 = exponential_func(x_fit2, a, b, c)



def exponential_func2(x, a, b, c):
    return a * np.exp(b * (x - 80)) + c
# Filtrar os dados para o intervalo de 80 a 90
mask = (x1 >= 84) & (x1 <= 92)
x_filtered2 = x1[mask]
y_filtered2 = y[mask]
# Realizar o ajuste da função exponencial
params, covariance = curve_fit(exponential_func2, x_filtered2, y_filtered2)
# Parâmetros ajustados
a, b, c = params
# Gerar pontos para a curva ajustada
x_fit3 = np.linspace(87.65, 90.330405, 500)
y_fit3 = exponential_func2(x_fit3, a, b, c)





plt.figure(figsize=(8,8))
plt.scatter(x1, hist, label='Dados',color='blue',marker='+', s=150)
plt.plot(x_fit1, y_fit1, color='red', label='Curva Gaussiana ajustada')
plt.plot(x_fit2, y_fit2, color='red', label='Curva exponencial ajustada')
plt.plot(x_fit3, y_fit3, color='red', label='Curva exponencial ajustada 2')
plt.xlim(80,100)


plt.show()