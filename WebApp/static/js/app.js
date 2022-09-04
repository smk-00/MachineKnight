const filePicker = document.getElementById('pickingarea');
let fileInput = filePicker.querySelector(".file-input")
const uploadedArea = document.querySelector(".uploaded-area");

filePicker.addEventListener("click", () => {
    fileInput.click();
});

fileInput.onchange = ({target})=>{
    let file = target.files[0];
    if(file){
      let fileName = file.name;
      if(fileName.length >= 12){
        let splitName = fileName.split('.');
        fileName = splitName[0].substring(0, 13) + "... ." + splitName[1];
      }
      uploadFile(fileName);
    }
  }
  
  function uploadFile(name){
    let uploadedHTML = `<li class="area-row">
    <div class="content">
      <i class="fas fa-file-alt"></i>
      <div class="details">
        <span class="name">${name} • Uploaded</span>
      </div>
    </div>
    <i class="fas fa-check"></i>
  </li>`;
uploadedArea.insertAdjacentHTML("afterbegin", uploadedHTML);
  }