# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import unicode_literals
from urllib import quote
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.GSGroupMember.groupmembership import GroupMembers
from gs.content.email.base import GroupEmail, TextMixin
from gs.group.member.list.queries import MembersQuery
from gs.group.messages.topics.queries import TopicsQuery
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
        m = 'mailto:{to}?Subject=Unsubscribe&body={body}'
        retval = m.format(to=self.email, body=quote(body.encode(UTF8)))
        return retval

    def get_support_email(self, user, admin):
        subj = 'Group Welcome'
        uu = '{}{}'.format(self.siteInfo.url, user.url)
        au = '{}{}'.format(self.siteInfo.url, admin.url)
        msg = 'Hello,\n\nI was added to the group {group} by {adminName}\n'\
                'and...\n\n--\nThis technical information may help you:\n  '\
                'Group          {url}\n  Me             {userUrl}\n  '\
                'Administrator  {adminUrl}\n'
        body = msg.format(group=self.groupInfo.name, url=self.groupInfo.url,
                                adminName=admin.name, userUrl=uu, adminUrl=au)
        m = 'mailto:{to}?Subject={subj}&body={body}'
        retval = m.format(to=self.email, subj=quote(subj),
                            body=quote(body.encode(UTF8)))
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
        memberIds = q.posting_authors(self.siteInfo.id, self.groupInfo.id, 6)
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

    def format_message(self, m):
        retval = self.fill(m)
        return retval
