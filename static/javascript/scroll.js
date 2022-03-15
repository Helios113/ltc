$(document).ready(function () {
    let height1 = $("nav").height();
    let height2 = $("#course-info").height();
    alert(height1+height2);
    $("body").scrollspy({ target: "#scroll-list", offset: height1+height2});
});
