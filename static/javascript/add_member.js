const user_input = $("#select-search");
const endpoint = "";
const delay_by_in_ms = 100;
let scheduled_function = false;

user_input.selectpicker("refresh");

let ajax_call = function (endpoint, request_parameters) {
  $.getJSON(endpoint, request_parameters).done((response) => {
    user_input.html(response["html_from_view"]);
    
    
    user_input.selectpicker("refresh");
    user_input.selectpicker("refresh");
  });
};
$(document).on('keyup', '#userDropdown .bs-searchbox input', function() {
  const request_parameters = {
    q: $(this).val(),
  };

  if (scheduled_function) {
    clearTimeout(scheduled_function);
  }

  scheduled_function = setTimeout(
    ajax_call,
    delay_by_in_ms,
    endpoint,
    request_parameters
  );
});
