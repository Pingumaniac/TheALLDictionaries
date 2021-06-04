// Constants for colours
const BEGINNER_COLOUR = '#eb4841';
const NOVICE_COLOUR = '#FF7F50';
const INTERMEDIATE_COLOUR = '#DD9B00';
const FAST_COLOUR = '#98af07';
const PROFESSIONAL_COLOUR = '#4cc35c';
const EXPERT_COLOUR = '#20C0B0';
const MASTER_COLOUR = '#6495ED';
const GRANDMASTER_COLOUR = '#6363B0';
const ENLIGHTENED_COLOUR = '#AA62B0';

// Global variables related to scoring
let score = 0
let currentAccuracy = document.getElementById("currentAccuracy");
let scoreSubmit = document.getElementById("scoreSubmit");
scoreSubmit.style.visibility = 'hidden';
let charactersPerMinute = document.getElementById('currentCPM');
let currentScore = document.getElementById('currentScore');
let aboutScore = document.getElementById('aboutScore');

// Global variables related to the text
let challengeText = document.getElementById("challengeText");

// Global variables for character count
let challengeCharacterCount = document.getElementById('challengeCharacterCount');
challengeCharacterCount.innerHTML = challengeText.innerHTML.length;
let currentCharacterCount = document.getElementById('currentCharacterCount');

// Global variables related to displaying game status
let gameStatus = document.getElementById("gameStatus");
let gameLevel = document.getElementById("gameLevel");
let gamePlaying = false;
let hasAlerted = false;

// Global variables for beginning && stopping the challenge
let start = document.getElementById('start');
let restart = document.getElementById('restart');
restart.style.visibility = 'hidden';

// Global variables for timing
let stopwatchDisplay = document.getElementById("stopwatchDisplay")
stopwatchDisplay.style.visibility = 'hidden';
let timeTaken = document.getElementById('timeTaken');
let currentTime = 0;

// Global variables for the text box
let textarea = document.getElementById("textarea");
textarea.style.visibility = 'hidden';
textarea.addEventListener("input", increaseRow, false);
function increaseRow() {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

/*  
Global variable and a function to check accuracy.
stringSimilary.compareTwoStrings is based on Dice coefficent's algorithm
Reference: https://www.npmjs.com/package/string-similarity 
Works by adding the following in startTextTyping.html: 
<script src="//unpkg.com/string-similarity/umd/string-similarity.min.js"></script>
*/
let accuracy = 0;
function updateAccuracy() {
    correspondingOriginalText = challengeText.innerHTML.slice(0, textarea.value.length)
    accuracy = stringSimilarity.compareTwoStrings(correspondingOriginalText, textarea.value);
    currentAccuracy.innerHTML = (accuracy * 100).toString().slice(0,5) + "%";
    return accuracy;
}

// Find out the game status 
function getGameStatus() {
    if (!gamePlaying) {
        gameStatus.innerHTML = "Game Over.".bold();
        scoreSubmit.style.visibility = 'visible';
        start.style.visibility = 'hidden';
        restart.style.visibility = 'visible';
        if (!hasAlerted) {
            alert("Game over. Your score is " + score);
            hasAlerted = true;
        }
    }
    else {
        if (challengeText.innerHTML.length <= textarea.value.length) {
            gamePlaying = false;
            scoreSubmit.style.visibility = 'visible';
            scoreSubmit.value = score;
        }
    }
    checkScore();
}

function stopwatch() {
    if (gamePlaying) {
        currentTime += 1;
        timeTaken.innerHTML = currentTime;
    }
    else {
        timeTaken.innerHTML = currentTime;
    }
}

function checkScore() {
    currentCharacterCount.innerHTML = textarea.value.length;
    if (gamePlaying) {
        if (textarea.value == null) {
            charactersPerMinute.innerHTML = 0;
            score = 0;
        }
        else {
            if (textarea.value.length < 1) {
                charactersPerMinute.innerHTML = 0;
                score = 0;
            }
            charactersPerMinute.innerHTML = Math.round(textarea.value.length / currentTime * 60);
            score = Math.round(charactersPerMinute.innerHTML * accuracy);
        }
    }

    if (score <= 150) {
        gameLevel.innerHTML = "You are a beginner.".bold();
        currentScore.innerHTML = score;
        gameLevel.style.color = BEGINNER_COLOUR;
        aboutScore.style.color = BEGINNER_COLOUR;
    }
    else if (score > 150 && score <= 300) {
        gameLevel.innerHTML = "You are a novice.".bold();
        currentScore.innerHTML = score;
        gameLevel.style.color = NOVICE_COLOUR;
        aboutScore.style.color = NOVICE_COLOUR;
    }
    else if (score > 300 && score <= 400) {
        gameLevel.innerHTML = "You are an intermediate player.".bold();
        currentScore.innerHTML = score;
        gameLevel.style.color = INTERMEDIATE_COLOUR;
        aboutScore.style.color = INTERMEDIATE_COLOUR;
    }
    else if (score > 400 && score <= 500) {
        gameLevel.innerHTML = "You are a fast player.".bold();
        currentScore.innerHTML = score;
        gameLevel.style.color = FAST_COLOUR;
        aboutScore.style.color = FAST_COLOUR;
    }
    else if (score > 500 && score <= 600) {
        gameLevel.innerHTML = "You are a professional player.".bold();
        currentScore.innerHTML = score;
        gameLevel.style.color = PROFESSIONAL_COLOUR;
        aboutScore.style.color = PROFESSIONAL_COLOUR;
    }
    else if (score > 600 && score <= 700) {
        gameLevel.innerHTML = "You are an expert in this game.".bold();
        currentScore.innerHTML = score;
        gameLevel.style.color = EXPERT_COLOUR;
        aboutScore.style.color = EXPERT_COLOUR;
    }
    else if (score > 700 && score <= 800) {
        gameLevel.innerHTML = "You are a master!".bold();
        currentScore.innerHTML = score;
        gameLevel.style.color = MASTER_COLOUR;
        aboutScore.style.color = MASTER_COLOUR;
    }
    else if (score > 800 && score <= 900) {
        gameLevel.innerHTML = "You are a grand master!!".bold();
        currentScore.innerHTML = score;
        gameLevel.style.color = GRANDMASTER_COLOUR;
        aboutScore.style.color = GRANDMASTER_COLOUR;
    }
    else if (score > 900) {
        gameLevel.innerHTML = "You are enlightened!!!".bold();
        currentScore.innerHTML = score;
        gameLevel.style.color = ENLIGHTENED_COLOUR;
        aboutScore.style.color = ENLIGHTENED_COLOUR;
    }
}

// Executed when the user presses the start button
function beginTextTyping() {
    start.style.visibility = 'hidden';
    restart.style.visibility = 'visible';
    textarea.style.visibility = 'visible';
    textarea.value = '';
    stopwatchDisplay.style.visibility = 'visible';
    currentTime = 0;
    timeTaken.innerHTML = currentTime;
    currentScore.innerHTML = 0;
    gamePlaying = true;
    hasAlerted = false;
    // Call the stopwatch every 1 second
    setInterval(stopwatch, 1000)
    // update accuracy every 0.25 second
    setInterval(updateAccuracy, 250)
    // Check game status every 0.25 second
    setInterval(getGameStatus, 250)
}