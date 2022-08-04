function openTab(target, tabName) {
  // Declare all variables
    let i, tabcontent, tablinks;
    
    // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";
  //evt.currentTarget.className += " active";
  if (target == '') {
    tablinks[0].className += " active";
  } else {
    target.className += " active";
  }
   
}


function updateBlocks() {

  let sensorBlock = document.getElementById('sensor_names');
  let csvBlock = document.getElementById('csv_group');

  let csvButton = document.getElementById('csvRadioInput')
  if (csvButton.checked && sensorBlock.className == 'control-group') {
      csvBlock.className = csvBlock.className.replace(" hidden", "");
      sensorBlock.className  += " hidden";

  } else if (!csvButton.checked && csvBlock.className == 'control-group'){
      csvBlock.className  += " hidden";
      sensorBlock.className = sensorBlock.className.replace(" hidden", "");
  }
}

const radioButtons = document.getElementsByClassName('control control--radio');
for (i = 0; i < radioButtons.length; i++) {
    radioButtons[i].addEventListener('click', updateBlocks);
}


function submitDataToFlask() {
  let url = '/generateData';
    let formObj = document.getElementById("mainForm");
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

const submitDataButton = document.getElementById('submitData')
submitDataButton.addEventListener('click', submitDataToFlask)