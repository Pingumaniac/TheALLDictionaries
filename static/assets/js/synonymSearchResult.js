$(document).ready(function () {
    const getSynonymSettings = {
        "async": true,
        "crossDomain": true,
        "url": "/synonymDict/" + WORD_INPUT,
        "method": "GET"
    };

    function synonymPolling() {
        $.ajax(getSynonymSettings).done(function (response) {
            let thesaurusResult = JSON.parse(response);
            let synonymResult = thesaurusResult["synonyms"];
            let antonymResult = thesaurusResult["antonyms"];
            
            if (synonymResult[0] == "No synonym found at synonym.com") {
                var html = "<li>No synonym found at synonym.com.</li>";
                $("#synonymList").append(html);
            }
            else {
                for (var i = 0; i < synonymResult.length; i++) {
                    var html = '<a href=' + '/searchResult/' + synonymResult[i] + ' target="_blank">';
                    html += "<li>" + synonymResult[i] + "</li>";
                    html += '</a>';
                    $("#synonymList").append(html);
                }
            }

            if (antonymResult[0] == "No antonym found at synonym.com") {
                var html = "<li>No antonym found at synonym.com.</li>";
                $("#antonymList").append(html);
            }
            else {
                for (var i = 0; i < antonymResult.length; i++) {
                    var html = '<a href=' + '/searchResult/' + antonymResult[i] + ' target="_blank">';
                    html += "<li>" + antonymResult[i] + "</li>";
                    html += '</a>';
                    $("#antonymList").append(html);
                }
            }
        })
    }

    synonymPolling();
});