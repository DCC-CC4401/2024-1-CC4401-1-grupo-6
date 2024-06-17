const validatePoster = (poster) => {
  if (!poster) return false;

  // file type validation
  let typeValid = true;

  // file.type should be image/<foo> or application/pdf
  let fileFamily = poster.type.split("/")[0];
  typeValid &&= fileFamily == "image" || poster.type == "application/pdf";

  return typeValid;
};

const validateDescription = (description) => {
  //length validation
  let lengthValid = description.length <= 200;

  return lengthValid;
};

const validateName = (name) => {
  if (!name) return false;

  //length validation
  let lengthValid = name.length >= 1 && name.length <= 200;

  //format validation
  let re2 = /^[\w.\sáéíóúÁÉÍÓÚñÑüÜ]+$/; // Cualquier string que incluya tildes y otros caracteres especiales
  let formatValid = re2.test(name);
  return formatValid && lengthValid;
};

const validatePrice = (price) => {
  if (!price) return false;
  //length validation
  let maxValue = 999999999;

  if (price > 0 && price <= maxValue) return true;

  return false;
};

const validatePhoneNumber = (phoneNumber) => {
  if (!phoneNumber) return false;
  //length validation
  let minValue = 900000000;
  let maxValue = 999999999;

  if (phoneNumber >= minValue && phoneNumber <= maxValue) return true;

  return false;
};

const validateHour = (hour) => {
  if (!hour) return false;

  let re3 = /^([01]?[0-9]|2[0-3]):([0-5][0-9])$/;
  let formatValid = re3.test(hour);
  return formatValid;
};

const validateForm = () => {
  let isValid = true;
  // get elements from DOM by using id's.
  let poster = document.getElementById("id_url").files[0];
  let description = document.getElementById("id_descripcion").value;
  let name = document.getElementById("id_nombre").value;
  // let courses = document.getElementById("id_courses");
  let price = document.getElementById("id_price").value;
  // let modality = document.getElementById("id_modality");
  let phone = document.getElementById("id_phone").value;
  // let disponibility = document.getElementById("id_disponibility");
  let time_init = document.getElementById("id_time_init").value;
  let time_end = document.getElementById("id_time_end").value;

  // validation auxiliary variables and function.
  let invalidInputs = [];
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid = false;
  };

  // validation logic
  if (!validatePoster(poster)) {
    setInvalidInput(
      "Suba un archivo de tipo imagen o pdf para el poster del curso"
    );
  }
  if (!validateDescription(description)) {
    setInvalidInput("Escriba una descripción de máximo 200 caracteres");
  }
  if (!validateName(name)) {
    setInvalidInput("Escriba un nombre de máximo 200 caracteres");
  }
  if (!validatePrice(price)) {
    setInvalidInput(
      "Ingrese un precio mayor o igual a 0 y menor o igual a 999999999"
    );
  }
  if (!validatePhoneNumber(phone)) {
    setInvalidInput("Número de teléfono, debe tener 9 dígitos sin código zona");
  }
  if (!validateHour(time_init)) {
    setInvalidInput("Hora de inicio debe ser en formato HH:MM");
  }
  if (!validateHour(time_end)) {
    setInvalidInput("Hora de término debe ser en formato HH:MM");
  }

  // finally display validation
  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");

  if (!isValid) {
    validationListElem.textContent = "";
    // add invalid elements to val-list element.
    for (input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    }
    // set val-msg
    validationMessageElem.innerText = "Los siguiente campos son inválidos:";

    // make validation prompt visible
    validationBox.hidden = false;
    return false; // Form is not valid
  }

  return true; // Form is valid
};

let submitBtn = document.getElementById("publish_button");
submitBtn.addEventListener("click", (event) => {
  event.preventDefault(); // Prevent the form from submitting immediately
  if (validateForm()) {
    document.getElementById("val-box").hidden = true;
    document.getElementById("confirmation-box").hidden = false;
  }
});

let confirmBtn = document.getElementById("confirm_button");
confirmBtn.addEventListener("click", () => {
  document.getElementById("publish_form").submit(); // Submit the form if the user confirms
});

let cancelBtn = document.getElementById("cancel_button");
cancelBtn.addEventListener("click", () => {
  document.getElementById("confirmation-box").hidden = true;
});
