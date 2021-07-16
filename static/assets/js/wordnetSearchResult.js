$(document).ready(function () {
    const getWordNetSettings = {
        "async": true,
        "crossDomain": true,
        "url": "/wordnetDict/" + WORD_INPUT,
        "method": "GET"
    };

    function wordnetPolling() {
        $.ajax(getWordNetSettings).done(function (response) {
            let wordnetResult = JSON.parse(response);
            
            if (wordnetResult == null) {
                var html = "<li>The word, " + WORD_INPUT + ", is not found on WordNet.</li>";
                $("#wordnetList").append(html);
            }
            else {
                for (var partOfSpeech in wordnetResult) {
                    var partOfSpeechHTML = '<li>' + partOfSpeech + '</li>';
                    $("#wordnetList").append(partOfSpeechHTML);

                    var definitions = wordnetResult[partOfSpeech];
                    let definitionHTML = '<ul>';
                    for (var i = 0; i < definitions.length; i++) {
                        definitionHTML += '<li>' + definitions[i] + '</li>';
                    }
                    definitionHTML += '</ul>';
                    $("#wordnetList").append(definitionHTML);
                }
            }
        })
    }

    if (WORD_INPUT == "") {
        var html = "<li>The word, " + WORD_INPUT + ", is not found on WordNet.</li>";
        $("#wordnetList").append(html);
    } 
    else {
        wordnetPolling();
    }
});