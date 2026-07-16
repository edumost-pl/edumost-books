# ENGINEERING ROADMAP
## Том 5 · Лаборатория №7 — Космос

> **🟣 Архитектор технологий** · Миссия дня

---

## 📡 История

**Мехатроника** (Лаб. №6) — **земная** гравитация, **воздух**, **розетка** рядом. **Космос** **меняет** **все** **допущения**: **vacuum**, **радиация**, **thermal**, **delay**, **single failure = mission loss**. Ты **не** обязан **летать** — но **архитектор** **должен** **читать** **миссии** как **system design** **на максимуме**. Сегодня — **орбитальная** лаборатория **на столе**: **телеметрия**, **link budget**, **этика** **dual-use** и **деbris**.

---

## 🚀 Миссия

**Смоделировать** мини-миссию (CubeSat-style / Mars rover sim) с **телеметрией**, **задержкой** и **mission ops** документом.

---

## 🎯 Цель

- **понять** **subsystems** космического аппарата (power, comms, ADCS, payload);
- **реализовать** **delayed telemetry** **через** скрипт **или** симулятор;
- **написать** **ops playbook** **≥ 1** anomaly.

**Результат:** `~/Moja_Laboratoria/T5/space/mission_ops.md` + **лог** **≥ 20** telemetry packets.

---

## ⏱ Время

3–5 часов (можно **4 дня** по 45 min).

---

## 🧰 Что понадобится

- [ ] ПК + Python (Том 1, Лаб. №0)
- [ ] Опционально: **Kerbal Space Program** / **OpenRocket** / **NASA Eyes**
- [ ] Опционально: ESP32 **как** «спутник» на **столе**
- [ ] dnevnik.txt

---

## 🤔 Как ты думаешь?

**Не читай ответ сразу.**

1. Почему **Mars** **rover** **не** **управляют** **джойстиком** **real-time**?
2. **Solar panel** **+** **eclipse** — **что** **отключить** **первым**?
3. **Спутник** с **ИИ** **автономного** **maneuver** — **кто** **отвечает** **за** **debris**?

*(Запиши в dnevnik.)*

**Настоящее объяснение:** **Light-time delay** → **autonomy** + **planning**. **Power budget** → **режимы** **safe** / **science** / **sleep**. **Space ethics:** **deorbiting**, **не** **мусорить** orbit, **dual-use** **технологии** (навигация **vs** **weaponization**) — **инженер** **осознан**.

---

## 💡 Аналогия

**Космический аппарат** = **подводная лодка** **без** **возможности** **всплыть** **починить** **USB**. **Mission Control** = **Том 3** **NOC**, но **ping** **минуты**, **не** **ms**.

| В жизни | Космос |
|---------|--------|
| Wi‑Fi дома | **Deep Space Network** |
| UPS | **Battery + eclipse** |
| `ping google` | **Round-trip light time** |
| Docker restart | **Safe mode reboot** |
| GDPR | **Planetary protection** |

### 😲 ВАУ!

**Voyager** **still** **отправляет** **данные** — **< 1 W** **transmitter**, **delay** **> 20 h**. **Инженерия** **терпения**.

### 😄 Момент улыбки

«**Перезагрузи** **спутник** **Ctrl+Alt+Del**» — **если** **работает**, **ты** **либо** **гений**, **либо** **создал** **debris**.

---

## 📷 Иллюстрация

:::illustration
ILL-T5-L7-01
:::

## 📊 Mermaid

```mermaid
flowchart TB
    subgraph space["Spacecraft"]
        PWR[Power EPS]
        COM[Comms]
        ADCS[ADCS]
        PL[Payload sensors]
        OBC[On-board computer]
    end
    subgraph ground["Mission Control"]
        MC[Ops team / you]
        LOG[Archives NAS]
    end
    OBC --> PWR
    PL --> OBC
    ADCS --> OBC
    OBC <-->|delayed RF| COM
    COM <-->|RTT| MC
    MC --> LOG
```

```mermaid
stateDiagram-v2
    [*] --> Safe
    Safe --> Science: power OK
    Science --> Safe: low power
    Safe --> Sleep: eclipse
    Sleep --> Safe: sun
```

---

## 🔬 Эксперимент

**Правило:** минимум **№1, №2, №3, №5**.

---

### Эксперимент 1 — «Subsystem map»

**⏱** 30 min

`mission_ops.md`:

| Subsystem | Function | Failure |
|-----------|----------|---------|
| EPS | Power | Brownout |
| COM | Link | Loss of signal |
| ADCS | Pointing | Tumble |
| TTC | Command | Wrong opcode |
| PL | Science | Noise |

**✅ Проверь себя:** **≥ 5** subsystems.

---

### Эксперимент 2 — «Telemetry simulator»

**⏱** 45 min

`~/Moja_Laboratoria/T5/space/telemetry_sim.py`:

```python
import json, time, random
for i in range(25):
    pkt = {
        "mission_time_s": i * 60,
        "battery_v": round(7.4 - i*0.01 + random.uniform(-0.02, 0.02), 2),
        "temp_c": round(20 + random.uniform(-2, 5), 1),
        "signal_dbm": round(-90 + random.uniform(-5, 5), 1),
    }
    print(json.dumps(pkt))
    time.sleep(0.2)  # ускоренно; для Mars добавь time.sleep(720) в комментарии
```

```bash
python3 ~/Moja_Laboratoria/T5/space/telemetry_sim.py | tee ~/Moja_Laboratoria/T5/space/tm.log
```

**✅ Проверь себя:** **≥ 20** строк **в** tm.log.

---

### Эксперимент 3 — «Light-time delay»

**⏱** 25 min

Добавь **функцию** `mars_rtt_min = 4` **to** `22` **в** **зависимости** от **opposition**.

**Упражнение:** команда «**поверни** **solar** **panel**» → **ответ** **через** **RTT/2** **min** **в** sim.

**✅ Проверь себя:** **1** **абзац** **в** dnevnik: **почему** **autonomy** **обязательна**.

---

### Эксперимент 4 — «OpenRocket / KSP / NASA Eyes»

**⏱** 45 min *(рекомендуется)*

**Один** **из**:

- **OpenRocket:** **стability** **margin**
- **KSP:** **orbit** **insertion** **Δv** **запись**
- **NASA Eyes:** **скрин** **миссии** **+** **1** **факт**

**✅ Проверь себя:** **скрин** **+** **caption** **в** mission_ops.

---

### Эксперимент 5 — «Anomaly playbook»

**⏱** 30 min

Сценарий: **battery_v < 7.0** **3** **packets** **подряд**.

**Playbook:**

1. **Detect**
2. **Safe mode** (отключить payload)
3. **Notify** ops
4. **Log** to NAS (Том 3)
5. **Review** post-mortem

**Этика:** **autonomous** **deorbit** **ИИ** — **только** **с** **human** **approval** **на** **Земле**.

**✅ Проверь себя:** **5** **шагов** **numbered**.

---

### Эксперимент 6 — «Space + local AI»

**⏱** 20 min *(рекомендуется)*

**Paper design:** **Ollama** **на** **Земле** **не** **управляет** **thrusters** **real-time** — **only** **plan** **upload** **batch**.

**✅ Проверь себя:** **NFR** **в** **1** **абзаце**.

---

## ⚠ Типичные ошибки

| Ошибка | Как исправить |
|--------|---------------|
| **Real-time** **ожидание** **Mars** | **Plan** **blocks** |
| **Ignore** **thermal** | **Model** **temp** **telemetry** |
| **No** **safe** **mode** | **Default** **Safe** |
| **Kessler** **who cares** | **Deorbit** **plan** |
| **ИИ** **=** **auto** **maneuver** | **Human** **gate** |
| **Секретные** **TLE** **в** **Git** | **Не** **commit** |

---

## 🧪 Проверь себя

- [ ] mission_ops.md **готов**
- [ ] tm.log **≥ 20** packets
- [ ] Delay **объяснён**
- [ ] Anomaly playbook **5** steps
- [ ] **Этика** **debris/AI** **1** **абзац**

---

## 📝 Запись в инженерный dnevnik

```
=== LAB №7 (TOM 5) ===
Data: ___
Mission name: ___
RTT (sim): ___ min
Anomaly trained:
Space ethics (1 zdanie):
Następny krok:
```

---

## 🏆 Что теперь умеешь

- [ ] **Читать** **космическую** **миссию** как **system**
- [ ] **Симулировать** **telemetry** **и** **delay**
- [ ] **Писать** **ops** **playbook**
- [ ] **Связать** **NAS** **logging** **(T3)** **с** **ops**
- [ ] **Обсуждать** **этику** **orbit** **и** **AI**

---

## ➡ Что дальше

**Следующий файл:** `08_LAB_AVIACIJA.md` — **Лаборатория №8:** **атмосфера**, **аэродинамика**, **сертификация**.

**Перед переходом:**

- [ ] telemetry + playbook — **обязательно**
- [ ] LAB №7 — **обязательно**

### 🔮 Вопрос без ответа

**CubeSat** **в** **vacuum**. **Самолёт** **в** **air**. **Общее** **между** **орбитой** **и** **крылом** — **кроме** **«летает»**?

**Ответ — в Лаборатории №8.**

---

*Запусти **telemetry_sim**. **Подожди** **RTT** — **даже** **в** **sim** **учит** **терпению**.*
