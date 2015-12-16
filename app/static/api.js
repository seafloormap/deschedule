function api_get(url, callback) {
  return $.getJSON(url, callback);
}

function api_classes(school, semester, callback) {
  return api_get('/api/' + school + '/semester/' + semester + '/class/',
      callback);
}

function url_api_schedule_events(school, semester, section_ids) {
  return '/api/' + school + '/semester/' + semester + '/schedule/events/' +
    '?sections=' + section_ids.join(',');
}
