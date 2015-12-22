function style_semester_li(semester) {
  return '<a class="semester">' + semester.name + '</a>';
}

function style_section(section, classes) {
  if(!classes) { classes = []; }
  return '<li>' +
           '<div class="section card waves-effect waves-block waves-light ' +
                classes.join(' ') +
              '" data-sectionid="' + section.class_code+'.'+section.number +'" ' +
              'onclick="section_click(this);">' +
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
               '<div class="section-info row">' +
                 '<div class="col s4">' + section.days.join('/') + '</div>' +
                 '<div class="col s4">' + section.time + '</div>' +
                 '<div class="col s4 right-align">' + (section.room ? section.room : '') + '</div>' +
               '</div>' +
             '</div>' +
           '</div>' +
         '</li>';
}

function style_section_chip(code_id) {
  return '<div class="section chip" data-sectionid="' + code_id + '">' + code_id +
      '<i class="material-icons">close</i>' +
    '</div>'
}
