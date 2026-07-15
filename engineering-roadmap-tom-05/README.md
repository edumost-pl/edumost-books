# Engineering Roadmap · Tom 5 — Инженер будущего

Самостоятельная книга серии **Engineering Roadmap** · 🟣 Уровень 5 · Инженер будущего

| Поле | Значение |
|------|----------|
| **id** | `engineering-roadmap-tom-05` |
| **seriesId** | `engineering-roadmap` |
| **seriesOrder** | 5 |
| **Статус** | ✅ **READY** — 10/10 лабораторий |

## Лаборатории

| № | Файл |
|---|------|
| 0 | `00_LAB_II.md` |
| 1 | `01_LAB_LOKALNY_II.md` |
| 2 | `02_LAB_DRONY.md` |
| 3 | `03_LAB_3D_PECHAT.md` |
| 4 | `04_LAB_CAD.md` |
| 5 | `05_LAB_PROEKTIROVANIE.md` |
| 6 | `06_LAB_MEHATRONIKA.md` |
| 7 | `07_LAB_KOSMOS.md` |
| 8 | `08_LAB_AVIACIJA.md` |
| 9 | `09_LAB_FINALNY_PROEKT.md` |

**Capstone:** Финальный проект

## Release

Reader ZIP: [`../releases/engineering-roadmap-tom-05.zip`](../releases/engineering-roadmap-tom-05.zip)

Пересборка:

```bash
../scripts/make-releases.sh engineering-roadmap-tom-05
```

## Сборка

```bash
cd ../../EduMost-Publisher
npx tsx packages/cli/src/index.ts doctor ../EduMost-Books/engineering-roadmap-tom-05
npx tsx packages/cli/src/index.ts build ../EduMost-Books/engineering-roadmap-tom-05
```

## Стандарты

- [KONSTITUTSIYA.md](../../ENGINEERING_ROADMAP/KONSTITUTSIYA.md)
- [SHABLON_LABORATORII.md](../../ENGINEERING_ROADMAP/SHABLON_LABORATORII.md)
