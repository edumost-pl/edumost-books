# Engineering Roadmap · Tom 2 — Электроника и Raspberry Pi

Самостоятельная книга серии **Engineering Roadmap** · 🔵 Уровень 2 · Конструктор

| Поле | Значение |
|------|----------|
| **id** | `engineering-roadmap-tom-02` |
| **seriesId** | `engineering-roadmap` |
| **seriesOrder** | 2 |
| **Статус** | ✅ **READY** — 10/10 лабораторий |

## Лаборатории

| № | Файл |
|---|------|
| 0 | `00_LAB_RASPBERRY_PI.md` |
| 1 | `01_LAB_GPIO.md` |
| 2 | `02_LAB_ELEKTRICHESTVO.md` |
| 3 | `03_LAB_BREADBOARD.md` |
| 4 | `04_LAB_LED.md` |
| 5 | `05_LAB_KNOPKI.md` |
| 6 | `06_LAB_DATCHIKI.md` |
| 7 | `07_LAB_DVIGATELI.md` |
| 8 | `08_LAB_ESP32.md` |
| 9 | `09_LAB_METEOSTANCJA.md` |

**Capstone:** Домашняя метеостанция

## Release

Reader ZIP: [`../releases/engineering-roadmap-tom-02.zip`](../releases/engineering-roadmap-tom-02.zip)

Пересборка:

```bash
../scripts/make-releases.sh engineering-roadmap-tom-02
```

## Сборка

```bash
cd ../../EduMost-Publisher
npx tsx packages/cli/src/index.ts doctor ../EduMost-Books/engineering-roadmap-tom-02
npx tsx packages/cli/src/index.ts build ../EduMost-Books/engineering-roadmap-tom-02
```

## Стандарты

- [KONSTITUTSIYA.md](../../ENGINEERING_ROADMAP/KONSTITUTSIYA.md)
- [SHABLON_LABORATORII.md](../../ENGINEERING_ROADMAP/SHABLON_LABORATORII.md)
