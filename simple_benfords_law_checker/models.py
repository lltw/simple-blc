from mongoengine import *


class CurrentUserFile(Document):

    file_id = UUIDField(required=True, primary_key=True)
    filename = StringField(required=True)
    file_path = StringField(required=True)
    data_column = ListField(FloatField(), required=True, default=list)
    are_errors_present = BooleanField(required=True)
    no_lines = IntField(required=True)
    no_ncol_err = IntField(required=True)
    no_val_err = IntField(required=True)
    ncol_err_rows_nums = ListField(IntField(), default=list)
    val_err_rows_nums = ListField(IntField(), default=list)

    @classmethod
    def get_by_file_id(cls, file_id):
        return cls.objects.with_id(file_id)

    meta = {'collection': 'current_user_files'}


class UserSubmittedData(Document):

    data_column = ListField(FloatField(), required=True, default=list)

    meta = {'collection': 'user_submitted_data'}


