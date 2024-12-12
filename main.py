# Домашнее задание 4 (Вариант 2)
# В парикмахерской работают 3 мастера, а в зале ожидания расположены 3 стула. Поток клиентов имеет интенсивность
# λ = 12 клиентов в 1 ч. Среднее время обслуживания b = 20 мин. Определить относительную и абсолютную пропускную
# способность системы, среднее число занятых кресел, среднюю длину очереди, среднее время, которое клиент проводит
# в парикмахерской.

import numpy as np
import matplotlib.pyplot as plt
from math import factorial

def compute_p0(load_factor, channels, queue_length):
    base_series = sum((load_factor ** i) / factorial(i) for i in range(channels + 1))
    correction = (load_factor ** (channels + 1) * (1 - (load_factor / channels) ** queue_length)) / (factorial(channels) * channels * (1 - load_factor / channels))
    return 1 / (base_series + correction)

def compute_block_probability(load_factor, channels, queue_length, p0):
    return (load_factor ** (channels + queue_length)) * p0 / (channels ** queue_length * factorial(channels))

def compute_average_queue_size(load_factor, channels, queue_length, p0):
    numerator = load_factor ** (channels + 1) * (1 - (load_factor / channels) ** queue_length *
                (queue_length + 1 - (queue_length / channels) * load_factor)) * p0
    denominator = factorial(channels) * channels * (1 - load_factor / channels) ** 2
    return numerator / denominator

# Тут находятся заданные параметры системы
channels, queue_length = 3, 3
arrival_rate, service_rate = 12, 3
load_factor = arrival_rate / service_rate

# Вычисления для системы
p0 = compute_p0(load_factor, channels, queue_length)
block_probability = compute_block_probability(load_factor, channels, queue_length, p0)
throughput_ratio = 1 - block_probability
effective_arrival_rate = arrival_rate * throughput_ratio
avg_busy_channels = effective_arrival_rate / service_rate
avg_queue_size = compute_average_queue_size(load_factor, channels, queue_length, p0)
avg_wait_time = avg_queue_size / arrival_rate
avg_system_size = avg_queue_size + avg_busy_channels
avg_stay_time = avg_system_size / arrival_rate

# Вывод результатов
print(f"\nРезультаты:")
print(f"Вероятность простоя (p0): {p0:.3f}")
print(f"Вероятность отказа (π): {block_probability:.3f}")
print(f"Относительная пропускная способность (Q): {throughput_ratio:.3f}")
print(f"Абсолютная пропускная способность (λ'): {effective_arrival_rate:.2f}")
print(f"Среднее число занятых каналов (k_зан): {avg_busy_channels:.2f}")
print(f"Среднее число заявок в очереди (L): {avg_queue_size:.2f}")
print(f"Среднее время ожидания (W): {avg_wait_time:.2f}")
print(f"Среднее число заявок в системе (M): {avg_system_size:.2f}")
print(f"Среднее время пребывания заявки (U): {avg_stay_time:.2f}\n")

# Построение графиков
lambda_range, mu_range = np.linspace(0.1, 10, 50), np.linspace(0.1, 10, 50)
arrival_rate_grid, service_rate_grid = np.meshgrid(lambda_range, mu_range)
load_factor_grid = arrival_rate_grid / service_rate_grid

p0_grid = compute_p0(load_factor_grid, channels, queue_length)
block_probability_grid = compute_block_probability(load_factor_grid, channels, queue_length, p0_grid)
throughput_ratio_grid = 1 - block_probability_grid
effective_arrival_rate_grid = arrival_rate_grid * throughput_ratio_grid
avg_busy_channels_grid = effective_arrival_rate_grid / service_rate_grid
avg_queue_size_grid = compute_average_queue_size(load_factor_grid, channels, queue_length, p0_grid)
avg_wait_time_grid = avg_queue_size_grid / arrival_rate_grid
avg_system_size_grid = avg_queue_size_grid + avg_busy_channels_grid
avg_stay_time_grid = avg_system_size_grid / arrival_rate_grid

data_mapping = {
    "Вероятность простоя (p0)": p0_grid,
    "Вероятность отказа (π)": block_probability_grid,
    "Относительная пропускная способность (Q)": throughput_ratio_grid,
    "Абсолютная пропускная способность (λ')": effective_arrival_rate_grid,
    "Среднее число занятых каналов (k_зан)": avg_busy_channels_grid,
    "Среднее число заявок в очереди (L)": avg_queue_size_grid,
    "Среднее время ожидания (W)": avg_wait_time_grid,
    "Среднее число заявок в системе (M)": avg_system_size_grid,
    "Среднее время пребывания заявки (U)": avg_stay_time_grid
}

for title, data in data_mapping.items():
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(arrival_rate_grid, service_rate_grid, data, cmap='viridis')
    ax.set_title(title)
    ax.set_xlabel('Интенсивность потока (λ)')
    ax.set_ylabel('Интенсивность обслуживания (μ)')
    ax.set_zlabel(title)
    plt.show()
