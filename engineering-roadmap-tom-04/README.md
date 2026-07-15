# Engineering Roadmap · Tom 4 — Робототехника

Самостоятельная книга серии **Engineering Roadmap** · 🔴 Уровень 4 · Робототехник

| Поле | Значение |
|------|----------|
| **id** | `engineering-roadmap-tom-04` |
| **seriesId** | `engineering-roadmap` |
| **seriesOrder** | 4 |
| **Статус** | ✅ **READY** — 10/10 лабораторий |

## Лаборатории

| № | Файл |
|---|------|
| 0 | `00_LAB_ARDUINO.md` |
| 1 | `01_LAB_SERVO.md` |
| 2 | `02_LAB_ULTRAZVUK.md` |
| 3 | `03_LAB_ROBOT.md` |
| 4 | `04_LAB_KAMERA.md` |
| 5 | `05_LAB_COMPUTER_VISION.md` |
| 6 | `06_LAB_OPENCV.md` |
| 7 | `07_LAB_RASPBERRY_ROBOT.md` |
| 8 | `08_LAB_AVTOMATIZACJA.md` |
| 9 | `09_LAB_AVTONOMNY_ROBOT.md` |

**Capstone:** Автономный робот

## Release

Reader ZIP: [`../releases/engineering-roadmap-tom-04.zip`](../releases/engineering-roadmap-tom-04.zip)

Пересборка:

```bash
../scripts/make-releases.sh engineering-roadmap-tom-04
```

## Сборка

```bash
cd ../../EduMost-Publisher
npx tsx packages/cli/src/index.ts doctor ../EduMost-Books/engineering-roadmap-tom-04
npx tsx packages/cli/src/index.ts build ../EduMost-Books/engineering-roadmap-tom-04
```

## Стандарты

- [KONSTITUTSIYA.md](../../ENGINEERING_ROADMAP/KONSTITUTSIYA.md)
- [SHABLON_LABORATORII.md](../../ENGINEERING_ROADMAP/SHABLON_LABORATORII.md)
