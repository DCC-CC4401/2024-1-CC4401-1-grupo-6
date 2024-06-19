const validateName = (name) => {
    if (!name) return false;
    //length validation
    let lengthValid = name.length >= 1 && name.length <= 50;
    //format validation
    let re2 = /^[A-Za-zÁÉÍÓÚáéíóúÑñÜü]+(?:\s(de|del|de la)\s[A-Za-zÁÉÍÓÚáéíóúÑñÜü]+|(?:\s[A-Za-zÁÉÍÓÚáéíóúÑñÜü]+))+$/;// Cualquier string que incluya tildes y otros caracteres especiales
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
    
    let name = document.getElementById("name").value;
    let username = document.getElementById("username").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let password2 = document.getElementById("password2").value;

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

let submitBtn = document.getElementById("sendForm");
submitBtn.addEventListener("click", (event) => {
    event.preventDefault(); // Prevent the form from submitting immediately
    if (validateForm()) {
        document.getElementById("val-box").hidden = true;
        document.getElementById("confirmation-box").hidden = false;
    }
});
let confirmBtn = document.getElementById("confirm_button");
confirmBtn.addEventListener("click", () => {
    document.getElementById("register_form").submit(); // Submit the form if the user confirms
});

let cancelBtn = document.getElementById("cancel_button");
cancelBtn.addEventListener("click", () => {
    document.getElementById("confirmation-box").hidden = true;
});