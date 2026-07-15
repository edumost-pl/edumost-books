# Engineering Roadmap · Tom 3 — Серверы и сети

Самостоятельная книга серии **Engineering Roadmap** · 🟡 Уровень 3 · Системный инженер

| Поле | Значение |
|------|----------|
| **id** | `engineering-roadmap-tom-03` |
| **seriesId** | `engineering-roadmap` |
| **seriesOrder** | 3 |
| **Статус** | ✅ **READY** — 10/10 лабораторий |

## Лаборатории

| № | Файл |
|---|------|
| 0 | `00_LAB_SSH.md` |
| 1 | `01_LAB_GIT.md` |
| 2 | `02_LAB_DOCKER.md` |
| 3 | `03_LAB_NAS.md` |
| 4 | `04_LAB_PIHOLE.md` |
| 5 | `05_LAB_VPN.md` |
| 6 | `06_LAB_HOME_ASSISTANT.md` |
| 7 | `07_LAB_DNS.md` |
| 8 | `08_LAB_ROUTER.md` |
| 9 | `09_LAB_INFRASTRUKTURA.md` |

**Capstone:** Домашний NAS

## Release

Reader ZIP: [`../releases/engineering-roadmap-tom-03.zip`](../releases/engineering-roadmap-tom-03.zip)

Пересборка:

```bash
../scripts/make-releases.sh engineering-roadmap-tom-03
```

## Сборка

```bash
cd ../../EduMost-Publisher
npx tsx packages/cli/src/index.ts doctor ../EduMost-Books/engineering-roadmap-tom-03
npx tsx packages/cli/src/index.ts build ../EduMost-Books/engineering-roadmap-tom-03
```

## Стандарты

- [KONSTITUTSIYA.md](../../ENGINEERING_ROADMAP/KONSTITUTSIYA.md)
- [SHABLON_LABORATORII.md](../../ENGINEERING_ROADMAP/SHABLON_LABORATORII.md)
