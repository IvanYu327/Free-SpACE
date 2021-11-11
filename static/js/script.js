//the array
function printBtn() {
  fetch("/static/js/master.json")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);

      for (var key in data) {
        if (data.hasOwnProperty(key)) {
          console.log(key + " -> " + data[key]);

          var btn = document.createElement("button");
          var t = document.createTextNode(key + ": " + data[key]);
          btn.id = "adminbutton";
          btn.className = "adminbtn";
          btn.appendChild(t);
          document.body.appendChild(btn);
          document.body.addEventListener("click", function (event) {
            if (event.target.id == "adminbutton") {
              console.log("func called");
              var elem = document.getElementById("adminbutton");
              var txt = elem.textContent;
              if (txt.endsWith("false")) {
                txt = txt.replace("false", "true");
                elem.innerHTML = txt;
              } else {
                txt = txt.replace("true", "false");
                elem.innerHTML = txt;
              }
            }
          });
        }
      }
    });
}
