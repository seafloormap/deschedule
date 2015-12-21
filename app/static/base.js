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
    sections = resp['data'];
    show_sections(sections);
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

function show_sections(sections) {
  dismiss_sections();

  var styled_sections = [];
  $.each(sections, function(key, val) {
    styled_sections.push(style_section(val));
  });
  $('#spinner').removeClass('active');
  $('#sections').html(styled_sections.join(''));
  console.log('Loaded class sections.');
  Materialize.showStaggeredList('#sections-container');
}

function dismiss_sections() {
  // Adapted from Materialize/js/transitions.js showStaggeredList
  var time = 0;
  $('#sections-container').find('li').each(function() {
    $(this).velocity(
        { opacity: "0", translateX: "200px" },
        { duration: 800, delay: time, easing: [60, 10] });
    time += 120;
  });
}

function any_sections_selected() {
  return ($('.section.active').length > 0);
}

function construct_schedule_url(school, semester, sections) {
    if(typeof(sections) != 'string') { sections = sections.join(','); }
    return 'schedule/?semester=' + semester + '&sections=' + sections;
}

function get_school() {
  /* TODO: remove toLowerCase once API supports it */
  return $('div[name="school"] input').val().trim().toLowerCase();
}

function get_semester() {
  return $('div[name="semester"] input').val().trim();
}

function format_days(monday, tuesday, wednesday, thursday, friday, saturday, sunday) {
  var day_bools = [monday, tuesday, wednesday, thursday, friday, saturday, sunday];
  var day_names = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'];
  var days = [];
  for (var i = 0; i < 7; i++) {
    if(day_bools[i]) {
      days.push(day_names[i]);
    }
  }
  return days.join('/');
}
