

class ModianRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'modian':
            return 'modian'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'modian':
            return 'modian'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'modian' or \
                obj2._meta.app_label == 'modian':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'modian':
            return db == 'modian'
        return None
