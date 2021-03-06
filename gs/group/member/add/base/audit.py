# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import unicode_literals
from pytz import UTC
from datetime import datetime
from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy
from Products.CustomUserFolder.userinfo import userInfo_to_anchor
from Products.GSGroup.groupInfo import groupInfo_to_anchor
from Products.GSAuditTrail import (IAuditEvent, BasicAuditEvent,
                                   AuditQuery, event_id_from_data)

SUBSYSTEM = 'gs.group.member.add'
import logging
log = logging.getLogger(SUBSYSTEM)

UNKNOWN = '0'
ADD_NEW_USER = '1'
ADD_OLD_USER = '2'
ADD_EXISTING_MEMBER = '3'


class AuditEventFactory(object):
    implements(IFactory)

    title = 'User Profile Add Audit-Event Factory'
    description = 'Creates a GroupServer audit event for user add'

    def __call__(self, context, event_id, code, date, userInfo,
                 instanceUserInfo, siteInfo, groupInfo, instanceDatum='',
                 supplementaryDatum='', subsystem=''):

        if (code == ADD_NEW_USER):
            event = AddNewUserEvent(context, event_id, date, userInfo,
                                    instanceUserInfo, siteInfo, groupInfo,
                                    instanceDatum, supplementaryDatum)
        elif (code == ADD_OLD_USER):
            event = AddOldUserEvent(context, event_id, date, userInfo,
                                    instanceUserInfo, siteInfo, groupInfo,
                                    instanceDatum, supplementaryDatum)
        elif (code == ADD_EXISTING_MEMBER):
            event = AddExistingMemberEvent(context, event_id, date,
                                           userInfo, instanceUserInfo,
                                           siteInfo, groupInfo,
                                           instanceDatum,
                                           supplementaryDatum)
        else:
            event = BasicAuditEvent(context, event_id, UNKNOWN, date,
                                    userInfo, instanceUserInfo, siteInfo,
                                    groupInfo, instanceDatum,
                                    supplementaryDatum, SUBSYSTEM)
        assert event
        return event

    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)


class AddNewUserEvent(BasicAuditEvent):
    """Administrator adding a New User Event.

    The "instanceDatum" is the address used to create the new user.
    """
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, instanceUserInfo, siteInfo,
                 groupInfo, instanceDatum, supplementaryDatum):

        BasicAuditEvent.__init__(self, context, id, ADD_NEW_USER, d,
                                 userInfo, instanceUserInfo, siteInfo,
                                 groupInfo, instanceDatum,
                                 supplementaryDatum, SUBSYSTEM)

    def __unicode__(self):
        r = 'Administrator {0} ({1}) adding a new user {2} ({3}) '\
            'with address <{4}> to join {5} ({6}) on {7} ({8})'
        retval = r.format(self.userInfo.name, self.userInfo.id,
                          self.instanceUserInfo.name,
                          self.instanceUserInfo.id, self.instanceDatum,
                          self.groupInfo.name, self.groupInfo.id,
                          self.siteInfo.name, self.siteInfo.id)
        return retval

    @property
    def xhtml(self):
        cssClass = 'audit-event profile-add-event-{0}'.format(self.code)
        email = '<code class="email">{}</code>'.format(self.instanceDatum)
        m = '<span class="{cssClass}">Adding the new user {user} (with '\
            'the email address {email}) to join {group}.</span>'
        retval = m.format(cssClass=cssClass, email=email,
                          user=userInfo_to_anchor(self.instanceUserInfo),
                          group=groupInfo_to_anchor(self.groupInfo))
        if ((self.instanceUserInfo.id != self.userInfo.id)
                and not(self.userInfo.anonymous)):
            u = userInfo_to_anchor(self.userInfo)
            retval = '{0} &#8212; {1}'.format(retval, u)
        return retval


class AddOldUserEvent(BasicAuditEvent):
    """Administrator adding an old User Event.

    The "instanceDatum" is the address used to match the old user.
    """
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, instanceUserInfo,
                 siteInfo, groupInfo, instanceDatum, supplementaryDatum):

        BasicAuditEvent.__init__(self, context, id,
          ADD_OLD_USER, d, userInfo, instanceUserInfo,
          siteInfo, groupInfo, instanceDatum, supplementaryDatum,
          SUBSYSTEM)

    def __unicode__(self):
        retval = 'Administrator %s (%s) adding an existing user '\
                  '%s (%s) with address <%s> to join %s (%s) on %s (%s)' %\
          (self.userInfo.name, self.userInfo.id,
          self.instanceUserInfo.name, self.instanceUserInfo.id,
          self.instanceDatum,
          self.groupInfo.name, self.groupInfo.id,
          self.siteInfo.name, self.siteInfo.id)
        return retval

    @property
    def xhtml(self):
        cssClass = 'audit-event profile-add-event-{}'.format(self.code)
        m = '<span class="{cssClass}">Adding the existing user {user} '\
            'to {group}</span>'
        retval = m.format(cssClass=cssClass,
                            user=userInfo_to_anchor(self.instanceUserInfo),
                            group=groupInfo_to_anchor(self.groupInfo))
        if ((self.instanceUserInfo.id != self.userInfo.id)
            and not(self.userInfo.anonymous)):
            retval = '{} &#8212; {}'.format(retval,
                                            userInfo_to_anchor(self.userInfo))
        return retval


class AddExistingMemberEvent(BasicAuditEvent):
    """Administrator Adding an Existing Group Member.

    The "instanceDatum" is the address used to match the existing group
    member.
    """
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, instanceUserInfo,
        siteInfo, groupInfo, instanceDatum, supplementaryDatum):

        BasicAuditEvent.__init__(self, context, id,
          ADD_OLD_USER, d, userInfo, instanceUserInfo,
          siteInfo, groupInfo, instanceDatum, supplementaryDatum,
          SUBSYSTEM)

    def __unicode__(self):
        retval = 'Administrator %s (%s) tried to add an existing '\
                  'group member %s (%s) with address <%s> to join %s (%s) '\
                  'on %s (%s)' %\
          (self.userInfo.name, self.userInfo.id,
          self.instanceUserInfo.name, self.instanceUserInfo.id,
          self.instanceDatum,
          self.groupInfo.name, self.groupInfo.id,
          self.siteInfo.name, self.siteInfo.id)
        return retval

    @property
    def xhtml(self):
        cssClass = 'audit-event profile-add-event-%s' % self.code
        retval = '<span class="%s">Tried to add the existing member '\
            ' %s to join %s.</span>' %\
            (cssClass, userInfo_to_anchor(self.instanceUserInfo),
            groupInfo_to_anchor(self.groupInfo))
        if ((self.instanceUserInfo.id != self.userInfo.id)
            and not(self.userInfo.anonymous)):
            retval = '%s &#8212; %s' %\
              (retval, userInfo_to_anchor(self.userInfo))
        return retval


class Auditor(object):
    def __init__(self, siteInfo, groupInfo, adminInfo, userInfo):
        self.siteInfo = siteInfo
        self.groupInfo = groupInfo
        self.adminInfo = adminInfo
        self.userInfo = userInfo

        self.queries = AuditQuery()

        self.factory = AuditEventFactory()

    def info(self, code, instanceDatum='', supplementaryDatum=''):
        d = datetime.now(UTC)
        eventId = event_id_from_data(self.adminInfo, self.userInfo,
            self.siteInfo, code, instanceDatum, supplementaryDatum)

        e = self.factory(self.userInfo.user, eventId, code, d,
                self.adminInfo, self.userInfo, self.siteInfo,
                self.groupInfo, instanceDatum, supplementaryDatum,
                SUBSYSTEM)

        self.queries.store(e)
        log.info(e)
