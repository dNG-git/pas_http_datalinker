# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.module.blocks.output.Index
"""
"""n// NOTE
----------------------------------------------------------------------------
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
----------------------------------------------------------------------------
NOTE_END //n"""

import re

from dNG.pas.controller.predefined_http_request import PredefinedHttpRequest
from dNG.pas.data.data_linker import DataLinker
from dNG.pas.data.settings import Settings
from dNG.pas.data.http.translatable_exception import TranslatableException
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.link import Link
from dNG.pas.runtime.value_exception import ValueException
from .module import Module

class Index(Module):
#
	"""
Service for "m=datalinker"

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: datalinker
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	def execute_related(self):
	#
		"""
Action for "related"

TODO: Check if "load list" for tags with empty mid are feasible.

:since: v0.1.00
		"""

		_id = InputFilter.filter_file_path(self.request.get_dsd("oid", ""))
		main_id = InputFilter.filter_file_path(self.request.get_dsd("omid", ""))
		tag = InputFilter.filter_file_path(self.request.get_dsd("otag", ""))

		source_iline = InputFilter.filter_control_chars(self.request.get_dsd("source", "")).strip()

		L10n.init("pas_http_datalinker")
		Settings.read_file("{0}/settings/pas_http_datalinker_type_registry.json".format(Settings.get("path_data")))

		if (len(source_iline) > 0): Link.store_set("servicemenu", Link.TYPE_RELATIVE, L10n.get("core_back"), { "__query__": re.sub("\\[\\w+\\]", "", source_iline) }, image = "mini_default_back", priority = 2)

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
		except ValueException as handled_exception: _exception = handled_exception

		# TODO: Provide option to create wiki style
		if (datalinker_object == None): raise TranslatableException("pas_http_datalinker_oid_invalid", 404, _exception = _exception)

		identity = datalinker_object.get_identity()
		identity_registry = Settings.get("pas_http_datalinker_identity_registry", { })

		if (identity not in identity_registry): raise TranslatableException("pas_http_datalinker_oid_not_identifiable")

		Link.store_clear("servicemenu")

		datalinker_view_iline = identity_registry[identity]['view_iline'].replace("[id]", _id)
		datalinker_view_iline = re.sub("\\[\\w+\\]", "", datalinker_view_iline)

		redirect_request = PredefinedHttpRequest()
		redirect_request.set_iline(datalinker_view_iline)
		self.request.redirect(redirect_request)	#
#

##j## EOF