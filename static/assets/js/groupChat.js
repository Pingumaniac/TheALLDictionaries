$(document).ready(function() {
    let chatMessageBox = document.getElementById('chatMessageBox');
    let groupChatList = document.getElementById('groupChatList');
    let chatJson;
    let pTagNumber;
    const settings = {
        "async": true,
        "crossDomain": true,
        "url": "/groupChatMessage",
        "method": "GET"
    }

    function polling() {
        $.ajax(settings).done(function (response) {
        // chatJson = JSON.parse(response);
        // pTagNumber = document.getElementsByTagName("P").length;
        // Note that chatJson.length = pTagNumber - 1 as there is another p element in the footer.
        chatJson = JSON.parse(response);
        pTagNumber = document.getElementsByTagName("P").length;
        console.log(chatJson)
        console.log(pTagNumber)
        // Case: the input box for writing the message is empty
        if (chatMessageBox.value.length == 0) {
            // Case: new message has been sent from an another user or more
            if (chatJson.length >= pTagNumber) {
                for (i = pTagNumber - chatJson.length; i >= 0; i--) {
                    var jsonData = chatJson[i];
                    var senderID = jsonData["senderID"];
                    var chatMessage = ' ' + jsonData["chatMessage"]; // added a blank space for spacing
                    var sendDate = jsonData["sendDate"];
                    var nickName = jsonData["nickName"] + ' '; // added a blank space for spacing
                    var profilePictureURL = jsonData["profilePictureURL"]
                    if (profilePictureURL == null) {
                        var html = '<p><strong>' + nickName + '</strong>';
                        html += '<span class="small text-truncate text-gray-700">(' + senderID + ', ' + sendDate + ') </span>';
                        html += '<strong>:</strong>' + chatMessage + '</p>';
                        $("#groupChatList").prepend(html);
                    }
                    else {
                        var html = '<a href=' + profilePictureURL + ' target="_blank"><p><strong>' + nickName + '</strong></a>';
                        html += '<span class="small text-truncate text-gray-700">(' + senderID + ', ' + sendDate + ') </span>';
                        html += '<strong>:</strong>' + chatMessage + '</p>';
                        $("#groupChatList").prepend(html);
                    }
                }
            } 
        }
    })}; 
    setInterval(polling, 3000);
});  

