# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
from random import randint
import datetime

dateTips =  [   "You miss 100% of the shots you don't take... [Wayne Gretzky]",
                "Shit happens... [Life]",
                "A fluke is one of the most common fish in the sea, so if you go fishing for a fluke, chances are you just might catch one... [Kevin Malone]",
                "To find a prince, you gotta kiss some toads... [Foxy Brown]",
                "You must search well enough, to find the answers... [Lailah Gifty Akita]",
                "To live, to TRULY live, we must be willing to RISK... [Mandy Hale]", 
                "It's hard to believe in coincidence, but it's even harder to believe in anything else... [John Green]",
                "The doors will be opened to those who are bold enough to knock...",
                "Life has no remote. Get up and change it yourself...",
                "All glory comes from a daring to begin...",
                "You are not born a winner; you are not born a loser. You are born a chooser...",
                "Now is your chance to make a move!",
            ]

profTips =  [   "People see your picture before hellos. Be sure to take a good picture!",
                "Keep it simple and mysterious!",
                "What most interests you? What are your hobbies?",
                "Don't leave your profile empty!",
            ]

def index():
    #display
    profile = db().select(db.person.user_id, db.person.image, db.person.your_name, db.person.college, db.person.birthday, db.person.seeking_a, db.person.gender)
    myprofile = db(db.person.user_id == auth.user).select()
    prefs = db(db.pref.user_id == auth.user).select()
    return dict(myprofile=myprofile, form=auth(), profile=profile, prefs=prefs)

def matches():
    thisprofile = db(db.person.user_id == auth.user).select()
    matches = db.select(db.person.seeking_a == this.profile.gender)
    return dict(thisprofile=thisprofile, matches=matches)

def messages():
    return dict()

def get_messages():
    '''This will return all emails that the user has sent or received -cole '''
    rec_rows = db(db.email.receiver==auth.user_id).select(orderby=db.email.sent)

    d1 = {r.message_id: {
        'sender':r.sender,
        'receiver':r.receiver,
        'body':r.body,
        'subject':r.subject,
        'seen':r.seen,
        'message_id':r.message_id,
        'sent':r.sent}
          for r in rec_rows}

    sent_rows = db(db.email.sender==auth.user_id).select(orderby=db.email.sent)

    d2 = {r.message_id: {
        'sender':r.sender,
        'receiver':r.receiver,
        'body':r.body,
        'subject':r.subject,
        'seen':r.seen,
        'message_id':r.message_id,
        'sent':r.sent }
          for r in sent_rows}

    return response.json(dict(rec_messages=d1, sent_messages=d2))


def send_message():
    '''Sends a new message '''
    db.email.update_or_insert((db.email.message_id == request.vars.message_id),
            message_id=request.vars.message_id,
            sender=auth.user_id,
            receiver=request.vars.receiver,
            body=request.vars.body,
            subject=request.vars.subject,
            seen=False,
            sent=datetime.datetime.now())
    return "ok"

def chat():
    '''This will return all chats that the user has sent or received -cole '''
    recChats = db(db.chat.receiver==auth.user_id).select()
    sentChats = db(db.chat.sender==auth.user_id).select()
    return dict(sentChats=sentChats, recChats=recChats)

def settings():
    profile = db(db.pref.user_id == auth.user).select().first()
    print profile
    form = SQLFORM(db.pref,
                   fields=[
                        'male',
                        'female',
                        'Porter',
                        'Kresge',
                        'Merrill',
                        'Crown',
                        'Oakes',
                        'Cowell',
                        'Stevenson',
                        'Eight',
                        'Nine',
                        'Ten',
                   ],

                   record=profile
                   )
    form.vars.setdefault('user_id', auth.user)
    if form.process().accepted:
        session.flash = T('Your settings have been updated')
        redirect(URL('default', 'settings'))
    return dict(form=form)

def myprofile():
    thisprofile = db(db.person.user_id == auth.user).select()
    if db.person.user_id.validate(auth.user)[1] != None:
        session.flash = T('You have to update your profile first!')
        redirect(URL('editprofile'))
    return dict(thisprofile=thisprofile)

def profile():
    profile_id = db.person(request.args(0))
    thisprofile = db(db.person.user_id == profile_id).select()
    thumb_profile = db(db.rating.user_id == profile_id).select()

    def get_thumbs(profileindex):
        if not auth.user_id:
            return None
        r = db((db.rating.user_id == auth.user_id) & (db.rating.profile_id == profileindex)).select().first()
        return None if r is None else r.thumbs

    user_list = []
    for i, user_lst in enumerate(thisprofile):
        user_list.append(dict(
        url= user_lst,
        thumbs = get_thumbs(i),
        id=i,
    ))

    return dict(thisprofile=thisprofile, thumb_profile=thumb_profile, user_list=user_list)

@auth.requires_signature()
def vote():
    picid = int(request.vars.picid)
    thumbs = request.vars.thumbs
    db.rating.update_or_insert(
        ((db.rating.profile_id == picid) & (db.rating.user_id == auth.user_id)),
        profile_id = picid,
        user_id = auth.user_id,
        thumbs = thumbs
    )
    return "ok"


def editprofile():
    profile = db(db.person.user_id == auth.user).select().first()
    print profile
    form = SQLFORM(db.person,
                   fields=[
                       'image',
                       'your_name',
                       'birthday',
                       'gender',
                       'seeking_a',
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
    return dict(form=form)

#JOSH'S TIP SECTION YAY.
def loadTips():
    """
    0 = profile tips
    1 = dating tips
    """
    if request.args(0) is "0":
        return response.json(dict(tip_dict=profTips))
    else:
        return response.json(dict(tip_dict=dateTips))


def selRandTip():
    """
    0 = profile tips
    1 = dating tips
    """
    if request.args(0) is "0":
        x = randint(0, len(profTips)-1)
        return profTips[x]
    else:
        x = randint(0, len(dateTips)-1)
        return dateTips[x]



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
