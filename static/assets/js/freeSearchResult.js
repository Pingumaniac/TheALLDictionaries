$(document).ready(function () {
    let baseURL = "http://www.thefreedictionary.com/";
    let queryURL = WORD_INPUT.replaceAll(" ", "+");
    let wordURL = baseURL + queryURL;
    let html = '<a href='+ wordURL + ' target="_blank"><button class="btn btn-xs btn-outline-primary">';
    html += 'View the results from The Free Dictionary.</button></a>';
    $('#free').append(html);
});