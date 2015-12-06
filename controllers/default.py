# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    #display
    return dict(form = auth())

def matches():

    return dict()

def messages():

    return dict()

def profile():
    profile = db.person
    return dict(profile=profile)


def editprofile():
    profile = db.person
    form = SQLFORM(db.person, record=profile)
    if form.process().accepted:
        session.flash = T('Your profile has been updated')
        redirect(URL('default', 'editprofile'))
    return dict(form=form)



    """form = SQLFORM(db.person)
    if form.process().accepted:
        logger.info("Form Accepted")
        redirect(URL('default', 'index'))
    elif form.errors:
        response.flash = "Form has errors"
    
    return dict(form = form)"""

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
    db(db.person.id > 0).delete()