# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;http;datalinker

The following license agreement remains valid unless any additions or
changes are being made by direct Netware Group in a written form.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(pasHttpDataLinkerVersion)#
#echo(__FILEPATH__)#
"""

from time import time

from dNG.data.text.l10n import L10n
from dNG.database.sort_definition import SortDefinition

from .abstract import Abstract
from .data_linker_row import DataLinkerRow
from .inaccessible_row import InaccessibleRow
from .source_callbacks_mixin import SourceCallbacksMixin

try: from dNG.data.ownable_mixin import OwnableMixin as OwnableInstance
except ImportError: OwnableInstance = None

try: from dNG.data.session.implementation import Implementation as Session
except ImportError: Session = None

class DataLinker(SourceCallbacksMixin, Abstract):
#
	"""
"DataLinker" uses a DataLinker entry to iterate over the sub entries.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: datalinker
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self, entry = None):
	#
		"""
Constructor __init__(DataLinker)

:param entry: DataLinker entry

:since: v0.2.00
		"""

		Abstract.__init__(self)
		SourceCallbacksMixin.__init__(self)

		self.entry = entry
		"""
DataLinker entry to iterate
		"""
		self.session = None
		"""
Session instance used to verify access permissions
		"""
		self.session_loaded = (Session is None)
		"""
True after the Session instance has been cached
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
:since:  v0.2.00
		"""

		if (self.sub_entry_iterator is None): self._init_iterator()

		try:
		#
			sub_entry = next(self.sub_entry_iterator)

			return (DataLinkerRow(sub_entry)
			        if (OwnableInstance is None
			            or (not isinstance(sub_entry, OwnableInstance))
			            or sub_entry.is_readable_for_session_user(self._get_session())
			           ) else
			        InaccessibleRow({ "id": "",
			                          "sub_entries": 0,
			                          "sub_entries_type": 0,
			                          "time_sortable": time(),
			                          "symbol": "",
			                          "title": L10n.get("pas_http_datalinker_entry_inaccessible"),
			                          "tag": "",
			                          "views_count": False,
			                          "views": 0
			                        })
			       )
		#
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
:since:  v0.2.00
		"""

		if (self.sub_entries_count is None):
		#
			source_row_count_callback = (self.entry.get_sub_entries_count if (self.source_row_count_callback is None) else self.source_row_count_callback)
			self.sub_entries_count = source_row_count_callback()
		#

		return self.sub_entries_count
	#

	def _get_session(self):
	#
		"""
Returns the session used to verify access permissions.
		"""

		if (not self.session_loaded):
		#
			self.session = Session.load(session_create = False)
			self.session_loaded = True
		#

		return self.session
	#

	def _init_iterator(self):
	#
		"""
Initializes the iterator on demand.

:since: v0.2.00
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

	def _is_sort_key_known(self, key):
	#
		"""
Checks if the given sort key is known.

:param key: Key used internally

:return: (bool) Returns true if the sort key is known
:since:  v0.2.00
		"""

		_return = Abstract._is_sort_key_known(self, key)
		if (not _return): _return = self.entry.is_data_attribute_defined(key)

		return _return
	#
#

##j## EOF