# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
from random import randint
tip_list =   [   "You miss 100% of the shots you don't take. -Wayne Gretzky",
            "Shit happens. -Life",
            "A fluke is one of the most common fish in the sea, so if you go fishing for a fluke, chances are you just might catch one. -Kevin Malone",
        ]

def index():
    #display
    profile = db().select(db.person.user_id, db.person.image)
    return dict(form = auth(), profile=profile, tip=selRandTip(tip_list))

def matches():

    return dict()

def messages():
    '''This will return all emails that the user has sent or received -cole '''
    recMessages = db(db.email.receiver==auth.user_id).select()
    sentMessages = db(db.email.sender==auth.user_id).select()
    return dict(recMessages=messages, sentMessages = sentMessages, tip=selRandTip(tip_list))

def chat():
    '''This will return all chats that the user has sent or received -cole '''
    recChats = db(db.chat.receiver==auth.user_id).select()
    sentChats = db(db.chat.sender==auth.user_id).select()
    return dict(sentChats=sentChats, recChats=recChats)

def settings():
    return dict()

def myprofile():
    thisprofile = db(db.person).select()
    if thisprofile is None:
        session.flash = T('You have to update your profile first!')
        redirect(URL('default'))
    return dict(thisprofile=thisprofile, tip=selRandTip(tip_list))

def profile():
    profile = db.person
    return dict(profile=profile, tip=selRandTip(tip_list))


def editprofile():
    profile = db(db.person.user_id == auth.user).select().first()
    print profile
    form = SQLFORM(db.person,
                   fields=[
                       'image',
                       'about_me',
                       'interests',
                       'major',
                       'college'
                   ],
                   record=profile)
    form.vars.setdefault('user_id', auth.user)
    if form.process().accepted:
        session.flash = T('Your profile has been updated')
        redirect(URL('default', 'editprofile'))
    return dict(form=form, tip=selRandTip(tip_list))


def tips():
    return dict(tip_list=tip_list)


def selRandTip(tip_list):
    x = randint(0, len(tip_list)-1)
    return tip_list[x]



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


def reset_db():
    db.person.truncate()
    db.chat.truncate()
    db.email.truncate()
    db.auth_user.truncate()
    db.commit()
    return "ok"

def drop_db():
    db.person.drop()
    db.chat.drop()
    db.email.drop()
    db.commit()
    return "ok"
