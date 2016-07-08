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

import re

from dNG.controller.predefined_http_request import PredefinedHttpRequest
from dNG.data.data_linker import DataLinker
from dNG.data.http.translatable_error import TranslatableError
from dNG.data.settings import Settings
from dNG.data.text.input_filter import InputFilter
from dNG.data.text.l10n import L10n
from dNG.data.xhtml.link import Link
from dNG.database.nothing_matched_exception import NothingMatchedException

from .module import Module

class Index(Module):
#
	"""
Service for "m=datalinker"

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: datalinker
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
	"""

	def execute_related(self):
	#
		"""
Action for "related"

TODO: Check if "load list" for tags with empty mid are feasible.

:since: v0.2.00
		"""

		_id = InputFilter.filter_control_chars(self.request.get_dsd("oid", ""))
		main_id = InputFilter.filter_control_chars(self.request.get_dsd("omid", ""))
		tag = InputFilter.filter_control_chars(self.request.get_dsd("otag", ""))

		source_iline = InputFilter.filter_control_chars(self.request.get_dsd("source", "")).strip()

		L10n.init("pas_http_datalinker")
		Settings.read_file("{0}/settings/pas_http_datalinker_identity_registry.json".format(Settings.get("path_data")))

		if (self.response.is_supported("html_css_files")): self.response.add_theme_css_file("mini_default_sprite.min.css")

		if (len(source_iline) > 0):
		#
			Link.set_store("servicemenu",
			               Link.TYPE_RELATIVE_URL,
			               L10n.get("core_back"),
			               { "__query__": re.sub("\\_\\_\\w+\\_\\_", "", source_iline) },
			               icon = "mini-default-back",
			               priority = 7
			              )
		#

		datalinker_object = None
		_exception = None

		try:
		#
			if (len(_id) > 0): datalinker_object = DataLinker.load_id(_id)
			elif (len(tag) > 0 and len(main_id) > 0):
			#
				datalinker_object = DataLinker.load_tag(tag, main_id)
				_id = datalinker_object.get_id()
			#
		#
		except NothingMatchedException as handled_exception: _exception = handled_exception

		# TODO: Provide option to create wiki style
		if (datalinker_object is None): raise TranslatableError("pas_http_datalinker_oid_invalid", 404, _exception = _exception)

		identity = datalinker_object.get_identity()
		identity_registry = Settings.get("pas_http_datalinker_identity_registry", { })

		if (identity not in identity_registry): raise TranslatableError("pas_http_datalinker_oid_not_identifiable")

		Link.clear_store("servicemenu")

		datalinker_view_iline = identity_registry[identity]['view_iline'].replace("__id__", _id)
		datalinker_view_iline = re.sub("\\_\\_\\w+\\_\\_", "", datalinker_view_iline)

		redirect_request = PredefinedHttpRequest()
		redirect_request.set_iline(datalinker_view_iline)

		dsd_dict = self.request.get_dsd_dict()
		for key in dsd_dict: redirect_request.set_dsd(key, dsd_dict[key])

		self.request.redirect(redirect_request)
	#
#

##j## EOF