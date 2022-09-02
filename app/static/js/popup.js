var form = document.getElementById("newtask-form");
var modal = document.getElementById("modal");

function clearForm() {
    for (let x = 1; x < 4; x++) {
      form.elements[x].value = '';
    }
}

function openForm() {
  form.style.display = "flex";
  form.style.flexDirection = "column"  
  modal.style.display = "block";
}

function hidePopup() {
//  form.style.display = "none";
  modal.style.display = "none";
  clearForm();
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
    clearForm();
  }
}