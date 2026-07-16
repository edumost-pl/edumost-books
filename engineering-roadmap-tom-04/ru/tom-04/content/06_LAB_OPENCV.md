# ENGINEERING ROADMAP
## Том 4 · Лаборатория №6 — OpenCV

> **Библиотека, которая видит быстро** · Миссия дня

---

## 📡 История

В **Лаб. №5** ты **сам** считал яркость и центр — **понял** идею. На **живом** видео 30 кадров/с самописный цикл **тормозит**. **OpenCV** — индустриальный **стандарт** CV: готовые функции **контуров**, **фильтров**, **рисования** — оптимизированы под **C++** внутри, **Python** снаружи. Сегодня — **поставить** OpenCV на Pi и **обработать** поток с камеры: линия, контур, FPS.

---

## 🚀 Миссия

**Установить** OpenCV на Raspberry Pi, **написать** `line_follow_preview.py`, который **в реальном времени** показывает (или сохраняет кадры) **маску линии** и **центр** — зачем библиотека, а не только numpy.

---

## 🎯 Цель

- **установить** `opencv-python` (или `python3-opencv` из apt);
- **использовать** `cv2.findContours`, `cv2.moments`, `cv2.GaussianBlur`;
- **измерить FPS** обработки и **сравнить** с Лаб. №5.

**Результат:** скрипт обрабатывает **tape.jpg** и **5+ кадров** с камеры, `opencv_result.jpg`, FPS в dnevnik.

---

## ⏱ Время

90–120 мин (можно **3–4 дня** по 30 мин). Установка OpenCV на Pi может занять **20–40 мин**.

---

## 🧰 Что понадобится

- [ ] Raspberry Pi (**Лаб. №4–5**)
- [ ] `tape.jpg` или чёрная линия на полу
- [ ] Python 3, pip
- [ ] (Опционально) Монитор HDMI к Pi **или** только сохранение кадров без GUI
- [ ] **Терпение** при `pip install opencv-python` на Pi *(альтернатива: `sudo apt install python3-opencv`)*

---

## 🤔 Как ты думаешь?

**Не читай ответ сразу.**

1. Зачем **размытие** (blur) **до** порога, если линия **и так** видна?
2. `findContours` находит **много** форм. Как выбрать **линию**, а не **тень**?
3. OpenCV **тяжёлый** для Pi. Когда **стоит** вернуться к **простому** numpy?

*(Запиши в dnevnik.)*

**Настоящее объяснение:** **GaussianBlur** убирает **шум** сенсора — порог **стабильнее**. Контуры сортируют по **площади** — берём **самый большой** в нижней половине кадра (ROI). OpenCV **нужен**, когда **FPS** и **много операций**; на **одном** кадре numpy **достаточно** (Лаб. №5). На Pi часто **apt** быстрее, чем **pip** сборка.

---

## 💡 Аналогия

**Набор LEGO vs свой пластилин:** numpy — **лепишь** каждый кирпич. OpenCV — **коробка** с готовыми **дугами и колёсами**. Робот на соревновании — **LEGO**; одна домашняя задача — можно **лепить**.

| В жизни | OpenCV |
|---------|--------|
| Фильтр в Instagram | `GaussianBlur` |
| Обводка стикера | `findContours` |
| Счётчик кадров в игре | **FPS** |
| «Возьми самый большой кусок» | `max(contours, key=area)` |

### 😲 ВАУ!

**OpenCV** начался в **Intel** в 1999 году, сейчас **открытый** код. Его используют **Bosch** (автопилот), **NASA** (навигация), **медицина** (рентген) — один API, **миллионы** строк оптимизаций **бесплатно**.

### 😄 Момент улыбки

`pip install opencv-python` на Pi — момент, когда чай **остывает**, а прогресс-бар **ползёт**. `sudo apt install python3-opencv` — **скучнее**, но ты **инженер**, не **мученик**.

---

## 📷 Иллюстрация

:::illustration
ILL-T4-L6-01
:::

## 📊 Mermaid

```mermaid
flowchart LR
    CAM[Камера / файл] --> CV[cv2.imread / VideoCapture]
    CV --> ROI[Обрезка низа кадра]
    ROI --> BLUR[GaussianBlur]
    BLUR --> TH[cv2.threshold]
    TH --> FC[findContours]
    FC --> BIG[Крупнейший контур]
    BIG --> M[moments центр]
    M --> DRAW[circle + line]
    DRAW --> OUT[jpg / дисплей]
```

---

## 🔬 Эксперимент

**Минимум для зачёта:** **№1, №2, №3, №4**. **Рекомендуется:** все **6**.

---

### Эксперимент 1 — «Установка OpenCV»

**⏱** 20–40 мин

**Обязательный.**

```bash
cd ~/robot_vision
sudo apt update
sudo apt install -y python3-opencv python3-pip
python3 -c "import cv2; print(cv2.__version__)"
```

Если версия **не** печатается:

```bash
pip3 install --user opencv-python-headless
python3 -c "import cv2; print(cv2.__version__)"
```

| apt `python3-opencv` | **Быстро** на Pi | Может быть **старая** версия | Для учёбы OK |
| headless | **Без** GUI на сервере | Меньше зависимостей | Нет `imshow` на Pi без X |

**✅ Проверь себя:** `cv2.__version__` **напечатана**.

---

### Эксперимент 2 — «Один кадр: контуры»

**⏱** 20 мин

```python
# opencv_contour.py
import cv2
import numpy as np

img = cv2.imread("tape.jpg")
h, w = img.shape[:2]
roi = img[h//2:, :]  # только низ — где линия
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
_, mask = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

out = roi.copy()
if contours:
    c = max(contours, key=cv2.contourArea)
    M = cv2.moments(c)
    if M["m00"] > 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        cv2.circle(out, (cx, cy), 10, (0, 255, 0), 2)
        cv2.drawContours(out, [c], -1, (255, 0, 0), 2)
        print("Center:", cx, cy)

cv2.imwrite("opencv_result.jpg", out)
cv2.imwrite("opencv_mask.jpg", mask)
```

| ROI нижняя половина | Меньше **неба/стены** | Контур **стабильнее** | — |
| `THRESH_BINARY_INV` | Тёмная линия → **белая** на маске | Подбери 80–120 | — |

**✅ Проверь себя:** `opencv_result.jpg` — **круг** на линии.

---

### Эксперимент 3 — «Ошибка руля + текст на кадре»

**⏱** 15 мин

```python
err = cx - (w // 2)
steer = "LEFT" if err < -30 else "RIGHT" if err > 30 else "STRAIGHT"
cv2.putText(out, f"err={err} {steer}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
```

**✅ Проверь себя:** на jpg виден **текст** err и LEFT/RIGHT/STRAIGHT.

---

### Эксперимент 4 — «Псевдо-видео: 30 кадров с FPS»

**⏱** 25 мин

**Обязательный для зачёта.**

```bash
libcamera-still -o frame_%03d.jpg --width 320 --height 240 --timelapse 100 -t 3000
```

```python
# opencv_fps.py
import cv2
import time
import glob

paths = sorted(glob.glob("frame_*.jpg"))
t0 = time.time()
for p in paths:
    img = cv2.imread(p)
    # ... тот же pipeline ROI + contour ...
    # cv2.imwrite("proc_" + p, out)
n = len(paths)
dt = time.time() - t0
print(f"Frames: {n}, FPS: {n/dt:.1f}")
```

| FPS | **Кадров/сек** обработки | Для робота нужно **> 5** минимум | Уменьши разрешение |

**✅ Проверь себя:** FPS **напечатан**; сравни с Лаб. №5.

---

### Эксперимент 5 — «Живой поток USB (если есть)»

**⏱** 20 мин

```python
# usb_preview.py — только если есть /dev/video0
import cv2
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
ret, frame = cap.read()
if ret:
    cv2.imwrite("live_frame.jpg", frame)
cap.release()
```

Для CSI на Pi иногда используют **v4l2** loopback или **picamera2** + numpy → cv2 — запиши в dnevnik, что сработало **у тебя**.

**✅ Проверь себя:** `live_frame.jpg` **или** честная запись «только still».

---

### Эксперимент 6 — «Таблица: numpy vs OpenCV»

**⏱** 10 мин

**Рекомендуется.**

| Критерий | numpy (Лаб.5) | OpenCV |
|----------|---------------|--------|
| Понятность | | |
| Скорость на Pi | | |
| Контуры сложной формы | | |
| Зависимости | | |

**✅ Проверь себя:** **4 строки** заполнены.

---

## ⚠ Типичные ошибки

| Проблема | Как исправить |
|----------|---------------|
| `import cv2` fail | `apt install python3-opencv` |
| Пустые contours | Инвертируй порог; проверь **ROI**; свет |
| cx **скачет** | Blur; min площадь контура; игнор мелких |
| FPS **< 3** | 320×240; только ROI; пропуск кадров |
| `imshow` не работает | Headless — только `imwrite`; SSH без X |

---

## 🧪 Проверь себя

- [ ] OpenCV **установлен**, версия известна
- [ ] `opencv_result.jpg` с контуром и центром
- [ ] **err** и LEFT/RIGHT на кадре
- [ ] FPS на **серии** кадров измерен
- [ ] Таблица numpy vs OpenCV
- [ ] Скрипты в `~/robot_vision/`

---

## 📝 Запись в инженерный дневник

```
=== TOM4 LAB №6 — OPENCV ===
Дата: ___
cv2 version: ___
Порог / ROI: ___
opencv_result.jpg: ДА/НЕТ
FPS (n кадров): ___
Живой USB кадр: ДА/НЕТ / N/A
numpy vs OpenCV (1 предложение):
Что было сложно:
Следующая идея:
```

---

## 🏆 Что теперь умеешь

- [ ] **Установить** OpenCV на Pi **практичным** способом
- [ ] **Строить** pipeline: blur → threshold → contours → moments
- [ ] **Ограничивать** ROI для **скорости** и **стабильности**
- [ ] **Считать FPS** и **сравнивать** с самописным кодом
- [ ] **Выбирать**: библиотека vs numpy по **задаче**

---

## ➡ Что дальше

**Следующий файл:** `07_LAB_RASPBERRY_ROBOT.md` — **соединить** Pi (глаза) и Arduino (ноги) по **Serial**.

**Перед переходом:**

- [ ] **opencv_result + FPS** — **обязательно**
- [ ] Установка cv2 — **обязательно**
- [ ] err на кадре — **обязательно**
- [ ] Таблица сравнения — **рекомендуется**
- [ ] USB кадр — **рекомендуется**

### 🔮 Вопрос без ответа

Pi **считает** «влево». Arduino **крутит** моторы. Как **два** компьютера **договорятся** за **миллисекунды**, не **споря**?

**Ответ — в Лаборатории №7.**

---

*Сохрани opencv_result.jpg. Библиотека **сделала** тяжёлую математику — ты **свободен** думать о **роботе**.*
