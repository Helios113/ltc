$(document).ready(function () {
    let height1 = $("nav").height();
    let height2 = $("#course-info").height();
    $("body").scrollspy({ target: "#scroll-list", offset: height1+height2});
});
