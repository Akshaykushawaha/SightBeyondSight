document.getElementById("contrast1").addEventListener("click", () => {
  const meta = document.querySelector('meta[name="color-scheme"]');
  if (meta.content !== "light") {
    var toRemove = meta.content + "-mode";
    meta.content = "light";
    document.body.classList.remove(toRemove);
    document.body.classList.add("light-mode");
    document.getElementById("logo").src =
      "static/web/png/ColorLogoBackground.png";
  }
});

document.getElementById("contrast2").addEventListener("click", () => {
  const meta = document.querySelector('meta[name="color-scheme"]');
  if (meta.content !== "dark") {
    var toRemove = meta.content + "-mode";
    meta.content = "dark";
    document.body.classList.remove(toRemove);
    document.body.classList.add("dark-mode");
    document.getElementById("logo").src =
      "static/web/png/White logo - no background.png";
  }
});

document.getElementById("contrast4").addEventListener("click", () => {
  const meta = document.querySelector('meta[name="color-scheme"]');
  if (meta.content !== "blue") {
    var toRemove = meta.content + "-mode";
    meta.content = "blue";
    document.body.classList.remove(toRemove);
    document.body.classList.add("blue-mode");
    document.getElementById("logo").src =
      "static/web/png/Color logo - no background.png";
  }
});

function getSelectionText() {
  var text = "";
  if (window.getSelection) {
    text = window.getSelection().toString();
    // for Internet Explorer 8 and below. For Blogger, you should use &amp;&amp; instead of &&.
  } else if (document.selection && document.selection.type != "Control") {
    text = document.selection.createRange().text;
  }
  return text;
}

$(document).ready(function () {
  // when the document has completed loading
  $(document).mouseup(function (e) {
    // attach the mouseup event for all div and pre tags
    setTimeout(function () {
      responsiveVoice.cancel();
      responsiveVoice.speak(getSelectionText());
    }, 0);
  });
});
