"""
Database Connection - SQLite database connection management
"""
import sqlite3
import os
from contextlib import contextmanager
from typing import Optional


class DatabaseConnection:
    """Database connection manager for SQLite"""
    
    def __init__(self, db_path: str = "data/pos_system.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self._ensure_data_dir()
        self._ensure_database()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _ensure_database(self):
        """Ensure database file exists"""
        if not os.path.exists(self.db_path):
            # Database will be created when connection is established
            conn = self.get_connection()
            conn.close()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def execute(self, query: str, params: tuple = ()):
        """Execute a single query"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def execute_many(self, query: str, params_list: list):
        """Execute a query multiple times"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return cursor
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """Fetch one row"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        finally:
            conn.close()
    
    def fetch_all(self, query: str, params: tuple = ()) -> list:
        """Fetch all rows"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            conn.close()
