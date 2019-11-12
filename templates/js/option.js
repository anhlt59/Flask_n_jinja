option_ls_C = [];
  function option_lc(ts) {
         let ck = ""
    for (var i = option_ls_C.length - 1; i >= 0; i--) {

      if (option_ls_C[i] == ts.value) {
        ck = "no"
      }
    }
    if (ck != "no") {
      if (ts.value != "") {
        option_ls_C.push(ts.value);
      }else{ option_ls_C = [];}
    }else{
      var index = option_ls_C.indexOf(ts.value);
    if (index > -1) {
      option_ls_C.splice(index, 1);
      }
    }
    document.getElementById("option_lc_S").value = option_ls_C;
 }

  function option_hides() {
    if (option_checks()=="ok") {
      let x = document.getElementById("option_div2");
      if (x.style.display === "none") {
        x.style.display = "block";
      } else {
        x.style.display = "none";

      }}else{ alert("No, you missed.");}
    }

    let option_v = 1;
    function option_add() {
      option_v = option_v +1;
      var table = document.getElementById("option");
      var row = table.insertRow(1);
      row.id = "rowid_"+option_v;
      var cell1 = row.insertCell(0);
      var cell2 = row.insertCell(1);
      var cell3 = row.insertCell(2);
      var cell4 = row.insertCell(3);
      var cell5 = row.insertCell(4);
      var cell6 = row.insertCell(5);
      var cell7 = row.insertCell(6);
      cell1.innerHTML = "<input type='text' class='form-control' placeholder='option' required>";
      cell2.innerHTML = "<input type='text' class='form-control'   placeholder='dest' >";
      cell3.innerHTML = "<input type='text' class='form-control'   placeholder='type' >";
      cell4.innerHTML = "<input type='text' class='form-control'   placeholder='help' >";
      cell5.innerHTML = "<input type='text' class='form-control'   placeholder='metavar' >";
      cell6.innerHTML = "<input type='text' class='form-control'   placeholder='Default' >";
      cell7.innerHTML = "<button class='btn btn-secondary close'  onclick='option_delete(\"rowid_"+option_v+"\")'><i style='font-size:30px' class='material-icons'>remove_circle_outline</i></button>";

    }
    function option_delete(tbip_id) {
      let rowIndex = document.getElementById(tbip_id).rowIndex
      document.getElementById("option").deleteRow(rowIndex);
    }

    function option_checks() {
      var form = $("#option_myForm")
      form.addClass('was-validated');
      if (form[0].checkValidity() === false) {
        return "fail";
      }
      else{
       return "ok";
     }
   }
   function option_show(){
     option_list = option_ls_C;
     let x = document.getElementById("option").rows.length;
     for (var i = x - 1; i > 0; i--) {
       opti = (document.getElementById("option").rows[i].cells[0].children[0].value);
       dest = (document.getElementById("option").rows[i].cells[1].children[0].value);
       typ  = (document.getElementById("option").rows[i].cells[2].children[0].value);
       help = (document.getElementById("option").rows[i].cells[3].children[0].value);
       meta = (document.getElementById("option").rows[i].cells[4].children[0].value);
       defa = (document.getElementById("option").rows[i].cells[5].children[0].value);

       option_s = {'option':opti,'dest':dest,'type':typ,'help':help,'metavar':meta,'default':defa}
       option_list.push(option_s);
     }
     return option_list;
   }

