const prev_button = $("#previous");
const next_button = $("#next");
const weekNumber = $("#week");
const week_div = $("#replaceable-week");
const data_div = $("#replaceable-data");
let currentWeek = 0;
let workingWeek;
const endpoint = "";
const delay_by_in_ms = 100;
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
        week_div.html(response["html_week"]);
        data_div.html(response["html_data"]);
    });
    
  });
  $(next_button).click(function () {
    workingWeek++;
    $.getJSON(endpoint, {
      week: workingWeek,
      direction: workingWeek - currentWeek,
    }).done((response) => {
        week_div.html(response["html_week"]);
        data_div.html(response["html_data"]);
    });
    
  });
});
