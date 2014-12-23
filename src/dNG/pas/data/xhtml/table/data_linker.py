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

from dNG.pas.database.sort_definition import SortDefinition
from .abstract import Abstract
from .data_linker_row import DataLinkerRow
from .source_callbacks_mixin import SourceCallbacksMixin

class DataLinker(SourceCallbacksMixin, Abstract):
#
	"""
"DataLinker" uses a DataLinker entry to iterate over the sub entries.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: datalinker
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
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

		self.supported_features['sorting'] = True
	#

	def __next__(self):
	#
		"""
python.org: Return the next item from the container.

:return: (object) Result object
:since:  v0.1.00
		"""

		if (self.sub_entry_iterator is None): self._init_iterator()

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

		if (self.sub_entries_count is None):
		#
			source_row_count_callback = (self.entry.get_sub_entries_count if (self.source_row_count_callback is None) else self.source_row_count_callback)
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

		sort_list = None

		if (len(self.sort_list) > 0): sort_list = self.sort_list
		elif (self.default_sort_definition is not None): sort_list = [ self.default_sort_definition ]

		if (sort_list is not None):
		#
			sort_definition = SortDefinition()

			for sort_value in sort_list:
			#
				sort_definition.append(sort_value['key'],
				                       (SortDefinition.DESCENDING
				                        if (sort_value['direction'] == DataLinker.SORT_DESCENDING) else
				                        SortDefinition.ASCENDING
				                       )
				                      )
			#

			self.entry.set_sort_definition(sort_definition, self.sort_context)
		#

		source_rows_callback = (self.entry.get_sub_entries if (self.source_rows_callback is None) else self.source_rows_callback)
		self.sub_entry_iterator = source_rows_callback(self.offset, self.limit)
	#
#

##j## EOF