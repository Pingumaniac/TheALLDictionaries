$(document).ready(function () {
    let baseURL = "https://visuwords.com/";
    let queryURL = WORD_INPUT.replaceAll(" ", "%20");
    let wordURL = baseURL + queryURL;
    let html = '<a href='+ wordURL + ' target="_blank"><button class="btn btn-xs btn-outline-primary">';
    html += 'View the results from Visuwords.</button></a>';
    $('#visuwords').append(html);
});