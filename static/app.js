"use strict"

const $cupcakesList = $(".cupcakes-list");
const $addCupcakeForm = $("#add-cupcake-form");

const BASE_URL = "http://192.168.0.12:5001/api/cupcakes";  // robyns localhost: 192.168.0.12

/** Get list of cupcakes from API */
async function getCupcakesFromAPI(){
  const response = await axios({
    url:`${BASE_URL}`,
    method: 'GET'
  });
  const cupcakes = response.data.cupcakes;
  return cupcakes;
}

/** Get list of cupcakes from API and display on page */
async function start() {
  const cupcakes = await getCupcakesFromAPI();
  displayCupcakes(cupcakes);
}

/** Generate markup of cupcakes list */
function displayCupcakes(cupcakes){
  $cupcakesList.empty();

  for(let cupcake of cupcakes){
    $cupcakesList.append($(`<li class="list-group-item">
    <img src="${cupcake.image}" height=50px width=50px> - ${cupcake.size} ${cupcake.flavor}
    </li>`))
  };
}

/** Generate markup for new cupcake */
function updateCupcakesList(newCupcake){
  $cupcakesList.append($(`<li class="list-group-item">
  <img src="${newCupcake.image}" height=50px width=50px> - ${newCupcake.size} ${newCupcake.flavor}
  </li>`));
}

/** Add new cupcake to API */
async function postNewCupcake(cupcake){
  const response = await axios({
    url:`${BASE_URL}`,
    method: 'POST',
    data:{...cupcake}
  });

  const newCupcake = response.data.cupcake;
  return newCupcake;
}

/** Retrieves form data and calls functions to make new cupcake and update list */
async function addCupcake(evt){
  evt.preventDefault();
  // console.log("evt..",evt);
  const flavor = evt.target[0].value;
  const size = evt.target[1].value;
  const rating = evt.target[2].value;
  const image = evt.target[3].value;

  const cupcake = {flavor,size,rating,image};
  const newCupcake = await postNewCupcake(cupcake);
  updateCupcakesList(newCupcake);
}


/** Listens for add cupcake form submission and runs addCupcake function.*/
$addCupcakeForm.on("submit",addCupcake);


start();



