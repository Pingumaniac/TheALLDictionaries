$(document).ready(function () {
    const getUrbanSettings = {
        "async": true,
        "crossDomain": true,
        "url": "/urbanDict/" + WORD_INPUT,
        "method": "GET"
    };

    function urbanPolling() {
        if (WORD_INPUT == "") {
            var definitionHTML = "<p class='mb-1'>Definition: " + "No definition founded in Urban Dictionary." + "</p>";
            var exampleHTML = "<p class='mb-1'>Example: " + "No example founded in Urban Dictionary." + "</p>";
            $("#urban").append(definitionHTML);
            $("#urban").append(exampleHTML);
        }
        else {
            $.ajax(getUrbanSettings).done(function (response) {
                dictionaryResult = JSON.parse(response);

                for (var i = 0; i < dictionaryResult.length; i++) {
                    var definition = dictionaryResult[i]["definition"];
                    var example = dictionaryResult[i]["example"];
                    var definitionHTML = "<p class='mb-1' style='white-space:pre-wrap;'>Definition " + (i+1).toString() + ": " + "<br>";
                    definitionHTML += definition + "</p>";
                    var exampleHTML = "<p class='mb-1' style='white-space:pre-wrap;'>Example " + (i+1).toString() + ": " + "<br>";
                    exampleHTML += example + "</p>";
                    $("#urban").append(definitionHTML);
                    $("#urban").append("<br>");
                    $("#urban").append(exampleHTML);
                    $("#urban").append("<br>");
                    $("#urban").append("<br>");
                }

                var fullLink  = "https://www.urbandictionary.com/define.php?term=" + WORD_INPUT;
                var linkHTML = "<a href=" + fullLink + " target='_blank'><button class='btn btn-xs btn-outline-primary'>";
                linkHTML += "View the results from Urban Dictionary.</button></a>";
                $("#urban").append(linkHTML);
            })
        }
    }

    urbanPolling();
});