<div align="center">
  <h1>🧬 Генетический алгоритм. Покрытие точек квадратами</h1>
  <p>
    <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python">
    <img src="https://img.shields.io/badge/PyQt5-GUI-green.svg" alt="PyQt5">
  </p>
</div>
Программа с графическим интерфейсом для решения задачи о покрытии точек на плоскости с использованием генетического алгоритма. 

## 📌 О проекте

**Постановка задачи:** Дано $N$ точек в двумерном евклидовом пространстве. Необходимо найти координаты левого нижнего угла и длины сторон для $M$ квадратов так, чтобы они суммарно содержали максимальное количество точек внутри и **не пересекались** между собой.

Программа визуализирует процесс эволюции, позволяет гибко настраивать гиперпараметры алгоритма и анализировать графики функции приспособленности.


### 🖥️ Главное окно приложения
<table width="100%" style="border: none; text-align: center;">
  <tr>
    <td align="center" width="50%" style="border: none">
      <img src="https://drive.google.com/uc?export=view&id=11G2ErGBnJCXrcvV3rPHxux00DACT-J73" width="100%">
      <br>
      <b>☀️ Светлая тема</b>
    </td>
    <td align="center" width="50%" style="border: none">
      <img src="https://drive.google.com/uc?export=view&id=1FIb7AQvaW2vmq8uiTVukIdNpI5vstjiZ" width="100%">
      <br>
      <b>🌙 Тёмная тема</b>
    </td>
  </tr>
</table>
<!-- ![Главное окно программы](https://drive.google.com/uc?export=view&id=11G2ErGBnJCXrcvV3rPHxux00DACT-J73) -->

## ⚙️ Ключевые возможности
- **Интерактивный GUI:** Удобная настройка параметров алгоритма.
- **График Matplotlib:** Построение графиков лучшей и средней приспособленности по шагам.
- **Пошаговая визуализация:** Возможность просматривать историю изменения решения.
- **Подробный отчет:** Подробная информация по генам для каждой особи из любой популяции.
- **Загрузка/Сохранение:** Возможность загружать точки из форматов `.json` и `.txt`, сохранять точки и информацию о популяциях в формате `.json` или `.txt`.
- **Темы оформления:** Поддержка светлой и темной тем.

## 🚀 Установка и запуск

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/VARositsky/genetic-optimization-gui.git
   cd genetic-optimization-gui
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустите командой:
   ```bash
   python MainWindow.py
   ```
