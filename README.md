# EduMost Books

Репозиторий **контента книг** EduMost · серия **Engineering Roadmap** (5 самостоятельных книг · 50 лабораторий).

Каждая книга — **независимый пакет**: собственный `book.toml`, контент, assets, i18n и release ZIP.

## Книги

| Книга | seriesOrder | Лаборатории | Исходники | Release ZIP |
|-------|-------------|-------------|-----------|-------------|
| [engineering-roadmap-tom-01/](engineering-roadmap-tom-01/) | 1 | 10 | ✅ | [tom-01.zip](releases/engineering-roadmap-tom-01.zip) |
| [engineering-roadmap-tom-02/](engineering-roadmap-tom-02/) | 2 | 10 | ✅ | [tom-02.zip](releases/engineering-roadmap-tom-02.zip) |
| [engineering-roadmap-tom-03/](engineering-roadmap-tom-03/) | 3 | 10 | ✅ | [tom-03.zip](releases/engineering-roadmap-tom-03.zip) |
| [engineering-roadmap-tom-04/](engineering-roadmap-tom-04/) | 4 | 10 | ✅ | [tom-04.zip](releases/engineering-roadmap-tom-04.zip) |
| [engineering-roadmap-tom-05/](engineering-roadmap-tom-05/) | 5 | 10 | ✅ | [tom-05.zip](releases/engineering-roadmap-tom-05.zip) |

```toml
series = "Engineering Roadmap"
seriesId = "engineering-roadmap"
seriesOrder = 1…5
```

## Структура одной книги

```
engineering-roadmap-tom-0N/
├── book.toml
├── metadata/library.json
├── assets/illustrations/   # ILL-*.webp|png|svg (для Reader)
├── prompts/                # EduMost Illustration Prompt (не показывается читателю)
├── i18n/
├── ru/tom-0N/content/      # лаборатории с :::illustration
├── README.md
└── CHANGELOG.md
```

В Markdown книги:

```markdown
## 📷 Иллюстрация

:::illustration
ILL-T1-L0-01
:::
```

Промпт художника — только в `prompts/ILL-T1-L0-01.md`.

## Release ZIP (Reader)

Публикационный артефакт для **EduMost Reader** — zip **исходной папки книги** (`book.toml` в корне архива):

```
releases/
├── engineering-roadmap-tom-01.zip
├── …
└── engineering-roadmap-tom-05.zip
```

## Облачный каталог

[`catalog.json`](catalog.json) — список опубликованных книг для Reader (следующий этап: UI каталога).

```json
{
  "version": "1.0",
  "books": [{ "id": "...", "releaseUrl": "https://github.com/.../releases/....zip" }]
}
```

Создание:

```bash
./scripts/make-releases.sh
# или одной книги:
./scripts/make-releases.sh engineering-roadmap-tom-01
```

**Импорт в Reader:** ссылка на ZIP в GitHub или файл с диска.

Пример ссылки:

```
https://github.com/edumost-pl/edumost-books/blob/main/releases/engineering-roadmap-tom-01.zip
```

## Сборка (Publisher)

```bash
cd ../EduMost-Publisher
npx tsx packages/cli/src/index.ts doctor ../EduMost-Books/engineering-roadmap-tom-01
npx tsx packages/cli/src/index.ts build ../EduMost-Books/engineering-roadmap-tom-01
```

## Авторский источник

`../ENGINEERING_ROADMAP/` — канонический текст лабораторий и [WORKFLOW_ROLI.md](../ENGINEERING_ROADMAP/WORKFLOW_ROLI.md).

---

*EduMost Engineering Academy · Engineering Roadmap v1.0*
