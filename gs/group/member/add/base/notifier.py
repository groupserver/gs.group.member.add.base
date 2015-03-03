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
from zope.i18n import translate
from gs.content.email.base import GroupNotifierABC
from gs.profile.notify import MessageSender
from . import GSMessageFactory as _


class Notifier(GroupNotifierABC):
    htmlTemplateName = 'gs-group-member-add-welcome.html'
    textTemplateName = 'gs-group-member-add-welcome.txt'

    def notify(self, adminInfo, userInfo, fromAddr, toAddr, passwordLink):
        subject = _('welcome-subject', 'Welcome to ${groupName}',
                    mapping={'groupName': self.groupInfo.name})
        translatedSubject = translate(subject)
        text = self.textTemplate(adminInfo=adminInfo, userInfo=userInfo)
        html = self.htmlTemplate(adminInfo=adminInfo, userInfo=userInfo,
                                 passwordLink=passwordLink)

        sender = MessageSender(self.context, userInfo)
        sender.send_message(translatedSubject, text, html, fromAddr,
                            [toAddr])
        self.reset_content_type()
