var semesters = [];
function fill_all_semesters(school, callback) {
  console.log('Loading semesters...');
  api_semesters(school, function(resp) {
    semesters = [];
    $.each(resp['data'], function(key, value) {
      semesters.push('<li>' + style_semester_li(val) + '</li>');
    });
    $('ul.semesters').html(semesters.join(''));
    console.log('Loaded semesters.');

    callback(resp);
  });
}

var sections = [];
function fill_all_sections(school, semester, callback) {
  console.log('Loading class sections...');
  $('#results .preloader-wrapper').addClass('active');
  api_classes(school, semester, function(resp) {
    sections = [];
    $.each(resp['data'], function(key, val) {
      sections.push('<li>' + style_section(val) + '</li>');
    });

    $('#results .preloader-wrapper').removeClass('active');
    $('#sections').html(sections.join(""));
    console.log('Loaded class sections.');

    callback(resp);
  });
}

function fill_some_sections(school, semester, sections) {
  console.log('Loading class sections...');
  api_schedule(school, semester, sections, function(resp) {
    var items = [];
    $.each(resp['data'], function(key, val) {
      items.push('<li>' + style_section(val) + '</li>');
    });
    $('#sections').html(items.join(""));
    console.log('Loaded class sections.');
  });
}

function any_sections_selected() {
  return ($('.section-selected').length > 0);
}

function construct_schedule_url(school, semester, sections) {
    if(typeof(sections) != 'string') { sections = sections.join(','); }
    return 'schedule/?semester=' + semester + '&sections=' + sections;
}
