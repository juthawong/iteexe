# ===========================================================================
# eXe
# Copyright 2004-2006, University of Auckland
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# ===========================================================================

"""
The PreferencesPage is responsible for managing eXe preferences
"""

import logging
from twisted.web.resource      import Resource
from exe.webui                 import common
from exe.webui.renderable      import RenderableResource

log = logging.getLogger(__name__)


class PreferencesPage(RenderableResource):
    """
    The PreferencesPage is responsible for managing eXe preferences
    """
    name = 'preferences'

    def __init__(self, parent):
        """
        Initialize
        """
        RenderableResource.__init__(self, parent)
        self.localeNames  = []
        
        for locale, translation in self.config.locales.items():
            localeName  = locale + ": " 
            langName = translation.info().get('x-exe-language', None)
            if langName == None:
                langName = translation.info().get('x-poedit-language', '')
            localeName += langName
            self.localeNames.append((localeName, locale))
        self.localeNames.sort()

    def render_GET(self, request):
        """Render the preferences"""
        log.debug("render_GET")
        
        # Rendering
        html  = common.docType()
        html += u"<html xmlns=\"http://www.w3.org/1999/xhtml\">\n"
        html += u"<head>\n"
        html += u"<style type=\"text/css\">\n"
        html += u"@import url(/css/exe.css);\n"
        html += u'@import url(/style/base.css);\n'
        html += u"@import url(/style/standardwhite/content.css);</style>\n"
        html += u"<title>"+_("eXe : elearning XHTML editor")+"</title>\n"
        html += u"<meta http-equiv=\"content-type\" content=\"text/html; "
        html += u" charset=UTF-8\"></meta>\n";
        html += u"</head>\n"
        html += u"<body>\n"
        html += u"<div id=\"main\"> \n"     
        html += u"<form method=\"post\" action=\"\" "
        html += u"id=\"contentForm\" >"  

        html += common.formField('select', _(u"Select Language"),
                                 'locale',
                                 options = self.localeNames,
                                 selection = self.config.locale)

        html += u"<div id=\"editorButtons\"> \n"     
        html += u"<br/>" 
        html += common.submitButton("ok", _("OK"))
        html += common.submitButton("cancel", _("Cancel"))
        html += u"</div>\n"
        html += u"</div>\n"
        html += u"<br/></form>\n"
        html += u"</body>\n"
        html += u"</html>\n"
        return html.encode('utf8')


    def render_POST(self, request):
        """
        Process the preferences selection
        """
        log.debug("render_POST " + repr(request.args))
        
        if "ok" in request.args:
            self.config.locale = request.args["locale"][0]
            self.config.locales[self.config.locale].install(unicode=True)
            self.config.configParser.set('user', 'locale', self.config.locale)

        html  = common.docType()
        html += u"<html xmlns=\"http://www.w3.org/1999/xhtml\">\n"
        html += u"<head></head>\n"
        html += u"<body onload=\"opener.location.reload(); "
        html += u"self.close();\"></body>\n"
        html += u"</html>\n"
        return html.encode('utf8')
