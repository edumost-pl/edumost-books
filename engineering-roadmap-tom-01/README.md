# Engineering Roadmap · Tom 1 — Основы инженера

Самостоятельная книга серии **Engineering Roadmap** · 🟢 Уровень 1 · Исследователь

| Поле | Значение |
|------|----------|
| **id** | `engineering-roadmap-tom-01` |
| **seriesId** | `engineering-roadmap` |
| **seriesOrder** | 1 |
| **Статус** | ✅ **READY** — 10/10 лабораторий |

## Лаборатории

| № | Файл |
|---|------|
| 0 | `00_LAB_DOBRO_POZALOVAT.md` |
| 1 | `01_LAB_KOMPUTER.md` |
| 2 | `02_LAB_TERMINAL.md` |
| 3 | `03_LAB_LINUX.md` |
| 4 | `04_LAB_FAJLY.md` |
| 5 | `05_LAB_BASH.md` |
| 6 | `06_LAB_SERVER.md` |
| 7 | `07_LAB_SET.md` |
| 8 | `08_LAB_INTERNET.md` |
| 9 | `09_LAB_MINECRAFT_PROEKT.md` |

**Capstone:** Minecraft-сервер

## Release

Reader ZIP: [`../releases/engineering-roadmap-tom-01.zip`](../releases/engineering-roadmap-tom-01.zip)

Пересборка:

```bash
../scripts/make-releases.sh engineering-roadmap-tom-01
```

## Сборка

```bash
cd ../../EduMost-Publisher
npx tsx packages/cli/src/index.ts doctor ../EduMost-Books/engineering-roadmap-tom-01
npx tsx packages/cli/src/index.ts build ../EduMost-Books/engineering-roadmap-tom-01
```

## Стандарты

- [KONSTITUTSIYA.md](../../ENGINEERING_ROADMAP/KONSTITUTSIYA.md)
- [SHABLON_LABORATORII.md](../../ENGINEERING_ROADMAP/SHABLON_LABORATORII.md)
