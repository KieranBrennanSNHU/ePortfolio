import sqlite3
import json
import csv
import re
from typing import Optional, Dict, Any, Iterable


class AnimalShelter(object):
    """SQLite-backed AnimalShelter CRUD helper.
    This class provides methods to create, read, update, and delete records in a SQLite database."""

    records_updated = 0
    records_matched = 0
    records_deleted = 0

    def __init__(self, _password: Optional[str] = None, _username: str = 'aacUser', db_path: str = 'animal_shelter_sql', table: str = 'animals'):
        # signature kept compatible with previous MongoDB version
        # _password and _username are ignored for SQLite, kept for compatibility
        self.db_path = db_path
        self.table = table
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._ensure_table()
        self.table_columns = self._get_table_columns()
        self.column_mode = self._detect_column_mode()
        self.column_name_map = {
            'age_upon_outcome': 'age upon outcome',
            'animal_id': 'animal id',
            'animal_type': 'animal type',
            'date_of_birth': 'date of birth',
            'datetime': 'date time',
            'monthyear': 'month year',
            'outcome_subtype': 'outcome subtype',
            'outcome_type': 'outcome type',
            'sex_upon_outcome': 'sex upon outcome',
            'location_lat': 'location lat',
            'location_long': 'location long',
            'age_upon_outcome_in_weeks': 'age upon outcome in weeks',
        }

    def _get_table_columns(self) -> list[str]:
        cur = self.conn.cursor()
        cur.execute(f"PRAGMA table_info({self.table})")
        rows = cur.fetchall()
        return [row['name'] for row in rows]

    def _detect_column_mode(self) -> bool:
        # Use explicit SQL columns if the table has more than just id and data
        if 'data' not in self.table_columns:
            return True
        return len([c for c in self.table_columns if c not in ('id', 'data')]) > 0

    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        if self.column_mode:
            obj = {k: row[k] for k in row.keys() if k != 'id'}
            obj['_id'] = row['id']
            return obj

    def _normalize_csv_key(self, key: str) -> str:
        key = key.strip()
        if key in self.column_name_map:
            return self.column_name_map[key]
        if key.replace('_', ' ') in self.table_columns:
            return key.replace('_', ' ')
        return key

        obj = json.loads(row['data'])
        obj['_id'] = row['id']
        return obj

    def load_from_csv(self, csv_path: str = 'aac_shelter_outcomes.csv') -> int:
        """Load records from a CSV file into the SQLite `animals` table.

        Returns the number of records inserted.
        """
        inserted = 0
        try:
            with open(csv_path, newline='', encoding='utf-8') as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    # coerce empty strings to None and attempt numeric casts
                    clean = {}
                    for k, v in row.items():
                        mapped_key = self._normalize_csv_key(k)
                        if self.column_mode and mapped_key not in self.table_columns:
                            continue
                        if v is None or v == '':
                            clean[mapped_key] = None
                            continue
                        # try int then float
                        try:
                            iv = int(v)
                            clean[mapped_key] = iv
                            continue
                        except Exception:
                            pass
                        try:
                            fv = float(v)
                            clean[mapped_key] = fv
                            continue
                        except Exception:
                            pass
                        clean[mapped_key] = v

                    if self.createRecord(clean):
                        inserted += 1
        except FileNotFoundError:
            raise
        return inserted

    def _ensure_table(self):
        cur = self.conn.cursor()
        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def createRecord(self, data: Dict[str, Any]) -> bool:
        if not data or not isinstance(data, dict):
            raise Exception("No document to save. Data is empty or not a dict.")

        cur = self.conn.cursor()
        if self.column_mode:
            insert_keys = [k for k in data.keys() if k in self.table_columns and k != 'id']
            if not insert_keys:
                raise Exception("No valid columns found for insert.")
            columns = ','.join(f'"{k}"' for k in insert_keys)
            placeholders = ','.join('?' for _ in insert_keys)
            values = [data[k] for k in insert_keys]
            cur.execute(f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})", values)
        else:
            payload = json.dumps(data)
            cur.execute(f"INSERT INTO {self.table} (data) VALUES (?)", (payload,))
        self.conn.commit()
        return cur.lastrowid is not None

    def getRecordId(self, postId: int) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        if self.column_mode:
            cur.execute(f"SELECT * FROM {self.table} WHERE id = ?", (postId,))
        else:
            cur.execute(f"SELECT id, data FROM {self.table} WHERE id = ?", (postId,))
        row = cur.fetchone()
        if not row:
            return None
        return self._row_to_dict(row)

    def getRecordCriteria(self, criteria: Optional[Dict[str, Any]] = None) -> Iterable[Dict[str, Any]]:
        cur = self.conn.cursor()
        if self.column_mode:
            cur.execute(f"SELECT * FROM {self.table}")
        else:
            cur.execute(f"SELECT id, data FROM {self.table}")
        rows = cur.fetchall()
        for r in rows:
            obj = self._row_to_dict(r)
            if criteria:
                if not self._matches(obj, criteria):
                    continue
            yield obj

    def _matches(self, obj: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """Check if a record `obj` matches the provided `criteria`.

        Supports a small subset of Mongo-like operators used in the notebook:
        - $or: list of criteria dicts
        - $regex: compiled or string regex
        - $gte, $lte: numeric comparisons
        - $in: membership check
        Exact matches for scalar values are supported.
        """
        for key, cond in criteria.items():
            if key == '$or' and isinstance(cond, list):
                if not any(self._matches(obj, c) for c in cond):
                    return False
                continue

            # if condition is a dict, interpret operators
            if isinstance(cond, dict):
                # $regex
                if '$regex' in cond:
                    pattern = cond['$regex']
                    val = obj.get(key)
                    if val is None:
                        return False
                    if isinstance(pattern, re.Pattern):
                        if not pattern.search(str(val)):
                            return False
                    else:
                        # treat as string pattern
                        if not re.search(str(pattern), str(val)):
                            return False
                    continue

                # range queries
                if '$gte' in cond or '$lte' in cond:
                    val = obj.get(key)
                    if val is None:
                        return False
                    try:
                        num = float(val)
                    except Exception:
                        return False
                    if '$gte' in cond and num < float(cond['$gte']):
                        return False
                    if '$lte' in cond and num > float(cond['$lte']):
                        return False
                    continue

                # $in operator
                if '$in' in cond:
                    val = obj.get(key)
                    if val not in cond['$in']:
                        return False
                    continue

                # nested exact matches
                matched = True
                for subk, subv in cond.items():
                    if obj.get(subk) != subv:
                        matched = False
                        break
                if not matched:
                    return False
                continue

            # direct equality
            if obj.get(key) != cond:
                return False

        return True

    def updateRecord(self, query: Dict[str, Any], newValue: Dict[str, Any]) -> bool:
        if not query:
            raise Exception("No search criteria is present.")
        if not newValue:
            raise Exception("No update value is present.")

        cur = self.conn.cursor()
        matched_ids = []
        for rec in self.getRecordCriteria(query):
            matched_ids.append(rec['_id'])

        self.records_matched = len(matched_ids)
        updated = 0
        for _id in matched_ids:
            if self.column_mode:
                cur.execute(f"SELECT * FROM {self.table} WHERE id = ?", (_id,))
                row = cur.fetchone()
                if not row:
                    continue
                obj = self._row_to_dict(row)
                obj.update(newValue)
                update_keys = [k for k in obj.keys() if k != '_id' and k in self.table_columns]
                if not update_keys:
                    continue
                set_clause = ', '.join(f'"{k}" = ?' for k in update_keys)
                values = [obj[k] for k in update_keys] + [_id]
                cur.execute(f"UPDATE {self.table} SET {set_clause} WHERE id = ?", values)
            else:
                cur.execute(f"SELECT data FROM {self.table} WHERE id = ?", (_id,))
                row = cur.fetchone()
                if not row:
                    continue
                obj = json.loads(row['data'])
                obj.update(newValue)
                cur.execute(f"UPDATE {self.table} SET data = ? WHERE id = ?", (json.dumps(obj), _id))
            updated += 1

        self.conn.commit()
        self.records_updated = updated
        return updated > 0

    def deleteRecord(self, query: Dict[str, Any]) -> bool:
        if not query:
            raise Exception("No search criteria is present.")

        cur = self.conn.cursor()
        matched_ids = []
        for rec in self.getRecordCriteria(query):
            matched_ids.append(rec['_id'])

        deleted = 0
        for _id in matched_ids:
            cur.execute(f"DELETE FROM {self.table} WHERE id = ?", (_id,))
            deleted += cur.rowcount

        self.conn.commit()
        self.records_deleted = deleted
        return deleted > 0


if __name__ == '__main__':
    # Small interactive test block demonstrating usage.
    shelter = AnimalShelter()

    sample = {"name": "Rex", "age_upon_outcome": "2 months", "type": "Dog"}
    print('Create:', shelter.createRecord(sample))

    # get all
    print('All records:')
    for r in shelter.getRecordCriteria(None):
        print(r)

    # update
    q = {"name": "Rex"}
    shelter.updateRecord(q, {"adopted": True})
    print('Updated:', shelter.records_updated, 'Matched:', shelter.records_matched)

    # delete
    shelter.deleteRecord({"name": "Rex"})
    print('Deleted:', shelter.records_deleted)