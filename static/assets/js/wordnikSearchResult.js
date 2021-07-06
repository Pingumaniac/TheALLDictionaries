$(document).ready(function () {
    let wordURL = "";
    if (WORD_INPUT == "") {
        wordURL = "https://www.wordnik.com/";
    }
    else {
        let baseURL = "https://www.wordnik.com/words/";
        let queryURL = WORD_INPUT.replaceAll(" ", "%20");
        wordURL = baseURL + queryURL;
    }
    let html = '<a href='+ wordURL + ' target="_blank"><button class="btn btn-xs btn-outline-primary">';
    html += 'View the results from Wordnik.</button></a>';
    $('#wordnik').append(html);
});