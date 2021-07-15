$(document).ready(function () {
    const getYouTubeSettings = {
        "async": true,
        "crossDomain": true,
        "url": "/youtubeDict/" + WORD_INPUT,
        "method": "GET"
    };

    function youtubePolling() {
        $.ajax(getYouTubeSettings).done(function (response) {
            let youtubeOutput = JSON.parse(response);
            let youtubeResult = youtubeOutput["result"];

            
            if (youtubeResult == []) {
                var youtubeHTML = "<p>No results found. Try different keywords.</p>";
                $("#youtubeList").append(youtubeHTML);
            }
            else {
                for (var i = 0; i < youtubeResult.length; i++) {
                    var youtubeLink = youtubeResult[i]['link'];
                    var youtubeEmbedLink = youtubeLink.replace('watch?v=', 'embed/');
                    var embedHTML = '<p><iframe width="100%" height="500" src=' + youtubeEmbedLink +  ' allowfullscreen></iframe></p>';
                    $("#youtubeList").append(embedHTML);

                    $("#youtubeList").append('<br>');
                }
            }
        })
    }

    if (WORD_INPUT == "") {
        var youtubeHTML = "<p>No results found. Try different keywords.</p>";
        $("#youtubeList").append(youtubeHTML);
    } 
    else {
        youtubePolling();
    }
});