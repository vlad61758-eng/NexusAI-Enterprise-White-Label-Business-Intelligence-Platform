import aiosqlite
import logging

logger = logging.getLogger(__name__)

DB_FILE = 'tasks.db'

async def init_db():
    """Initializes the database schema."""
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_link TEXT,
                instructions TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()
    logger.info("Database initialized.")

async def insert_task(source_link: str, instructions: str):
    """Inserts a new task into the database."""
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''
            INSERT INTO tasks (source_link, instructions)
            VALUES (?, ?)
        ''', (source_link, instructions))
        await db.commit()
    logger.info(f"Inserted new task from {source_link}")

async def get_uncompleted_task():
    """Fetches a single uncompleted task."""
    async with aiosqlite.connect(DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('''
            SELECT id, source_link, instructions
            FROM tasks
            WHERE status = 'pending'
            ORDER BY created_at ASC
            LIMIT 1
        ''') as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def mark_task_completed(task_id: int):
    """Marks a task as completed."""
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''
            UPDATE tasks
            SET status = 'completed'
            WHERE id = ?
        ''', (task_id,))
        await db.commit()
    logger.info(f"Task {task_id} marked as completed.")
