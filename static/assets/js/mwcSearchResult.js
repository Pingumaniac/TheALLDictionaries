$(document).ready(function () {
    const getMwcSettings = {
        "async": true,
        "crossDomain": true,
        "url": "/mwcDict/" + WORD_INPUT,
        "method": "GET"
    };

    function mwcNotFound() {
        var html = "<li>The short definition of, '" + WORD_INPUT + ",' is not found on Merriam Webster Dictionary.</li>";
        $("#mwcList").append(html);
    }

    function mwcPolling() {
        if (WORD_INPUT == "") {
            mwcNotFound();
        }
        else {
            $.ajax(getMwcSettings).done(function (response) {
                dictionaryResult = JSON.parse(response);

                if (dictionaryResult.length == 0) {
                    mwcNotFound();
                }
                else {
                    for (var i = 0; i < dictionaryResult.length; i++) {
                        if ('meta' in dictionaryResult[i] === false) {
                            mwcNotFound();
                            break;
                        }
                        else {
                            var shortDefinitionList = dictionaryResult[i]['shortdef'];
                            for (var j = 0; j < shortDefinitionList.length; j++) {
                                var html = '<li>' + shortDefinitionList[j] + '</li>';
                                $("#mwcList").append(html);
                            }
                        }
                    }
                }
            })
        }
    }

    mwcPolling();
});
