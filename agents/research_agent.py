from __future__ import annotations

import dataclasses
import json
import re
from typing import Dict, Optional

import requests


WIKI_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
WIKI_SEARCH_URL = "https://en.wikipedia.org/w/rest.php/v1/search/title"


@dataclasses.dataclass
class ResearchProfile:
    name: str
    description: Optional[str]
    birth_date: Optional[str]
    death_date: Optional[str]
    extract: Optional[str]
    url: Optional[str]

    def to_brief_dict(self) -> Dict[str, Optional[str]]:
        return dataclasses.asdict(self)


class ResearchAgent:
    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()

    def _search_title(self, name: str) -> Optional[str]:
        params = {"q": name, "limit": 1}
        resp = self.session.get(WIKI_SEARCH_URL, params=params, timeout=15)
        if not resp.ok:
            return None
        data = resp.json()
        try:
            page = data["pages"][0]
            return page["title"]
        except Exception:
            return None

    def _fetch_summary(self, title: str) -> Optional[Dict]:
        url = WIKI_SUMMARY_URL.format(title=title.replace(" ", "%20"))
        resp = self.session.get(url, timeout=15, headers={"accept": "application/json"})
        if not resp.ok:
            return None
        return resp.json()

    def _parse_dates_from_extract(self, extract: str) -> Dict[str, Optional[str]]:
        # Simple heuristic: find patterns like (born 1958) or (1901–1976)
        birth_date = None
        death_date = None
        m = re.search(r"\((?:born\s+)?(\d{3,4})(?:\s*[–-]\s*(\d{3,4}))?\)", extract)
        if m:
            birth_date = m.group(1)
            death_date = m.group(2)
        return {"birth_date": birth_date, "death_date": death_date}

    def research(self, name: str) -> ResearchProfile:
        title = self._search_title(name) or name
        summary = self._fetch_summary(title)
        if not summary:
            return ResearchProfile(name=name, description=None, birth_date=None, death_date=None, extract=None, url=None)

        description = summary.get("description")
        extract = summary.get("extract")
        url = summary.get("content_urls", {}).get("desktop", {}).get("page")

        birth_date = summary.get("birth") or None
        death_date = summary.get("death") or None

        # Fallback: heuristic parse if fields missing
        if extract:
            date_guess = self._parse_dates_from_extract(extract)
            birth_date = birth_date or date_guess.get("birth_date")
            death_date = death_date or date_guess.get("death_date")

        return ResearchProfile(
            name=summary.get("title", name),
            description=description,
            birth_date=str(birth_date) if birth_date else None,
            death_date=str(death_date) if death_date else None,
            extract=extract,
            url=url,
        )

