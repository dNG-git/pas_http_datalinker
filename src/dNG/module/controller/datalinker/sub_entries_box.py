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

from dNG.data.http.translatable_error import TranslatableError
from dNG.data.text.l10n import L10n

from .abstract_sub_entries import AbstractSubEntries

class SubEntriesBox(AbstractSubEntries):
#
	"""
"SubEntriesBox" is a navigation element providing links to child entries.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: datalinker
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def _get_rendered_links(self):
	#
		"""
Returns a list of rendered links for object children.

:return: (list) Links for the service menu
:since:  v0.2.00
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

		if ("id" in self.context): links += self._get_datalinker_entry_links(self.context['id'], hide_inaccessible = True)

		for link in links: _return.append(self._render_link(link))

		return _return
	#

	def execute_render(self):
	#
		"""
Action for "render"

:since: v0.2.00
		"""

		if (self._is_primary_action()): raise TranslatableError("core_access_denied", 403)

		rendered_links = self._get_rendered_links()

		if (len(rendered_links) > 0):
		#
			title = self._get_sub_entries_title()

			content = ("" if (title == "") else "<h1>{0}</h1>".format(title))
			content += "<ul><li>{0}</li></ul>".format("</li>\n<li>".join(rendered_links))

			self.set_action_result("<nav class='pagecontent_box pagecontent_datalinker_sub_entries_box'>{0}</nav>".format(content))
		#
	#
#

##j## EOF