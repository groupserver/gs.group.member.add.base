Changelog
=========

3.3.3 (2015-09-15)
------------------

* [DE] Updating the German translation, thanks to Cousin Clara
* [EN] ``s/Dear/Hello/g`` in the *Welcome* notification
* Using the actual support email address, rather than the group
  email address, in the HTML form of the *Welcome* notification,
  thanks to Paul for spotting that

3.3.2 (2015-03-30)
------------------

* Fixing the feedback text on the *Add a member* page

3.3.1 (2015-03-11)
------------------

* [FR] Adding a French translation, thanks to `Razique Mahroua`_

.. _Razique Mahroua: https://www.transifex.com/accounts/profile/Razique/

3.3.0 (2015-03-03)
------------------

* Added internationalisation support
* Adding support for Transifex_
* Following the rename of `gs.group.messages.topic.list`_ from
  ``gs.group.messages.topics``
* Naming the reStructuredText files as such
* Switching to GitHub_ as the primary source-code repository

.. _Transifex:
   https://www.transifex.com/projects/p/gs-group-member-add-base/
.. _gs.group.messages.topic.list:
   https://github.com/groupserver/gs.group.messages.topic.list
.. _GitHub:
   https://github.com/groupserver/gs.group.member.add.base

3.2.0 (2014-06-13)
------------------

* Following the rename `gs.content.form.base` from
  ``gs.content.form``

.. _gs.content.form.base:
   https://github.com/groupserver/gs.content.form.base

3.1.2 (2014-04-25)
------------------

* Metadata update

3.1.1 (2014-02-28)
------------------

* Ensuring the content-type header is reset after sending the
  notifications

3.1.0 (2014-02-20)
------------------

* Switching the base-class of the notifications to those supplied
  by `gs.content.email.base`_

.. _gs.content.email.base:
   https://github.com/groupserver/gs.content.email.base

3.0.2 (2014-02-11)
------------------

* Encoding the text-headers as ASCII strings

3.0.1 (2014-01-30)
------------------

* Verify the address when adding, closing `Bug 4037`_
* Sanitising the email address
* Switching to Unicode literals

.. _Bug 4037: https://redmine.iopen.net/issues/4037

3.0.0 (2014-01-08)
------------------

* Changing the name of the product to `gs.group.member.add.base`_
  from ``gs.group.member.add``

.. _gs.group.member.add.base:
   https://github.com/groupserver/gs.group.member.add.base

2.2.1 (2013-07-17)
------------------

* Adding breadcrumbs
* Cleaning up the JavaScript
* Fixing the ``Content-type`` header

2.2.0 (2013-03-19)
------------------

* Following the changes to the `gs.group.member.base`_ product

.. _gs.group.member.base:
   https://github.com/groupserver/gs.group.member.base


2.1.0 (2013-01-22)
------------------

* Moving the link to the *Add* page to the new *Administer group
  members* viewlet

2.0.1 (2012-11-26)
------------------

* Fixing a Python 2.6 issue with the format strings

2.0.0 (2012-11-13)
------------------

* Updating for the new GroupServer UI
  + Using a full-page layout
  + Creating the *Welcome* notification
  + Creating the *New member* notification
* Changing the base class of the *Add* page to ``GroupForm``
* Splitting the adder code from the *Add* page
* Changing the marker-interface that is used

1.4.0 (2012-06-22)
------------------

* Updating the SQLAlchemy code

1.3.0 (2012-05-15)
------------------

* Following the changes to `gs.group.member.invite.base`_

.. _gs.group.member.invite.base:
   https://github.com/groupserver/gs.group.member.invite.base


1.2.0 (2011-01-26)
------------------

* Adding support for `gs.profile.email.base`_

.. _gs.profile.email.base:
   https://github.com/groupserver/gs.profile.email.base

1.1.0 (2011-01-12)
------------------

* Adding support for `gs.profile.email.verify`_

.. _gs.profile.email.verify:
   https://github.com/groupserver/gs.profile.email.verify

1.0.0 (2010-12-15)
------------------

Initial version. Prior to the creation of this product adding
people was impossible with the standard GroupServer
user-interface.

..  LocalWords:  Changelog reStructuredText GitHub Transifex
