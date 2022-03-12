const prev_button = $("#previous");
const next_button = $("#next");
const weekNumber = $("#week");
const artist_div = $("#replaceable-week");
const artist_div1 = $("#replaceable-data");
let currentWeek = 0;
let workingWeek;
const endpoint = "";
const delay_by_in_ms = 700;
let scheduled_function = false;

$(document).ready(function () {
  currentWeek = parseInt($(weekNumber).html());
  workingWeek = currentWeek;
  $(prev_button).click(function () {
    workingWeek--;
    $.getJSON(endpoint, {
      week: workingWeek,
      direction: workingWeek - currentWeek,
    }).done((response) => {
      artist_div.html(response["html_from_view"]);
      artist_div1.html(response["html_from_view1"]);
    });
    
  });
  $(next_button).click(function () {
    workingWeek++;
    $.getJSON(endpoint, {
      week: workingWeek,
      direction: workingWeek - currentWeek,
    }).done((response) => {
      artist_div.html(response["html_from_view"]);
      artist_div1.html(response["html_from_view1"]);
    });
    
  });
});
