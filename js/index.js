function copyText() {
    var copyText = document.getElementById("mail");
    var text = "";
    for (var i = 0; i < copyText.children.length; i++) {
        if(copyText.children[i].nodeName !== "BUTTON" && copyText.children[i].textContent !== "Generated Email:")
            text += copyText.children[i].textContent + "\n";
    }
    var textArea = document.createElement("textarea");
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand("Copy");
    textArea.remove();
    alert("Copied the text: " + text);
}
document.documentElement.webkitRequestFullscreen();
document.documentElement.setAttribute("webkit-reader", "false");

document.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', e => {
        document.getElementById('language').value = e.target.textContent;
    });
});

