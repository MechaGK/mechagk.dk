$(document).ready(function () {
    //var activeMenu = "<?php echo $active_menu?>";
    var baseUrl = location.origin + "/";
    var jsonPath = baseUrl + "data/menu-items.json";

    $.getJSON(jsonPath, function (data) {
        $.each(data, function (index, object) {
            var itemID = "navbar-item-" + object.id;
            var linkID = "navbar-link-" + object.id;
            var objLink = baseUrl + object.link;

            $("#navbar-items").append('<li id="' + itemID + '">');
            $("#" + itemID)
                .append('<a id="' + linkID + '" href="' + objLink + '">' + object.title + '</a>');

            if (activeMenu == object.name) {
                $("#" + itemID).addClass("active");
                $("#" + linkID).append('<span class="sr-only">(current)</span>');
            }
        })
    })
})