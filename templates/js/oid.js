 function oid_snmp(){
     ck = "ok"
     if (
      (document.getElementById("Version").value) == ""
      && (document.getElementById("oid_walk").rows.length > 1
        ||  document.getElementById("oid_get").rows.length > 1)
      ){
       ck = "fail"
   }
   if (oid_checks()!= "ok") {
    ck = "fail"
  }
  return ck;
}

function oid_hides() {
  let x = document.getElementById("oid_div2");
  if (oid_snmp() == "ok") {
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }else{ alert("No, you missed snmp ");}
}

let input = 1;
function oid_add_get() {
  let x = document.getElementById("oid_get").rows.length ;
  if ((document.getElementById("Version").value) != "") {
    input = input +1;
    var table = document.getElementById("oid_get");
    var row = table.insertRow(x);
    row.id = "rowid_g"+input;
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);

    cell1.innerHTML = "<input  type='text' placeholder='Oid Get Var' class='form-control'  type='text' required>"
    +"        <div class='invalid-feedback'>No, you missed this one.</div>"
    cell2.innerHTML = "<input type='text' class='form-control' placeholder='Oid Get Value'  type='text' required>"
    +"        <div class='invalid-feedback'>No, you missed this one.</div>"
    cell3.innerHTML = "<button class='btn btn-secondary close'  onclick='oid_delete_get(\"rowid_g"+input+"\")'><i style='font-size:30px' class='material-icons'>remove_circle_outline</i></button>";

  }else{alert("No, you missed snmp")}

}
function oid_delete_get(tbip_id) {
  let rowIndex = document.getElementById(tbip_id).rowIndex
  document.getElementById("oid_get").deleteRow(rowIndex);
}
let input1 = 1;
function oid_add_walk() {
 let x = document.getElementById("oid_walk").rows.length ;
  if ((document.getElementById("Version").value) != "") {
    input1 = input1 +1;
    var table1 = document.getElementById("oid_walk");
    var row = table1.insertRow(x);
    row.id = "rowid_w"+input1;
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);

    cell1.innerHTML = "<input  type='text' placeholder='Oid Walk Var' class='form-control'  type='text' required>"
    +"        <div class='invalid-feedback'>No, you missed this one.</div>"
    cell2.innerHTML = "<input type='text' class='form-control' placeholder='Oid Walk Value'  type='text' required>"
    +"        <div class='invalid-feedback'>No, you missed this one.</div>"
    cell3.innerHTML = "<button class='btn btn-secondary close'  onclick='oid_delete_walk(\"rowid_w"+input1+"\")'><i style='font-size:30px' class='material-icons'>remove_circle_outline</i></button>";

  }else{alert("No, you missed snmp")}

}
function oid_delete_walk(tbip_id) {
  let rowIndex = document.getElementById(tbip_id).rowIndex
  document.getElementById("oid_walk").deleteRow(rowIndex);
}

function oid_checks() {
  var form = $("#oid_myForm")
  form.addClass('was-validated');
  if (form[0].checkValidity() === false) {
    return "fail";
  }
  else{
   return "ok";
 }
}
function oid_show(){
  if (oid_snmp()== "ok") {
   walk_ls =[]
   let x = document.getElementById("oid_walk").rows.length ;
   for (var i = 1; i < x; i++) {
     old_R = (document.getElementById("oid_walk").rows[i].cells[0].children[0].value);
     old_U = (document.getElementById("oid_walk").rows[i].cells[1].children[0].value);
     walk =  {var:old_R ,value:old_U}
     walk_ls.push(walk);
   }
   get_ls=[]
   let y = document.getElementById("oid_get").rows.length;
    for (var i = 1; i < y; i++){
     old_R = (document.getElementById("oid_get").rows[i].cells[0].children[0].value);
     old_U = (document.getElementById("oid_get").rows[i].cells[1].children[0].value);
     get =  {var:old_R ,value:old_U}
     get_ls.push(get);
   }
   oid_ls ={"get":get_ls, "walk":walk_ls}
   return oid_ls;
 }else{ alert("No, you missed.");}
}