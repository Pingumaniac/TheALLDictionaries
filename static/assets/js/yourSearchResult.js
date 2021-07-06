$(document).ready(function () {
    let wordURL = "";
    if (WORD_INPUT == "") {
        wordURL = "https://www.yourdictionary.com";
    }
    else {
        let baseURL = "https://www.yourdictionary.com/search/";
        let queryURL = WORD_INPUT.replaceAll(" ", "%20");
        wordURL = baseURL + queryURL;
    }
    let html = '<a href='+ wordURL + ' target="_blank"><button class="btn btn-xs btn-outline-primary">';
    html += 'View the results from Your Dictionary.</button></a>';
    $('#yourdictionary').append(html);
});