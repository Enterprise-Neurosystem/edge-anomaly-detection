function displayGraph(){
    let url = '/generateData/0';
    let formObj = document.getElementById("postgresForm");
    let formData = new FormData(formObj);
    postTestRequest(url, formData)
        .then()
        .catch(error => console.error(error))
}


async function postTestRequest(url, formData) {
    return fetch(url, {
        method: 'POST',
        body: formData
    })
        .then((response) => response.text());
}

function updateBlocks() {
    alert('*********');
    
    let sensorBlock = document.getElementById('sensor_names');
    let csvBlock = document.getElementById('csv_group');
    if (radioButtons.checked) {

        csvBlock.className = csvBlock.className.replace(" hidden", "");
        sensorBlock.className  += " hidden";

    } else {

        csvBlock.className  += " hidden";
        sensorBlock.className = sensorBlock.className.replace(" hidden", "");
    }
}
const radioButtons = document.getElementsByClassName('control control--radio');
for (i = 0; i < radioButtons.length; i++) {
    radioButtons[i].addEventListener('click', updateBlocks);
}

const graphBtnObj = document.getElementById("startPlotBtn");
graphBtnObj.addEventListener("click", displayGraph);
