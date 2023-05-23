import tensorflow as tf

# Определение архитектуры модели
model = tf.keras.Sequential()
model.add(tf.keras.layers.LSTM(units=64, input_shape=(timesteps, input_dim)))  # LSTM слой
model.add(tf.keras.layers.Dense(units=num_classes, activation='softmax'))  # Выходной слой с softmax активацией

# Компиляция модели
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Преобразование меток в one-hot encoding
y_train_encoded = tf.keras.utils.to_categorical(y_train, num_classes)
y_val_encoded = tf.keras.utils.to_categorical(y_val, num_classes)

# Обучение модели
model.fit(X_train, y_train_encoded, epochs=num_epochs, batch_size=batch_size, validation_data=(X_val, y_val_encoded))

# Оценка модели
y_test_encoded = tf.keras.utils.to_categorical(y_test, num_classes)
loss, accuracy = model.evaluate(X_test, y_test_encoded)

# Использование модели для предсказаний
predictions = model.predict(X_test)
