function myonfocus() {
    document.getElementById("message").style.display = "block";
}
function myonblur(){
    document.getElementById("message").style.display = "block";
}

  function checkname(){
stt =""
var var_Input =  document.getElementById("Input_name");
        ck = "ok"
  for (var i = names.length - 1; i >= 0; i--) {
        if (var_Input.value.toUpperCase() == names[i].toUpperCase()) {
          ck ="fail"
        }
      }
 let lowerCaseLetters = /^[A-Za-z_][A-Za-z_0-9]*$/;;
  if(var_Input.value.match(lowerCaseLetters) && ck == "ok") {
  stt ="ok"
    letter.classList.remove("invalid_ck");
    letter.classList.add("valid");
  } else {
    stt ="fail"
    letter.classList.remove("valid");
    letter.classList.add("invalid_ck");
  }
  return stt;
}