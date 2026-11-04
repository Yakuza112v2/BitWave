"""Playlist additions seen during an actual visit, independent of release dates."""
from collections import Counter
import json
import os
from pathlib import Path
import tempfile


class PlaylistVisits:
    def __init__(self, path):
        self.path = Path(path)
        try:
            data = json.loads(self.path.read_text(encoding='utf-8'))
            self.seen = data if isinstance(data, dict) else {}
        except (OSError, ValueError):
            self.seen = {}
        self.visits = {}

    def mark(self, account, playlist, visit, rows, complete=True):
        if not account or not playlist:
            return [False] * len(rows)
        key = json.dumps([str(account), str(playlist)], separators=(',', ':'))
        ids = [str(r.get('kind') or 'track') + ':' + str(r.get('id') or '') for r in rows]
        state = self.visits.get(key)
        if state is None or state[0] != visit:
            old = self.seen.get(key)
            baseline = Counter(old) if isinstance(old, list) and all(isinstance(x, str) for x in old) else None
            state = [visit, baseline]
            self.visits[key] = state
        if state[1] is None:
            # A partial/error result cannot establish or acknowledge a baseline.
            if complete:
                state[1] = Counter(ids)
            flags = [False] * len(ids)
        else:
            occurrence = Counter()
            flags = []
            for identity in ids:
                occurrence[identity] += 1
                flags.append(occurrence[identity] > state[1][identity])
        if complete and self.seen.get(key) != ids:
            self.seen[key] = ids
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=self.path.parent, delete=False) as fh:
                    temporary = fh.name
                    json.dump(self.seen, fh, separators=(',', ':'))
                os.replace(temporary, self.path)
            finally:
                if temporary and os.path.exists(temporary):
                    os.unlink(temporary)
        return flags
