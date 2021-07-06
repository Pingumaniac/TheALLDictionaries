$(document).ready(function () {
    const getWikipediaSettings = {
        "async": true,
        "crossDomain": true,
        "url": "/wikipedia/" + WORD_INPUT,
        "method": "GET"
    };

    function wikipediaPolling() {
        $.ajax(getWikipediaSettings).done(function (response) {
            let wikiResult = JSON.parse(response);
            let title = wikiResult["outputTitle"];
            let summary = wikiResult["outputSummary"];
            let url = wikiResult["outputURL"];

            if (title == null && summary == null & url == null) {
                $("#wikiTitle").html("The wikipedia article for, '" + WORD_INPUT + ",' has not been found.");
            }
            else {
                $("#wikiTitle").html("Title: " + title)
                $("#wikipedia").append("<br><h3><u>Summary</u></h3><br>");
                var summaryHTML = '<p class="mb-1 d-flex w-100 justify-content-between" id="wikiSummary">' + summary + '</p>';
                $('#wikipedia').append(summaryHTML);
                $("#wikipedia").append("<br>");
                var linkHTML = '<a href=' + url + '><button class="btn btn-xs btn-outline-primary">';
                linkHTML += 'View the full article from Wikipedia.</button></a><br>';
                $('#wikipedia').append(linkHTML);
            }
        })
    }

    wikipediaPolling();
});