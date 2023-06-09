from sqlalchemy import Table


class BaseRepository:
    table: Table

    def get_all(self):
        return self.table.select().execute().fetchall()

    def get_by_id(self, id):
        return self.table.select().where(
            self.table.c.id == id).execute().fetchone()
