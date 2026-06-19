from pathlib import Path


DOCS_DIR = Path(__file__).resolve().parent.parent / "data" / "docs"


def load_docs() -> list[dict[str, str]]:
    docs = []

    if not DOCS_DIR.exists():
        return docs

    for path in DOCS_DIR.glob("*.md"):
        content = path.read_text(encoding="utf-8")
        docs.append(
            {
                "title": path.stem.replace("_", " ").title(),
                "filename": path.name,
                "content": content,
            }
        )

    return docs


def search_docs(query: str, limit: int = 3) -> list[dict[str, str]]:
    q = query.lower()
    query_words = set(q.split())

    scored_docs = []

    for doc in load_docs():
        searchable_text = f"{doc['title']} {doc['content']}".lower()

        score = 0

        if q in searchable_text:
            score += 10

        for word in query_words:
            if word in searchable_text:
                score += 1

        if score > 0:
            snippet = doc["content"][:600].strip()
            scored_docs.append(
                {
                    "score": score,
                    "title": doc["title"],
                    "filename": doc["filename"],
                    "snippet": snippet,
                }
            )

    scored_docs.sort(key=lambda item: item["score"], reverse=True)

    return scored_docs[:limit]