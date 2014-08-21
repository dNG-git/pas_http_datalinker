# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;http;datalinker

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasHttpDataLinkerVersion)#
#echo(__FILEPATH__)#
"""

from .abstract_row import AbstractRow

class DataLinkerRow(AbstractRow):
#
	"""
"DataLinkerRow" provides properties mapped to DataLinker entry attributes.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: datalinker
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, entry):
	#
		"""
Constructor __init__(DataLinkerRow)

:param entry: DataLinker entry

:since: v0.1.00
		"""

		self.entry = entry
		"""
DataLinker entry to iterate
		"""
	#

	def __getitem__(self, key):
	#
		"""
python.org: Called to implement evaluation of self[key].

:param name: Attribute name

:return: (mixed) Attribute value
:since:  v0.1.00
		"""

		return self.entry.get_data_attributes(key)[key]
	#
#

##j## EOF