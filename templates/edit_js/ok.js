function OK_hides() {
   if (OK_checks() == "ok") {
  let x = document.getElementById("OK_div2");
   OK_checks();
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }else{alert("No, you missed.")}
}

let OK_input = {{OK|length}};
function OK_add() {
     let x = document.getElementById("OK_table").rows.length ;
    OK_input = OK_input +1;
    var table = document.getElementById("OK_table");
    var row = table.insertRow(x);
    row.id = "rowid_OK"+OK_input;
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);

    cell1.innerHTML = "<input  type='text' placeholder='Var' class='form-control' type='text' required>"
    cell2.innerHTML = "<input type='text' class='form-control' placeholder='Message' type='text' >"
    cell3.innerHTML = "<button class='btn btn-secondary close'  onclick='OK_delete(\"rowid_OK"+OK_input+"\")'><i style='font-size:30px' class='material-icons'>remove_circle_outline</i></button>";
}
function OK_delete(tbip_id) {
  let rowIndex = document.getElementById(tbip_id).rowIndex
  document.getElementById("OK_table").deleteRow(rowIndex);
}

function OK_checks() {

  var form = $("#OK_myForm")
  form.addClass('was-validated');
  if (form[0].checkValidity() === false) {
    return "fail";
  }
  else{
   return "ok";
 }
}

function OK_show(){
 OK_ls =[]
   let x = document.getElementById("OK_table").rows.length ;
   for (var i = 1; i < x; i++) {
     OK_cond = (document.getElementById("OK_table").rows[i].cells[0].children[0].value);
     OK_msg = (document.getElementById("OK_table").rows[i].cells[1].children[0].value);
     OK_di =  {cond:OK_cond, msg : OK_msg }
     OK_ls.push(OK_di);
   }

  return OK_ls;
}