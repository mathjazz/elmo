# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is l10n django site.
#
# The Initial Developer of the Original Code is
# Mozilla Foundation.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Zbigniew Braniecki <gandalf@mozilla.com>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from django.shortcuts import render_to_response, get_object_or_404
from webby.models import Project, Weblocale
from django.http import HttpResponseRedirect
from life.models import Locale
from django.template import RequestContext
from django import forms
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType


class AddLocaleForm(forms.Form):
    locale = forms.CharField()


def projects(request):
    projects = Project.objects.all().order_by('name')
    return render_to_response('webby/projects.html',
                              {'projects': projects})


def project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        form = AddLocaleForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            lcode = form.cleaned_data['locale']
            locale = Locale.objects.get(code=lcode)
            wlobj = Weblocale(locale=locale,
                              project=project,
                              requestee=request.user)
            wlobj.save()
            LogEntry.objects.log_action(
                user_id         = request.user.pk,
                content_type_id = ContentType.objects.get_for_model(wlobj).pk,
                object_id       = wlobj.pk,
                object_repr     = unicode(wlobj),
                action_flag     = ADDITION
            )
            return HttpResponseRedirect('')
        else:
            return HttpResponseRedirect('')
    else:
        form = AddLocaleForm()

    locales = Weblocale.objects.filter(project=project) \
                               .order_by('locale__code')
    new_locales = Locale.objects \
                        .exclude(id__in=project.locales.values_list('id')) \
                        .order_by('code')
    return render_to_response('webby/project.html',
                              {'project': project,
                               'locales': locales,
                               'new_locales': new_locales,
                               'form': form},
                              context_instance=RequestContext(request))
