$(document).ready(function () {
    const getGoogleNewsSettings = {
        "async": true,
        "crossDomain": true,
        "url": "/googleNewsDict/" + WORD_INPUT,
        "method": "GET"
    };

    function googleNewsPolling() {
        $.ajax(getGoogleNewsSettings).done(function (response) {
            let googleNewsResult = JSON.parse(response);

            if (googleNewsResult == []) {
                var googleNewsHTML = "<li>No results found. Try different keywords.</li>";
                $("#googleNewsList").append(googleNewsHTML);
            }
            else {
                var loopMax = 20;
                if (googleNewsResult.length < 20) {
                    loopMax = googleNewsResult.length;
                }
                for (var i = 0; i < googleNewsResult.length; i++) {
                    var link = "https://" + googleNewsResult[i]["link"];
                    var title = googleNewsResult[i]["title"];
                    var description = googleNewsResult[i]["desc"];
                    var date = googleNewsResult[i]["date"];
                    var image = googleNewsResult[i]["img"];
                    var site = googleNewsResult[i]["site"];

                    var newsHTML = '<a href=' + link + ' target="_blank">';
                    newsHTML += '<li>Title: ' + title;
                    newsHTML += '<br>Description: ' + description;
                    newsHTML += '<br>Source: ' + site;
                    newsHTML += '<br>Published ' + date + '.</li></a>';
                    $("#googleNewsList").append(newsHTML);

                    var newsImageHTML = '<a href=' + image + ' target="_blank"><img src=' + image + ' width="20%" , height="auto"></a>';
                    $("#googleNewsList").append(newsImageHTML);
                    $("#googleNewsList").append('<p></p>');
                }
            }
        })
    }

    if (WORD_INPUT == "") {
        var googleNewsHTML = "<li>No results found. Try different keywords.</li>";
        $("#googleNewsList").append(googleNewsHTML);
    }
    else {
        googleNewsPolling();
    }
});