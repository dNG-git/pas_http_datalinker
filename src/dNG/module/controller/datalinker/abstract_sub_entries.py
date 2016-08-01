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
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(pasHttpDataLinkerVersion)#
#echo(__FILEPATH__)#
"""

from time import time

from dNG.data.data_linker import DataLinker
from dNG.data.text.l10n import L10n
from dNG.data.xhtml.formatting import Formatting as XHtmlFormatting
from dNG.data.xhtml.link import Link
from dNG.data.xml_parser import XmlParser
from dNG.database.connection import Connection
from dNG.module.controller.abstract_http import AbstractHttp as AbstractHttpController

try: from dNG.data.ownable_mixin import OwnableMixin as OwnableInstance
except ImportError: OwnableInstance = None

class AbstractSubEntries(AbstractHttpController):
#
	"""
The "AbstractSubEntries" class provides methods to handle child entries.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: datalinker
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractSubEntries)

:since: v0.2.00
		"""

		AbstractHttpController.__init__(self)

		L10n.init("pas_http_datalinker")
	#

	@Connection.wrap_callable
	def _get_datalinker_entry_links(self, parent_id, offset = 0, limit = -1, hide_inaccessible = False):
	#
		"""
Returns a list of rendered links for object children.

:return: (list) Links for the service menu
:since:  v0.2.00
		"""

		_return = [ ]

		datalinker_parent = DataLinker.load_id(parent_id)
		session = (self.request.get_session() if (self.request.is_supported("session")) else None)

		datalinker_sub_entries = (datalinker_parent.get_sub_entries()
		                          if (OwnableInstance is None
		                              or (not isinstance(datalinker_parent, OwnableInstance))
		                              or datalinker_parent.is_readable_for_session_user(session)
		                             ) else
		                          [ ]
		                         )

		inaccessible_entry = { "id": "",
		                       "sub_entries": 0,
		                       "sub_entries_type": 0,
		                       "time_sortable": time(),
		                       "symbol": "",
		                       "title": L10n.get("pas_http_datalinker_entry_inaccessible"),
		                       "tag": "",
		                       "views_count": False,
		                       "views": 0
		                     }

		for datalinker_object in datalinker_sub_entries:
		#
			is_readable = (OwnableInstance is None
			               or (not isinstance(datalinker_object, OwnableInstance))
			               or datalinker_object.is_readable_for_session_user(session)
			              )

			if (is_readable):
			#
				datalinker_object_data = datalinker_object.get_data_attributes("id",
				                                                               "sub_entries",
				                                                               "sub_entries_type",
				                                                               "time_sortable",
				                                                               "symbol",
				                                                               "title",
				                                                               "tag",
				                                                               "views_count",
				                                                               "views"
				                                                              )

				_return.append(datalinker_object_data.copy())
			#
			elif (not hide_inaccessible): _return.append(inaccessible_entry.copy())
		#

		return _return
	#

	def _get_sub_entries_link_content(self, count, _type = None):
	#
		"""
Returns the text reflecting the sub entries type link for more content.

:param count: 
:param _type: Sub entries type defined

:return: (str) Sub entries link name; empty string if not known
:since:  v0.2.00
		"""

		if (not self._is_primary_action() and "type" in self.context):
		#
			if (self.context['type'] == DataLinker.SUB_ENTRIES_TYPE_ADDITIONAL_CONTENT): _type = self.context['type']
		#

		l10n_base_id = "pas_http_datalinker_view_sub_entries_link"

		if (_type == DataLinker.SUB_ENTRIES_TYPE_ADDITIONAL_CONTENT): l10n_base_id = "pas_http_datalinker_view_sub_entries_additional_content_link"

		return "{0}{1:d}{2}".format(L10n.get(l10n_base_id + "_1"), count, L10n.get(l10n_base_id + "_2"))
	#

	def _get_sub_entries_title(self, _type = None):
	#
		"""
Returns the title reflecting the sub entries type.

:param _type: Sub entries type defined

:return: (str) Sub entries title; empty string if not known
:since:  v0.2.00
		"""

		_return = ""

		if (not self._is_primary_action()):
		#
			if ("type" in self.context):
			#
				if (self.context['type'] == DataLinker.SUB_ENTRIES_TYPE_ADDITIONAL_CONTENT): _type = self.context['type']
			#
			elif ("title" in self.context): _return = self.context['title']
		#

		if (_return == ""):
		#
			if (_type == DataLinker.SUB_ENTRIES_TYPE_ADDITIONAL_CONTENT): _return = L10n.get("pas_http_datalinker_sub_entries_additional_content")
		#

		return _return
	#

	def _render_link(self, data):
	#
		"""
Renders a link.

:return: (str) Link XHTML
:since:  v0.2.00
		"""

		_return = ""

		if ("id" in data and "title" in data):
		#
			url = Link().build_url(Link.TYPE_RELATIVE_URL, { "m": "datalinker", "a": "related", "dsd": { "oid": data['id'] } })

			xml_parser = XmlParser()
			_return = "{0}{1}</a>".format(xml_parser.dict_to_xml_item_encoder({ "tag": "a", "attributes": { "href": url } }, False), XHtmlFormatting.escape(data['title']))
		#

		return _return
	#
#

##j## EOF