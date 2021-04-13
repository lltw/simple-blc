from mongoengine import Document, ListField, StringField

class UserSubmittedData(Document):
  title = StringField(required=True, max_length=70)
  data_column = ListField(required=True)
  first_digits_column = ListField(required=True)
