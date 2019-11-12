function UNKNOWN_hides() {
   if (UNKNOWN_checks() == "ok") {
  let x = document.getElementById("UNKNOWN_div2");
   UNKNOWN_checks();
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }else{alert("No, you missed.")}
}

let UNKNOWN_input = {{UNKNOWN|length}};
function UNKNOWN_add() {
     let x = document.getElementById("UNKNOWN_table").rows.length ;
    UNKNOWN_input = UNKNOWN_input +1;
    var table = document.getElementById("UNKNOWN_table");
    var row = table.insertRow(x);
    row.id = "rowid_UNKNOWN"+UNKNOWN_input;
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);

      cell1.innerHTML = "<input  type='text' placeholder='Var' class='form-control' type='text' required>"
    cell2.innerHTML = "<input type='text' class='form-control' placeholder='Message' type='text' >"
    cell3.innerHTML = "<button class='btn btn-secondary close'  onclick='UNKNOWN_delete(\"rowid_UNKNOWN"+UNKNOWN_input+"\")'><i style='font-size:30px' class='material-icons'>remove_circle_outline</i></button>";
}
function UNKNOWN_delete(tbip_id) {
  let rowIndex = document.getElementById(tbip_id).rowIndex
  document.getElementById("UNKNOWN_table").deleteRow(rowIndex);
}

function UNKNOWN_checks() {
  var form = $("#UNKNOWN_myForm")
  form.addClass('was-validated');
  if (form[0].checkValidity() === false) {
    return "fail";
  }
  else{
   return "ok";
 }
}

function UNKNOWN_show(){
 UNKNOWN_ls =[]
   let x = document.getElementById("UNKNOWN_table").rows.length ;
   for (var i = 1; i < x; i++) {
     UNKNOWN_cond = (document.getElementById("UNKNOWN_table").rows[i].cells[0].children[0].value);
     UNKNOWN_msg = (document.getElementById("UNKNOWN_table").rows[i].cells[1].children[0].value);
     UNKNOWN_di =  {cond:UNKNOWN_cond, msg : UNKNOWN_msg }
     UNKNOWN_ls.push(UNKNOWN_di);
   }
 
  return UNKNOWN_ls;
} 