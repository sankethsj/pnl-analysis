//selecting all required elements
const dropArea = document.querySelector(".drag-area"),
    dragText = dropArea.querySelector("header"),
    button = dropArea.querySelector("button"),
    input = dropArea.querySelector("input")
    analyze = document.getElementById('analyze-btn');

let file;

button.onclick = () => {
    input.click();
}

input.addEventListener("change", function () {
    //getting user select file and [0] this means if user select multiple files then we'll select only the first one
    file = this.files[0];
    dropArea.classList.add("active");
    showFile(); //calling function
});


//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropArea.classList.add("active");
    dragText.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
});

//If user drop File on DropArea
dropArea.addEventListener("drop", (event) => {
    event.preventDefault();
    file = event.dataTransfer.files[0];
    showFile(); //calling function
});

function showFile() {

    //getting selected file type
    let fileType = file.type;
    console.log(file);

    if (file.size > 2 * 1024 * 1024) {
        dragText.textContent = "Max allowed file size is 2MB";
        dragText.style.color = 'red';
        setTimeout(() => {
            dragText.textContent = "Drag & Drop to Upload File";
            dragText.style.color = 'rgb(134, 134, 134)';
        }, 3000);
        return
    }

    //adding some valid image extensions in array
    let validExtensions = ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"];

    if (validExtensions.includes(fileType)) {

        console.log("File is valid and uploading...")

        dropArea.classList.remove("active");
        dragText.textContent = "Uploading...";
        dragText.style.color = 'green';
        
        let formData = new FormData();
     
        formData.append("file", file);

        fetch('/uploadreport', {method: "POST", body: formData})
        .then((res)=>res.json())
        .then(
            (res) => {
                console.log(res);
                analyze.href = 'analyze/'+ res.report_filepath;
                analyze.style.backgroundColor = 'black';
                analyze.style.cursor = 'pointer';
                dragText.textContent = "File Uploaded";
                dragText.style.color = 'green';
            }
        ).catch((err)=>{
            console.log(`Error occured : ${err}`)
            dragText.textContent = `Error occured : ${err}`;
            dragText.style.color = 'red';
        })

    } else {
        dropArea.classList.remove("active");
        dragText.textContent = "Currently supports only excel file (.xlsx)";
        dragText.style.color = 'red';
        setTimeout(() => {
            dragText.textContent = "Drag & Drop to Upload File";
            dragText.style.color = 'rgb(134, 134, 134)';
        }, 3000);
        return
    }
}