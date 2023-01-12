
var copyButton = document.getElementById("copy-button");
var emailText = document.getElementsByTagName("p");

var concatenatedText = "";

for (var i = 0; i < emailText.length; i++) {
    concatenatedText += emailText[i].innerText + "\n";
}

var clipboard = new ClipboardJS(copyButton, {
    text: function() {
        return concatenatedText;
    }
});

copyButton.addEventListener("click", function() {
    alert("Email copied to clipboard!");
});
