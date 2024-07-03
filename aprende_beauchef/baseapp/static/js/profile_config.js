const validateName = (name) => {
    if (!name) return false;

    //length validation
    let lengthValid = name.length >= 1 && name.length <= 50;

    //format validation
    let re2 = /^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$/; // Cualquier string que incluya tildes y otros caracteres especiales
    let formatValid = re2.test(name);

    return formatValid && lengthValid;
};

const validateUsername = (username) => {
    if (!username) return false;
    //length validation
    let lengthValid = username.length >= 1 && username.length <= 20;
    //format validation
    let re2 = /^[A-Za-z0-9_!@#&$]+$/; // Cualquier string que incluya tildes y otros caracteres especiales
    let formatValid = re2.test(username);
    return formatValid && lengthValid;
}

const validateEmail = (email) => {
    if (!email) return false;
    //length validation
    let lengthValid = email.length >= 1 && email.length <= 50;
    //format validation
    let re2 = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/; // cualquier email
    let formatValid = re2.test(email);
    return formatValid && lengthValid;
}

const validateForm = () => {
    let isValid = true;

    let name = document.getElementById("name").value;
    let username = document.getElementById("username").value;
    let email = document.getElementById("email").value;

    // validation auxiliary variables and function.
    let invalidInputs = [];
    const setInvalidInput = (inputName) => {
        invalidInputs.push(inputName);
        isValid = false;
    };

    if (!validateName(name)) {
        setInvalidInput(
            "El nombre debe tener entre 1 y 50 caracteres y solo puede contener letras y tildes"
        );
    }
    if (!validateUsername(username)) {
        setInvalidInput(
            "El nombre de usuario debe tener entre 1 y 20 caracteres y solo puede contener letras, números y los caracteres especiales !@#&$, no se permiten espacios"
        );
    }

    if (!validateEmail(email)) {
        setInvalidInput(
            "El email debe tener entre 1 y 50 caracteres y debe tener formato de email (usuario@dominio.com)"
        );
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
}

let submitBtn = document.getElementById("ProfileConfigButton");
submitBtn.addEventListener("click", validateForm);