const validatePassword = (password) => {
    if (!password) return false;
    //length validation
    let lengthValid = password.length >= 8 && password.length <= 20;
    //format validation
    let re2 = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
    let formatValid = re2.test(password);
    return formatValid && lengthValid;
}

const validateForm = () => {
    let isValid = true;
    let password = document.getElementById("password").value;
    let password2 = document.getElementById("password2").value;

    let invalidInputs = [];
    const setInvalidInput = (inputName) => {
        invalidInputs.push(inputName);
        isValid = false;
    };

    if (!validatePassword(password)) {
        setInvalidInput(
            "La contraseña debe cumplir con los siguientes requisitos:\n- Debe tener entre 8 y 20 caracteres\n- Debe contener al menos una letra minúscula\n- Debe contener al menos una letra mayúscula\n- Debe contener al menos un número\n- Debe contener al menos un caracter especial (!@#$%^&*)"
        );
    }
    if (password != password2) {
        setInvalidInput(
            "Las contraseñas no coinciden"
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

let submitBtn = document.getElementById("LoginNewPassword_button");
submitBtn.addEventListener("click", validateForm);
