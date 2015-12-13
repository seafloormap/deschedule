function api_get(url, callback) {
  return $.getJSON(url, callback);
}

function api_classes(school, semester, callback) {
  return api_get('/api/' + school + '/semester/' + semester + '/class/',
      callback);
}
