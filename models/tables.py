#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db.define_table('person',
                Field('name', requires=IS_NOT_EMPTY()),
                Field('birthday', 'date', requires=IS_DATE(format=T('%Y-%m-%d'),
                        error_message='must be YYYY-MM-DD!')),
                Field('gender', requires=IS_IN_SET(['Male', 'Female', 'Other'])),
                Field('look_for', requires=IS_IN_SET(['Male', 'Female', 'Other'])),
                Field('email', requires = IS_EMAIL(error_message='invalid email!')),
                Field('password', 'password', requires=IS_NOT_EMPTY()),
                Field('verify_password', 'password', requires=IS_NOT_EMPTY())
                )

# Chat Table
# Will be used to hold chat messages for IMs.
# - Cole
db.define_table('chat',
                Field('sender', requires=IS_NOT_EMPTY()),   # User who sent
                Field('receiver', requires=IS_NOT_EMPTY()), # User who it's to'
                Field('body', requires=IS_NOT_EMPTY()),     # Text in chat message
                Field('seen', requires=IS_NOT_EMPTY()),     # Has it been seen?
                Field('sent', requires=IS_NOT_EMPTY()),# Time it was sent
                )

# Message Table
# Will be used to hold e-mails between two users.
# - Cole
db.define_table('email',
                Field('sender', requires=IS_NOT_EMPTY()),   # User who sent
                Field('receiver', requires=IS_NOT_EMPTY()), # User who it's to'
                Field('body', requires=IS_NOT_EMPTY()),     # Text in chat message
                Field('subject', requires=IS_NOT_EMPTY()),  # Subject of message
                Field('seen', requires=IS_NOT_EMPTY()),     # Has it been seen?
                Field('sent', requires=IS_NOT_EMPTY()),# Time it was sent
                )
