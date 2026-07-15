# EduMost Books

Репозиторий **контента книг** EduMost Publishing Platform.

Каждая папка — самодостаточная книга по [EduMost Book Specification](https://github.com/edumost-pl/edumost-book-specification).

| Книга | Статус | Том |
|-------|--------|-----|
| [engineering-roadmap/](engineering-roadmap/) | active | Tom 1 — 10 labs |

## Принцип

> Автор создаёт книгу. Publisher собирает Web · PDF · EPUB.

Этот репозиторий **не содержит код** Publisher или Reader.

## Структура книги

```
{book-id}/
├── book.toml
├── metadata/library.json
├── i18n/
├── assets/illustrations/
└── {locale}/{volume}/content/*.md
```

См. спецификацию: `edumost-pl/edumost-book-specification`.

## Сборка

Сборка выполняется **EduMost Publisher** (пока — EduMost-Book-Engine как эталон):

```bash
# Эталон (старый путь, до миграции Publisher)
cd ../EduMost-Book-Engine
pnpm build:book

# Будущий путь (после миграции Publisher)
edumost build ../EduMost-Books/engineering-roadmap
```

## Версионирование

Git tags: `engineering-roadmap-v1.0.0`
