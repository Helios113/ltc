const right = $("#right_pane");
const left = $("#left_pane");


$(document).ready(function () {
  right.css({"maxHeight":left.height()});
});
