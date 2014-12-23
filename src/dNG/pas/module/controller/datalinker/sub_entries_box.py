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

from dNG.data.xml_parser import XmlParser
from dNG.pas.data.data_linker import DataLinker
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.formatting import Formatting as XHtmlFormatting
from dNG.pas.data.xhtml.link import Link
from dNG.pas.database.connection import Connection
from dNG.pas.module.controller.abstract_http import AbstractHttp as AbstractHttpController

class SubEntriesBox(AbstractHttpController):
#
	"""
"SubEntriesBox" is a navigation element providing links to child entries.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: datalinker
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def _get_datalinker_entry_links(self, parent_id):
	#
		"""
Returns a list of rendered links for object children.

:return: (list) Links for the service menu
:since:  v0.1.01
		"""

		_return = [ ]

		with Connection.get_instance():
		#
			datalinker_parent = DataLinker.load_id(parent_id)

			datalinker_sub_entries = datalinker_parent.get_sub_entries()

			for datalinker_object in datalinker_sub_entries:
			#
				datalinker_object_data = datalinker_object.get_data_attributes("id", "title")
				_return.append({ "id": datalinker_object_data['id'], "title": datalinker_object_data['title'] })
			#
		#

		return _return
	#

	def _get_rendered_links(self):
	#
		"""
Returns a list of rendered links for object children.

:return: (list) Links for the service menu
:since:  v0.1.01
		"""

		_return = [ ]

		links = [ ]

		if ("parent_id" in self.context
		    and (self.context.get("id") != self.context['parent_id'])
		   ):
		#
			links.append({ "id": self.context['parent_id'],
			               "title": self.context.get("parent_title", L10n.get("pas_http_core_level_up"))
			             })
		#

		if ("id" in self.context): links += self._get_datalinker_entry_links(self.context['id'])

		for link in links: _return.append(self._render_link(link))

		return _return
	#

	def _render_link(self, data):
	#
		"""
Renders a link.

:return: (str) Link XHTML
:since:  v0.1.01
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

	def execute_render(self):
	#
		"""
Action for "render"

:since: v0.1.00
		"""

		rendered_links = self._get_rendered_links()

		if (len(rendered_links) > 0):
		#
			content = ""

			if ("type" in self.context):
			#
				if (self.context['type'] == DataLinker.SUB_ENTRIES_TYPE_ADDITIONAL_CONTENT): content = "<h1>{0}</h1>".format(L10n.get("pas_http_datalinker_sub_entries_additional_content"))
			#
			elif ("title" in self.context): content = "<h1>{0}</h1>".format(XHtmlFormatting.escape(self.context['title']))

			content += "<ul><li>{0}</li></ul>".format("</li>\n<li>".join(rendered_links))

			self.set_action_result("<nav class='pagecontent_box pagecontent_datalinker_sub_entries_box'>{0}</nav>".format(content))
		#
	#
#

##j## EOF