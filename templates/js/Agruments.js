function Agruments_hides() {
   if (Agruments_checks() == "ok") {
  let x = document.getElementById("Agruments_div2");
   Agruments_checks();
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }else{alert("No, you missed.")}
}

let Agruments_input = 1;
function Agruments_add() {
    let x = document.getElementById("Agruments_table").rows.length ;
    Agruments_input = Agruments_input +1;
    var table = document.getElementById("Agruments_table");
    var row = table.insertRow(x);
    row.id = "rowid_Agruments"+Agruments_input;
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);

      cell1.innerHTML = "<input  type='text' class='form-control' type='text' required>"
     cell2.innerHTML ='<select class="form-control" >'
    +'         <option value="int">int</option>'
    +'         <option value="float">float</option>'
    +'         <option value="string">string</option>'
    +'         <option value="list">list</option>'
    +'         <option value="regex">regex</option>'
    +'</select> '
    
    cell3.innerHTML = "<input type='text' class='form-control' type='text' >"
    cell4.innerHTML = "<input type='text' class='form-control' type='text' >"
    cell5.innerHTML = "<button class='btn btn-secondary close'  onclick='Agruments_delete(\"rowid_Agruments"+Agruments_input+"\")'><i style='font-size:30px' class='material-icons'>remove_circle_outline</i></button>";
}
function Agruments_delete(tbip_id) {
  let rowIndex = document.getElementById(tbip_id).rowIndex
  document.getElementById("Agruments_table").deleteRow(rowIndex);
}

function Agruments_checks() {
  var form = $("#Agruments_myForm")
  form.addClass('was-validated');
  if (form[0].checkValidity() === false) {
    return "fail";
  }
  else{
   return "ok";
 }
}

function Agruments_show(){
 Agruments_ls =[]
   let x = document.getElementById("Agruments_table").rows.length ;
   for (var i = 1; i < x; i++) {
     AG_var = (document.getElementById("Agruments_table").rows[i].cells[0].children[0].value);
     AG_type = (document.getElementById("Agruments_table").rows[i].cells[1].children[0].value);
     AG_val = (document.getElementById("Agruments_table").rows[i].cells[2].children[0].value);
     AG_condition = (document.getElementById("Agruments_table").rows[i].cells[3].children[0].value);
     Agrum =  {var:AG_var,type:AG_type ,val:AG_val ,cond:AG_condition }
     Agruments_ls.push(Agrum);
   }
 
  return Agruments_ls;
}
