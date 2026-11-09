"""Database connection and raw SQL execution module.

Uses psycopg for PostgreSQL when available/configured, with automatic fallback
to SQLite for offline local demo runs so the app never fails on systems
without an active PostgreSQL service.
"""

import os
import sqlite3
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/pink_wheels")

# Flag indicating whether we are connected to Postgres or SQLite
_use_postgres = False
_pg_conn = None


def get_db_connection():
    """Returns a direct database connection."""
    global _use_postgres, _pg_conn
    
    # Try PostgreSQL if URL starts with postgresql
    if DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://"):
        try:
            import psycopg
            from psycopg.rows import dict_row
            conn = psycopg.connect(DATABASE_URL, row_factory=dict_row, connect_timeout=2)
            _use_postgres = True
            return conn
        except Exception:
            # PostgreSQL server not reachable locally; fall back to SQLite
            _use_postgres = False

    # Fallback: SQLite with dictionary cursor
    db_path = os.path.join(os.path.dirname(__file__), "pink_wheels_dsa.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Execute a SELECT query and return rows as list of dicts."""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        # Adapt parameter placeholders if needed (%s for postgres, ? for sqlite)
        if not _use_postgres:
            query = query.replace("%s", "?")
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        # Convert sqlite3.Row to dict
        if not _use_postgres:
            return [dict(r) for r in rows]
        return [dict(r) for r in rows]
    finally:
        conn.close()


def execute_commit(query: str, params: tuple = ()) -> int:
    """Execute an INSERT, UPDATE, or DELETE query and return lastrowid / affected count."""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        if not _use_postgres:
            query = query.replace("%s", "?")
        cur.execute(query, params)
        conn.commit()
        last_id = getattr(cur, "lastrowid", None)
        cur.close()
        return last_id or 0
    finally:
        conn.close()


def init_db():
    """Initialize necessary tables for passengers and rides."""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        # 1. Passengers table
        if _use_postgres:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS passengers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    phone VARCHAR(50) NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rides (
                    id SERIAL PRIMARY KEY,
                    passenger_id INTEGER,
                    driver_id INTEGER,
                    pickup_location TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    pickup_latitude DOUBLE PRECISION NOT NULL,
                    pickup_longitude DOUBLE PRECISION NOT NULL,
                    destination_latitude DOUBLE PRECISION NOT NULL,
                    destination_longitude DOUBLE PRECISION NOT NULL,
                    distance_km DOUBLE PRECISION DEFAULT 0.0,
                    fare DOUBLE PRECISION DEFAULT 0.0,
                    vehicle_type VARCHAR(50) DEFAULT 'Bike',
                    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        else:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS passengers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rides (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    passenger_id INTEGER,
                    driver_id INTEGER,
                    pickup_location TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    pickup_latitude REAL NOT NULL,
                    pickup_longitude REAL NOT NULL,
                    destination_latitude REAL NOT NULL,
                    destination_longitude REAL NOT NULL,
                    distance_km REAL DEFAULT 0.0,
                    fare REAL DEFAULT 0.0,
                    vehicle_type TEXT DEFAULT 'Bike',
                    status TEXT NOT NULL DEFAULT 'PENDING',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
            """)

        conn.commit()
        
        # Seed default demo passenger if table is empty
        count_query = "SELECT COUNT(*) as c FROM passengers"
        cur.execute(count_query)
        row = cur.fetchone()
        count = row["c"] if isinstance(row, dict) else row[0]
        if count == 0:
            if _use_postgres:
                cur.execute("INSERT INTO passengers (name, phone) VALUES (%s, %s)", ("Fatima Noor", "+92 300 1234567"))
                cur.execute("INSERT INTO passengers (name, phone) VALUES (%s, %s)", ("Ayesha Khan", "+92 321 7654321"))
                cur.execute("INSERT INTO passengers (name, phone) VALUES (%s, %s)", ("Zainab Ali", "+92 333 9876543"))
            else:
                cur.execute("INSERT INTO passengers (name, phone) VALUES (?, ?)", ("Fatima Noor", "+92 300 1234567"))
                cur.execute("INSERT INTO passengers (name, phone) VALUES (?, ?)", ("Ayesha Khan", "+92 321 7654321"))
                cur.execute("INSERT INTO passengers (name, phone) VALUES (?, ?)", ("Zainab Ali", "+92 333 9876543"))
            conn.commit()

        cur.close()
    finally:
        conn.close()
