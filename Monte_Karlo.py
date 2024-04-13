import numpy as np
import matplotlib.pyplot as plt
N = 1000 # Количество итераций метода Монте-Карло
alpha = 0.05 # Ограничение на вероятность превышения количества заявок
lambda_ = 9.3 # Интенсивность появления заявок
lambda_G = 12.0 # Exponential(12.0) - распределение продолжительности обработки одной заявки

# Генерируем последовательность экспоненциально распр.сл.в.
def generate_(l, size):
    t = 0
    T_k_arr = []
    while t <= size:
        t += np.random.exponential(1/l)
        T_k_arr.append(t)
    return T_k_arr

# Подсчёт пикового количества активных заявок для текущей итерации метода Монте-Карло
def find_Q_i(T_k, gamma):
    Q = []
    T = np.linspace(0, max(T_k), num=100)
    for t in T:
        elem = sum((t >= T_k[j]) and (t <= T_k[j] + gamma[j]) for j in range(len(T_k)))
        Q.append(elem)
    return max(Q)

# Запуска метода Монте-Карло
def All_Q():
    Q = []
    for i in range(N):
        T_k = generate_(lambda_, 8)
        gamma = np.random.exponential(1/lambda_G, size=len(T_k))
        Q.append(find_Q_i(T_k, gamma))
    return Q


Qi = All_Q()
Qi.sort(reverse=True)
# Вычисление вероятностей превышения пикового количества заявок
# для выбранного и всех меньших значений s
# Вычисление минимального s, при котором вероятность не превышает заданного альфа

def find_s(Q):
    s_values = []
    probabilities = []
    s_min = 0
    for s in range(max(Q)+1):
        probability = sum(q > s for q in Q) / N
        probabilities.append(probability)
        s_values.append(s)
        if probability <= alpha:
            s_min = s
            break
    return [s_values, probabilities, s_min]

s_min = find_s(Qi)[2]
s_values = find_s(Qi)[0]
probabilities = find_s(Qi)[1]

#График оценок вероятностей превышения пикового количества заявок
#для выбранного и всех меньших значений s
#plt.figure(figsize=(10, 6))
plt.plot(s_values, probabilities, marker='o', linestyle='-', color='b')
plt.axhline(y=alpha, color='gray', linestyle='--')
plt.axvline(x=s_min, color='g', linestyle='--')
plt.title('График вероятности превышения пикового количества заявок')
plt.xlabel('Количество обслуживающих элементов - s')
plt.ylabel('Вероятность оценки s')
plt.grid(True)
plt.show()

print(f"Минимальное количество обслуживающих элементов s: {s_min}")
