$(document).ready(function () {
    const getWiktionarySettings = {
        "async": true,
        "crossDomain": true,
        "url": "/wiktionaryDict/" + WORD_INPUT,
        "method": "GET"
    };

    function wiktionaryPolling() {
        $.ajax(getWiktionarySettings).done(function (response) {
            let wiktionaryResult = JSON.parse(response);
            if (wiktionaryResult == [{"etymology": "", "definitions": [], "pronunciations": {"text": [], "audio": []}}]) {
                var definitionHTML = '<p class="mb-1 d-flex w-100 justify-content-between">'
                definitionHTML += 'The, '+ WORD_INPUT + ', is not found in Wiktionary.</p>';
                $("#wiktionary").append(definitionHTML);
            } 
            else {
                let definitionList = wiktionaryResult[0]["definitions"];
                for (var i = 0; i < definitionList.length; i++) {
                    var definitionHTML = '<p class="mb-1 d-flex w-100 justify-content-between">';
                    definitionHTML += '<u>Definition ' + (i+1).toString() + '</u></p>';
                    $("#wiktionary").append(definitionHTML);

                    let textList = definitionList[i]["text"];
                    $("#wiktionary").append('<ul>');
                    for (var j = 0; j < textList.length; j++) {
                        var textHTML = '<li>' + textList[j] + '</li>';
                        $("#wiktionary").append(textHTML);
                    }
                    $("#wiktionary").append('</ul>');
                    $("#wiktionary").append('<br>');

                    let partOfSpeech = definitionList[i]["partOfSpeech"];
                    var partOfSpeechHTML = '<p class="mb-1 d-flex w-100 justify-content-between">';
                    partOfSpeechHTML += 'Part of speech: ' + partOfSpeech + '</p>';
                    $("#wiktionary").append(partOfSpeechHTML);
                    $("#wiktionary").append('<br>');

                    let examples = definitionList[i]["examples"];
                    $("#wiktionary").append('<p class="mb-1 d-flex w-100 justify-content-between">Examples:</p>');
                    $("#wiktionary").append('<ol>');
                    for (var j = 0; j < examples.length; j++) {
                        var exampleHTML = '<li>' + examples[j] + '</li>';
                        $("#wiktionary").append(exampleHTML);
                    }
                    $("#wiktionary").append('</ol>');
                    $("#wiktionary").append('<br>');
                    $("#wiktionary").append('<br>');
                }                
            }
        })
    }

    if (WORD_INPUT == "") {
        var definitionHTML = '<p class="mb-1 d-flex w-100 justify-content-between">'
        definitionHTML += 'The, '+ WORD_INPUT + ', is not found in Wiktionary.</p>';
        $("#wiktionary").append(definitionHTML);
    }
    else {
        wiktionaryPolling();
    }
});