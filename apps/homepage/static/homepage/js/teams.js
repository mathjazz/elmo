/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function() {
  $('#id_locale_code').bind('keyup', function() {
    var s = this.value;
    $('#teams > li').show();
    if (s.length) {
      $('#teams > li:not([class*="' + s.toLowerCase() + '"])').hide();
    }
  });
});
