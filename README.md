# Калькулятор на Kivy

Компактный калькулятор с тёмным интерфейсом, крупными кнопками и поддержкой мыши, сенсорного экрана и клавиатуры.

## Запуск

Нужен Python 3.9 или новее. В терминале выполните:

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Кнопки `+`, `−`, `×`, `÷` выполняют последовательные вычисления; `=` можно нажимать повторно. `%` делит отображаемое число на 100. `AC` очищает калькулятор, `⌫` удаляет последний символ. При делении на ноль выводится сообщение об ошибке.

На клавиатуре доступны цифры, `+`, `-`, `*`, `/`, точка или запятая, `%`, Enter или `=`, Backspace и Escape/Delete для очистки.

## Проверка логики

```bash
python -m unittest discover -s tests
```

## Сборка для Android

Для сборки нужен Linux (или WSL), Python 3, Java 17 и системные зависимости Buildozer. Установите их согласно [инструкции Buildozer](https://buildozer.readthedocs.io/en/latest/installation.html), затем из корня проекта выполните:

```bash
python -m pip install buildozer 'Cython==0.29.37' setuptools wheel
buildozer android debug
```

При первой сборке Buildozer скачивает Android SDK, NDK и другие компоненты; для этого нужен доступ в интернет. Готовый отладочный APK находится в `bin/`. Его можно установить на устройство командой `adb install -r bin/*.apk`. Для публикации понадобится отдельная подписанная release-сборка.

Также можно запустить сборку через GitHub Actions: после публикации изменений в репозитории откройте **Actions → Build Android APK → Run workflow**, выберите ветку проекта и скачайте артефакт `calculator-android-debug` после завершения. В APK включён Kivy; KivyMD не включается, поскольку интерфейс приложения его не использует.
