const user_input = $("#user-input");
const artists_div = $("#replaceable-content");
const endpoint = "";
const delay_by_in_ms = 700;
let scheduled_function = false;

$("#my-select").selectpicker("refresh");

let ajax_call = function (endpoint, request_parameters) {
  $.getJSON(endpoint, request_parameters).done((response) => {
    $("#my-select").html(response["html_from_view"]);
    
    
    $("#my-select").selectpicker("refresh");
    $("#my-select").selectpicker("refresh");
  });
};

$("#my-div .form-control").on("keyup", function () {
  //here you listen to the change of the input corresponding to your select
  //and now you can populate your select element
  const request_parameters = {
    q: $(this).val(), // value of user_input: the HTML element with ID user-input
  };

  if (scheduled_function) {
    clearTimeout(scheduled_function);
  }

  // setTimeout returns the ID of the function to be executed
  scheduled_function = setTimeout(
    ajax_call,
    delay_by_in_ms,
    endpoint,
    request_parameters
  );
});
