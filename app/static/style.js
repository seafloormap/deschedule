function style_section(section) {
  return '<div class="mui-panel section" data-classcode="' +
             section.class_code + '" data-number="' + section.number + '">' +
           '<div class="section-header mui-row">' +
             '<div class="mui-col-md-4">' +
               '<span class="section-class-code mui--align-middle">' + section.class_code + '</span>' +
               '<span class="section-kind mui--align-middle">' + section.kind + '</span>' +
               '<span class="section-number mui--align-middle">' + section.number + '</span>' +
             '</div>' +
             '<div class="mui-col-md-4 mui-col-md-offset-4">' +
               '<span class="section-instructor mui--align-middle">' + section.instructor + '</span>' +
             '</div>' +
           '</div>' +
           '<div class="section-info mui-row">' +
             '<div class="mui-col-md-4">' +
               '<span class="section-time mui--align-middle">' +
                 section.time +
               '</span>' +
             '</div>' +
             '<div class="mui-col-md-4">' +
               '<span class="section-room mui--align-middle">' +
                 (section.days.join('/')) +
               '</span>' +
             '</div>' +
             '<div class="mui-col-md-4">' +
               '<span class="section-room mui--align-middle">' +
                 ((section.room != null) ? section.room : '') +
               '</span>' +
             '</div>' +
           '</div>' +
         '</div>';
}

function any_sections_selected() {
  return ($('.section-selected').length > 0);
}
