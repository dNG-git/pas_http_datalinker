# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;http;datalinker

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasHttpDataLinkerVersion)#
#echo(__FILEPATH__)#
"""

from .abstract import Abstract
from .data_linker_row import DataLinkerRow
from .source_callbacks_mixin import SourceCallbacksMixin

class DataLinker(Abstract, SourceCallbacksMixin):
#
	"""
"DataLinker" uses a DataLinker entry to iterate over the sub entries.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: datalinker
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, entry = None):
	#
		"""
Constructor __init__(DataLinker)

:param entry: DataLinker entry

:since: v0.1.00
		"""

		Abstract.__init__(self)
		SourceCallbacksMixin.__init__(self)

		self.entry = entry
		"""
DataLinker entry to iterate
		"""
		self.sub_entries_count = None
		"""
DataLinker sub entries count
		"""
		self.sub_entry_iterator = None
		"""
DataLinker sub entry iterator
		"""
	#

	def __next__(self):
	#
		"""
python.org: Return the next item from the container.

:return: (object) Result object
:since:  v0.1.00
		"""

		if (self.sub_entry_iterator == None): self._init_iterator()

		try: return DataLinkerRow(next(self.sub_entry_iterator))
		except StopIteration:
		#
			self.sub_entry_iterator = None
			raise
		#
	#

	def get_row_count(self):
	#
		"""
Returns the number of rows.

:return: (int) Number of rows
:since:  v0.1.00
		"""

		if (self.sub_entries_count == None):
		#
			source_row_count_callback = (self.entry.get_sub_entries_count if (self.source_row_count_callback == None) else self.source_row_count_callback)
			self.sub_entries_count = source_row_count_callback()
		#

		return self.sub_entries_count
	#

	def _init_iterator(self):
	#
		"""
Initializes the iterator on demand.

:since: v0.1.00
		"""

		source_rows_callback = (self.entry.get_sub_entries if (self.source_rows_callback == None) else self.source_rows_callback)
		self.sub_entry_iterator = source_rows_callback(self.offset, self.limit)
	#
#

##j## EOF