function CRITICAL_hides() {
   if (CRITICAL_checks() == "ok") {
  let x = document.getElementById("CRITICAL_div2");
   CRITICAL_checks();
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }else{alert("No, you missed.")}
}

let CRITICAL_input = {{CRITICAL|length}};
function CRITICAL_add() {
     let x = document.getElementById("CRITICAL_table").rows.length ;
    CRITICAL_input = CRITICAL_input +1;
    var table = document.getElementById("CRITICAL_table");
    var row = table.insertRow(x);
    row.id = "rowid_CRITICAL"+CRITICAL_input;
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);

    cell1.innerHTML = "<input  type='text' placeholder='Var' class='form-control' type='text' required>"
    cell2.innerHTML = "<input type='text' class='form-control' placeholder='Message' type='text' >"
    cell3.innerHTML = "<button class='btn btn-secondary close'  onclick='CRITICAL_delete(\"rowid_CRITICAL"+CRITICAL_input+"\")'><i style='font-size:30px' class='material-icons'>remove_circle_outline</i></button>";
}
function CRITICAL_delete(tbip_id) {
  let rowIndex = document.getElementById(tbip_id).rowIndex
  document.getElementById("CRITICAL_table").deleteRow(rowIndex);
}

function CRITICAL_checks() {
  var form = $("#CRITICAL_myForm")
  form.addClass('was-validated');
  if (form[0].checkValidity() === false) {
    return "fail";
  }
  else{
   return "ok";
 }
}

function CRITICAL_show(){
 CRITICAL_ls =[]
   let x = document.getElementById("CRITICAL_table").rows.length ;
   for (var i = 1; i < x; i++) {
     CRITICAL_cond = (document.getElementById("CRITICAL_table").rows[i].cells[0].children[0].value);
     CRITICAL_msg = (document.getElementById("CRITICAL_table").rows[i].cells[1].children[0].value);
     CRITICAL_di =  {cond:CRITICAL_cond, msg : CRITICAL_msg }
     CRITICAL_ls.push(CRITICAL_di);
   }
 
  return CRITICAL_ls;
}