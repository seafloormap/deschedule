function api_get(url, callback) {
  return $.getJSON(url, callback);
}

function api_classes(school, semester, callback) {
  return api_get('/api/' + school + '/semester/' + semester + '/class/',
      callback);
}

function api_schedule(school, semester, sections, callback) {
  if(typeof(sections) == 'string') {
    sections = sections.join(',');
  }
  return api_get('/api/' + school + '/semester/' + semester + '/schedule/' +
      '?sections=' + sections,
      callback);
}

function api_sections(school, semester, sections, callback) {
  if(typeof(sections) == "string") {
    sections = sections.split(',');
  }
  console.log(sections);
}

function url_api_schedule_events(school, semester, section_ids) {
  return '/api/' + school + '/semester/' + semester + '/schedule/events/' +
    '?sections=' + section_ids.join(',');
}

function api_random_sections(school, semester, number, callback) {
    var args = "";
    if(number) {
        args = '?number=' + number;
    }
    return api_get('/api/' + school + '/semester/' + semester + '/random/' + args,
            callback);
}
