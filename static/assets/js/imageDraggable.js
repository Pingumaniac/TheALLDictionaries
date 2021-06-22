let fromDragPosition;
let selected;
let toDragPosition;
let div;
let id;

document.addEventListener("drop", ({
    target
}) => {
    // Case: the class name of the place to be dropped is image
    if (target.className == "image") {
        // Case: the place to drop has different id (showing that the location is different)
        if (target.id !== id ) {
            selected.remove(selected);
            for (var index = 0; index < div.length; index++) {
                if (target === div[index]) {
                    toDragPosition = index;
                }
            }
            if (fromDragPosition <= toDragPosition) {
                target.after(selected);
            } 
            else {
                target.before(selected);
            }
        }
    }
});

document.addEventListener("dragover", (event) => {
    event.preventDefault();
});

document.addEventListener("dragstart", ({
    target
}) => {
    selected = target;
    div = target.parentNode.children;
    id = target.id;
    for (var index = 0; index < div.length; index++) {
        if (selected === div[index]) {
            fromDragPosition = index;
        }
    }
});