# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.module.blocks.datalinker.Module
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

from dNG.pas.data.translatable_exception import TranslatableException
from dNG.pas.database.connection import Connection
from dNG.pas.module.blocks.abstract_block import AbstractBlock

class Module(AbstractBlock):
#
	"""
Module for "datalinker"

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
Constructor __init__(Module)

:since: v0.1.00
		"""

		AbstractBlock.__init__(self)

		self.database = None
		"""
Database instance
		"""
	#

	def execute(self):
	#
		"""
Execute the requested action.

:since: v0.1.00
		"""

		with self.database: return AbstractBlock.execute(self)
	#

	def init(self, request, response):
	#
		"""
Initialize block from the given request and response.

:param request: Request object
:param response: Response object

:since: v0.1.00
		"""

		AbstractBlock.init(self, request, response)
		self._init_db()
	#

	def _init_db(self):
	#
		"""
Initializes the database.

:since: v0.1.00
		"""

		# pylint: disable=broad-except

		try: self.database = Connection.get_instance()
		except Exception as handled_exception:
		#
			if (self.log_handler != None): self.log_handler.error(handled_exception)
		#

		if (self.database == None): raise TranslatableException("core_database_error")
	#
#

##j## EOF