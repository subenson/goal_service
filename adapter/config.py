from adapter.orm import SqlAlchemy


database = SqlAlchemy('sqlite:///test.db')
database.configure_mappings()
database.create_schema()
