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
import codecs
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.txt"),
                 encoding='utf-8') as f:
    long_description += '\n' + f.read()

setup(name='gs.group.member.add.base',
      version=version,
      description="Add people to a GroupServer group, without an "
                  "invitation",
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          "Environment :: Web Environment",
          "Framework :: Zope2",
          "Intended Audience :: Developers",
          'License :: OSI Approved :: Zope Public License',
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='group, membership, add, group administration',
      author='Michael JasonSmith',
      author_email='mpj17@onlinegroups.net',
      url='https://source.iopen.net/groupserver/gs.group.member.add.base/',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gs', 'gs.group', 'gs.group.member',
                          'gs.group.member.add'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pytz',
          'zope.browserpage',  # For the <browser:page /> ZCML
          'zope.cachedescriptors',
          'zope.component',
          'zope.formlib',
          'zope.interface',
          'zope.tal',
          'zope.tales',
          'zope.viewlet',
          'Zope2',
          'gs.content.email.base',
          'gs.content.email.layout',
          'gs.content.form.base',
          'gs.content.layout',
          'gs.core',
          'gs.group.base',
          'gs.group.member.base',
          'gs.group.member.info',  # For the admin-links
          'gs.group.member.invite.base',
          'gs.group.member.join',
          'gs.group.member.list',
          'gs.group.member.viewlet',
          # The notification has a list of topics
          'gs.group.messages.topic.list',
          'gs.help',
          'gs.profile.email.base',
          'gs.profile.notify',
          'gs.profile.password',
          'Products.CustomUserFolder',
          'Products.GSAuditTrail',
          'Products.GSGroup',
          'Products.GSProfile',
          'Products.XWFCore',
      ],
      entry_points="""# -*- Entry points: -*-
      """,)
