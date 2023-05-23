import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense

# Входные данные
c = np.array([-40, -10, 0, 8, 15, 22, 38])
f = np.array([-40, 14, 32, 46, 59, 72, 100])

# Создание модели
model = Sequential()
model.add(Dense(1, input_shape=(1,)))  # Один входной слой с одним нейроном

# Компиляция модели
model.compile(optimizer=tf.keras.optimizers.Adam(0.1), loss='mean_squared_error')  # Оптимизатор: стохастический градиентный спуск, функция потерь: среднеквадратичная ошибка (MSE)

# Обучение модели
model.fit(c, f, epochs=500, verbose=0)  # Обучение на данных c и f в течение 1000 эпох

# Прогнозирование
c_new = np.array([30, 50, 70])  # Новые значения для прогноза
f_pred = model.predict(c_new)  # Прогнозирование значений f на основе c_new

print(f_pred)
