let textarea = document.getElementById("text");
textarea.addEventListener("input", increaseRow, false);

function increaseRow() {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

let title = document.getElementById('title');
let text = document.getElementById('text');

let titleCharacterCount = document.getElementById('titleCharacterCount');
let currentCharacterCount = document.getElementById('currentCharacterCount');

function CharacterCount() {
    titleCharacterCount.innerHTML = title.value.length;
    currentCharacterCount.innerHTML = text.value.length;
}

setInterval(CharacterCount, 250);