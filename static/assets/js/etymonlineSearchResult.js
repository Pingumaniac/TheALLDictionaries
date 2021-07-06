$(document).ready(function () {
    let baseURL = "https://www.etymonline.com/search?q=";
    let queryURL = WORD_INPUT.replaceAll(" ", "+");
    let wordURL = baseURL + queryURL;
    let html = '<a href='+ wordURL + ' target="_blank"><button class="btn btn-xs btn-outline-primary">';
    html += 'View the full results from Etymonline</button></a>';
    $('#etymonline').append(html);
});