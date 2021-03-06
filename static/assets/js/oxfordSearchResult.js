$(document).ready(function () {
    const getOxfordSettings = {
        "async": true,
        "crossDomain": true,
        "url": "/oxfordDict/" + WORD_INPUT,
        "method": "GET"
    }

    function oxfordNotFound() {
        var definitionHTML = "<p class='mb-1 d-flex w-100 justify-content-between'>The definition of, '" + WORD_INPUT;
        definitionHTML += ",' is not found on Oxford English Dictionary.</p>";
        var exampleHTML = "<p class='mb-1 d-flex w-100 justify-content-between'>No example found.</p>"
        $("#oxford").append(definitionHTML);
        $("#oxford").append("<br>");
        $("#oxford").append(exampleHTML);
    }

    function oxfordPolling() {
        if (WORD_INPUT == "") {
            oxfordNotFound();
        }
        else {
            $.ajax(getOxfordSettings).done(function (response) {
                dictionaryResult = JSON.parse(response);

                if ("results" in dictionaryResult === false) {
                    oxfordNotFound();
                }
                else {
                    let realResultList = dictionaryResult["results"];
                    let realResultDict = realResultList[0];
                    let resultInfoList = realResultDict["lexicalEntries"];
                    let resultInfoDict = resultInfoList[0];
                    let resultDataList = resultInfoDict["entries"];
                    let resultDataDict = resultDataList[0];

                    let partOfSpeech = "Not found";
                    if ("lexicalCategory" in resultInfoDict) {
                        var wordCategoryList = resultInfoDict["lexicalCategory"];
                        if (wordCategoryList.length != 0) {
                            partOfSpeech = wordCategoryList["text"];
                        }
                    }
                    if (partOfSpeech != "Not found") {
                        var partOfSpeechHTML = '<p class="mb-1 d-flex w-100 justify-content-between">Part of speech: ';
                        partOfSpeechHTML += partOfSpeech + '</p>';
                        $("#oxford").append(partOfSpeechHTML);
                    }

                    let wordPhoneticSpelling = "Not found";
                    let audioFile = "Not found";
                    if ("pronunciations" in resultDataDict) {
                        var wordPronunciationsList = resultDataDict["pronunciations"];
                        if (wordPronunciationsList.length != 0) {
                            var wordPronunciationsDict = wordPronunciationsList[0];
                            wordPhoneticSpelling = wordPronunciationsDict["phoneticSpelling"];
                            if (wordPronunciationsList.length >= 1) {
                                audioFile = wordPronunciationsList[1]["audioFile"];
                            }
                        }
                    }
                    if (wordPhoneticSpelling != "Not found") {
                        var wordPhoneticSpellingHTML = '<p class="mb-1 d-flex w-100 justify-content-between">Phonetic spelling: ';
                        wordPhoneticSpellingHTML += wordPhoneticSpelling + '</p>';
                        $("#oxford").append(wordPhoneticSpellingHTML);
                    }
                    if (audioFile != "Not found") {
                        var audioFileHTML = '<p class="mb-1 d-flex w-100 justify-content-between">';
                        audioFileHTML += '<audio controls><source src=' + audioFile + ' type="audio/mpeg"></audio></p><br>';
                        $("#oxford").append(audioFileHTML);
                    }

                    let wordSensesList = resultDataDict["senses"];
                    for (var i = 0; i < wordSensesList.length; i++) {
                        var definitionHTML = '<p class="mb-1 d-flex w-100 justify-content-between">Definition ' + (i + 1) + ': ';
                        definitionHTML += wordSensesList[i]['definitions'][0];
                        definitionHTML += '</p>';
                        $('#oxford').append(definitionHTML);

                        var exampleHTML = '<p class="mb-1 d-flex w-100 justify-content-between">Example(s):</p><p class="mb-1">';
                        exampleHTML += '<ol>';
                        var exampleData = wordSensesList[i]['examples'];
                        if (Array.isArray(exampleData)) {
                            for (var j = 0; j < exampleData.length; j++) {
                                exampleHTML += '<li>' + exampleData[j]['text'] + '</li>';
                            }
                        }
                        else {
                            if (exampleData === undefined) {
                                exampleHTML = "<li>No example found.</li><br>";
                            }
                            else {
                                exampleHTML += '<li>' + exampleData + '</li>';
                            }
                        }
                        exampleHTML += '</ol>';
                        $('#oxford').append(exampleHTML);
                    }
                }
            })
        }
    }

    oxfordPolling();
});
