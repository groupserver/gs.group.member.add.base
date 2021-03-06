# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2014, 2015 OnlineGroups.net and Contributors.
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
from __future__ import unicode_literals, absolute_import, print_function
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.i18n import translate
from Products.GSGroupMember.groupmembership import GroupMembers
from gs.content.email.base import GroupEmail, TextMixin
from gs.group.member.list.queries import MembersQuery
from gs.group.messages.topic.list.queries import TopicsQuery
from . import GSMessageFactory as _
UTF8 = 'utf-8'


class WelcomeHTMLNotification(GroupEmail):

    def __init__(self, group, request):
        super(WelcomeHTMLNotification, self).__init__(group, request)
        self.group = group

    @Lazy
    def mailingList(self):
        retval = createObject('groupserver.MailingListInfo', self.group)
        return retval

    @Lazy
    def subj(self):
        retval = '[{}]'.format(self.mailingList.get_property('title', ''))
        return retval

    @Lazy
    def email(self):
        retval = self.mailingList.get_property('mailto', '@')
        return retval

    @Lazy
    def unsub(self):
        body = 'Please remove me from {}.'.format(self.groupInfo.name)
        retval = self.mailto(self.email, 'Unsubscribe', body)
        return retval

    def get_support_email(self, user, admin):
        to = self.siteInfo.get_support_email()
        subj = _('support-email-subject', 'Group welcome')
        subject = translate(subj)
        uu = '{}{}'.format(self.siteInfo.url, user.url)
        au = '{}{}'.format(self.siteInfo.url, admin.url)
        msg = _('support-email-body',
                'Hello,\n\nI was added to the group ${group} by '
                '${adminName}\n and...\n\n'
                '--\nThis technical information may help you:\n'
                '  Group          ${url}\n'
                '  Me             ${userUrl}\n'
                '  Administrator  ${adminUrl}\n',
                mapping={'group': self.groupInfo.name,
                         'url': self.groupInfo.url,
                         'adminName': admin.name,
                         'userUrl': uu, 'adminUrl': au})
        body = translate(msg)
        retval = self.mailto(to, subject, body)
        return retval

    @Lazy
    def topics(self):
        query = TopicsQuery()
        topics = query.recent_non_sitcky_topics(self.siteInfo.id,
                                                self.groupInfo.id, 5, 0)
        retval = [topic['subject'] for topic in topics]
        return retval

    def member_names(self, user, admin):
        '''Get the names of the top-3 posting members, who are not the newly
        added user or the administrator.'''
        q = MembersQuery()
        memberIds = q.posting_authors(self.siteInfo.id, self.groupInfo.id,
                                      6)
        try:
            memberIds.remove(admin.id)
        except ValueError:
            pass
        try:
            memberIds.remove(user.id)
        except ValueError:
            pass

        members = GroupMembers(self.context)
        names = [members.getTermByToken(m).title for m in memberIds
                 if (m and (m in members))]
        retval = names[:3]
        return retval


class WelcomeTXTNotification(WelcomeHTMLNotification, TextMixin):

    def __init__(self, group, request):
        super(WelcomeTXTNotification, self).__init__(group, request)
        filename = 'welcome-to-{0}-{1}.txt'.format(self.siteInfo.id,
                                                   self.groupInfo.id)
        self.set_header(filename)
