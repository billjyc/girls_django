

class MemberRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'snh48':
            return 'snh48'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'snh48':
            return 'snh48'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'snh48' or \
                obj2._meta.app_label == 'snh48':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'snh48':
            return db == 'snh48'
        return None
