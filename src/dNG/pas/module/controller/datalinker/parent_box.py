# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;http;datalinker

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
http://www.direct-netware.de/redirect.py?licenses;gpl
----------------------------------------------------------------------------
#echo(pasHttpDataLinkerVersion)#
#echo(__FILEPATH__)#
"""

from dNG.data.xml_parser import XmlParser
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.formatting import Formatting as XHtmlFormatting
from dNG.pas.data.xhtml.link import Link
from dNG.pas.module.controller.abstract_http import AbstractHttp as AbstractHttpController

class ParentBox(AbstractHttpController):
#
	"""
"ParentBox" is a navigation element providing a link to the parent entry.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: datalinker
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self):
	#
		"""
Constructor __init__(ParentBox)

:since: v0.1.00
		"""

		AbstractHttpController.__init__(self)

		L10n.init("pas_http_datalinker")
	#

	def execute_render(self):
	#
		"""
Action for "render"

:since: v0.1.00
		"""

		if ("id" in self.context):
		#
			title =  self.context.get("title", L10n.get("pas_http_core_level_up"))
			url = Link().build_url(Link.TYPE_RELATIVE, { "m": "datalinker", "a": "related", "dsd": { "oid": self.context['id'] } })

			content = "{0}{1}{2}".format(L10n.get("pas_http_datalinker_view_parent_1"),
			                             XmlParser().dict_to_xml_item_encoder({ "tag": "a",
			                                                                    "value": XHtmlFormatting.escape(title),
			                                                                    "attributes": { "href": url }
			                                                                  }),
			                             L10n.get("pas_http_datalinker_view_parent_2")
			                            )

			self.set_action_result("<p class='pagecontent_box pagecontent_datalinker_parent_box'>{0}</p>".format(content))
		#
	#
#

##j## EOF