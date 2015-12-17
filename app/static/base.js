function fill_all_sections(school, semester, callback) {
  console.log('Loading class sections...');
  api_classes(school, semester, function(resp) {
    console.log('got resp');
    var items = [];
    $.each(resp['data'], function(key, val) {
      items.push('<li>' + style_section(val) + '</li>');
    });

    $('#sections').html(items.join(""));
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
