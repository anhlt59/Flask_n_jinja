function WARNING_hides() {
   if (WARNING_checks() == "ok") {
  let x = document.getElementById("WARNING_div2");
   WARNING_checks();
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }else{alert("No, you missed.")}
}

let WARNING_input = 1;
function WARNING_add() {
    let x = document.getElementById("WARNING_table").rows.length ;
    WARNING_input = WARNING_input +1;
    var table = document.getElementById("WARNING_table");
    var row = table.insertRow(x);
    row.id = "rowid_WARNING"+WARNING_input;
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);

      cell1.innerHTML = "<input  type='text' placeholder='Var' class='form-control' type='text' required>"
    +"        <div class='invalid-feedback'>No, you missed this one.</div>"
    cell2.innerHTML = "<input type='text' class='form-control' placeholder='Value' type='text' >"
    cell3.innerHTML = "<button class='btn btn-secondary close'  onclick='WARNING_delete(\"rowid_WARNING"+WARNING_input+"\")'><i style='font-size:30px' class='material-icons'>remove_circle_outline</i></button>";
}
function WARNING_delete(tbip_id) {
  let rowIndex = document.getElementById(tbip_id).rowIndex
  document.getElementById("WARNING_table").deleteRow(rowIndex);
}

function WARNING_checks() {
  var form = $("#WARNING_myForm")
  form.addClass('was-validated');
  if (form[0].checkValidity() === false) {
    return "fail";
  }
  else{
   return "ok";
 }
}

function WARNING_show(){
 WARNING_ls =[]
   let x = document.getElementById("WARNING_table").rows.length ;
   for (var i = 1; i < x; i++) {
     WARNING_cond = (document.getElementById("WARNING_table").rows[i].cells[0].children[0].value);
     WARNING_msg = (document.getElementById("WARNING_table").rows[i].cells[1].children[0].value);
     WARNING_di =  {cond:WARNING_cond, msg : WARNING_msg }
     WARNING_ls.push(WARNING_di);
   }

  return WARNING_ls;
}