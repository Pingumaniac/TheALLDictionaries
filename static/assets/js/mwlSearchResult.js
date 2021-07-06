$(document).ready(function () {
    const getMwlSettings = {
        "async": true,
        "crossDomain": true,
        "url": "/mwlDict/" + WORD_INPUT,
        "method": "GET"
    };

    function mwlNotFound() {
        var html = "<li>The short definition of, '" + WORD_INPUT + ",' is not found on Merriam Webster's Learner's Dictionary.</li>";
        $("#mwlList").append(html);
    }

    function mwlPolling() {
        if (WORD_INPUT == "") {
            mwlNotFound();
        }
        else {
            $.ajax(getMwlSettings).done(function (response) {
                dictionaryResult = JSON.parse(response);

                if (dictionaryResult.length == 0) {
                    mwlNotFound();
                }
                else {
                    // var loopMax = dictionaryResult.length > 3 ? 3 : dictionaryResult.length;
                    for (var i = 0; i < dictionaryResult.length; i++) {
                        if ('meta' in dictionaryResult[i] === false) {
                            mwlNotFound();
                            break;
                        }
                        else {
                            var shortDefinitionList = dictionaryResult[i]['shortdef'];
                            for (var j = 0; j < shortDefinitionList.length; j++) {
                                var html = '<li>' + shortDefinitionList[j] + '</li>';
                                $("#mwlList").append(html);
                            }
                        }
                    }
                }
            })
        }
    }

    mwlPolling();
});