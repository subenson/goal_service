from adapter.orm import SqlAlchemy


database = SqlAlchemy('sqlite:////Users/svendenotter/Code/Python/goal_app'
                      '/adapter/test.db')
database.configure_mappings()
database.create_schema()
