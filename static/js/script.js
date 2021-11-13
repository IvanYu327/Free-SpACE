var content = ["Watch Team Liquid", "Play Bingo", "Win Big"];
var part = 0;
var partIndex = 0;
var intervalValue;
var element = document.querySelector("#text");

// Implements typing effect
function Type() {
  try {
    var text = content[part].substring(0, partIndex + 1);
    element.innerHTML = text;
    partIndex++;

    if (text === content[part]) {
      clearInterval(intervalValue);
      setTimeout(function () {
        intervalValue = setInterval(Delete, 50);
      }, 1000);
    }
  } catch (err) {}
}

// Implements deleting effect
function Delete() {
  var text = content[part].substring(0, partIndex - 1);
  element.innerHTML = text;
  partIndex--;

  // If sentence has been deleted then start to display the next sentence
  if (text === "") {
    clearInterval(intervalValue);

    if (part == content.length - 1) part = 0;
    else part++;

    partIndex = 0;

    setTimeout(function () {
      intervalValue = setInterval(Type, 100);
    }, 200);
  }
}

intervalValue = setInterval(Type, 100);

function printBtn() {
  fetch("/static/js/master.json")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      var x = 0;
      for (var key in data) {
        if (data.hasOwnProperty(key)) {
          x++;
          console.log(key + " -> " + data[key]);
          console.log(x);
          var btn = document.createElement("button");
          var t = document.createTextNode(key + ": " + data[key]);
          btn.id = "adminbutton" + x;
          btn.name = "adminbutton" + x;
          btn.className = "adminbtn";
          btn.value = key + ": " + data[key];
          btn.appendChild(t);

          // btn.addEventListener("click", function (event) {
          //   console.log("foo");
          //   if (event.target) {
          //     console.log("func called");
          //     var elem = document.getElementById(event.target.id);
          //     var txt = elem.textContent;
          //     if (txt.endsWith("false")) {
          //       txt = txt.replace("false", "true");
          //       elem.innerHTML = txt;

          //       txt = txt.replace(": true", "");
          //       console.log(txt);
          //       data[txt] = true;
          //     } else {
          //       txt = txt.replace("true", "false");
          //       elem.innerHTML = txt;

          //       txt = txt.replace(": false", "");
          //       console.log(txt);
          //       data[txt] = false;
          //     }
          //   }
          // });
          console.log("button made");
          var form = document.getElementById("form");
          form.appendChild(btn);
        }
      }
    });
}
