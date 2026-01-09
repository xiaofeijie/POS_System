"""
Initialize Database - Create database and tables
"""
from database.schema import init_database


def main():
    """Initialize database"""
    print("Initializing POS System database...")
    db = init_database()
    print("Database initialized successfully!")
    print(f"Database location: data/pos_system.db")


if __name__ == "__main__":
    main()
