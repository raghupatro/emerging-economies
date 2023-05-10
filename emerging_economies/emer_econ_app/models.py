from django.db import models

class Database(models.Model):
    database = models.JSONField()
    database_refresh_date = models.DateTimeField()

    def __str__(self):
        return "database : "+str(self.database_refresh_date)