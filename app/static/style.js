function style_semester_li(semester) {
  return '<a class="semester">' + semester.name + '</a>';
}

function style_section(section) {
  return '<li>' +
           '<div class="section card waves-effect waves-block waves-light" data-classcode="' +
              section.class_code + '" data-number="' + section.number + '">' +
             '<div class="card-content">' +
               '<div class="section-header card-title row">' +
                 '<div class="col s6 left-align">' +
                   section.class_code + ' ' + section.kind + ' ' +
                   '<span class="thin section-number">' + section.number + '</span>' +
                 '</div>' +
                 '<div class="col s6 right-align">' +
                   section.instructor +
                 '</div>' +
               '</div>' +
               '<ul class="section-info">' +
                 '<li>' + section.time + '</li>' +
                 '<li>' + (section.days.join('/')) + '</li>' +
                 '<li>' + ((section.room != null) ? section.room : '') + '</li>' +
               '</ul>' +
             '</div>' +
           '</div>' +
         '</li>';
}
