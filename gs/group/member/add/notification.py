# -*- coding: utf-8 -*-
from urllib import quote
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.group.base import GroupPage
UTF8 = 'utf-8'


class WelcomeHTMLNotification(GroupPage):

    def __init__(self, group, request):
        super(WelcomeHTMLNotification, self).__init__(group, request)

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
        body = u'Please remove me from {}.'.format(self.groupInfo.name)
        m = 'mailto:{to}?Subject=Unsubscribe&body={body}'
        retval = m.format(to=self.email, body=quote(body.encode(UTF8)))
        return retval

    def get_support_email(self, user, admin):
        subj = 'Group Welcome'
        uu = '{}{}'.format(self.siteInfo.url, user.url)
        au = '{}{}'.format(self.siteInfo.url, admin.url)
        msg = u'Hello,\n\nI was added to the group {group} by {adminName}\n'\
                u'and...\n\n--\nThis technical information may help you:\n  '\
                u'Group          {url}\n  Me             {userUrl}\n  '\
                u'Administrator  {adminUrl}\n'
        body = msg.format(group=self.groupInfo.name, url=self.groupInfo.url,
                                adminName=admin.name, userUrl=uu, adminUrl=au)
        m = 'mailto:{to}?Subject={subj}&body={body}'
        retval = m.format(to=self.email, subj=quote(subj),
                            body=quote(body.encode(UTF8)))
        return retval


class WelcomeTXTNotification(WelcomeHTMLNotification):

    def __init__(self, group, request):
        super(WelcomeTXTNotification, self).__init__(group, request)