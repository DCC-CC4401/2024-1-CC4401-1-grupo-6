$(document).ready(function(){
    $("#buscador").keyup(function(){
        var query = $(this).val();
        if (query.length > 0) {
            $.ajax({
                url: "/search_courses",
                data: {
                    'search': query
                },
                dataType: 'json',
                success: function(data){
                    var resultsContainer = $("#results-container");
                    resultsContainer.empty().show();
                    if (data.length > 0) {
                        data.forEach(function(item){
                            var resultItem = $("<div class='result-item'></div>");
                            resultItem.text(item.nombre + " (" + item.codigo_curso + ")");
                            resultItem.click(function(){
                                $("#buscador").val(item.nombre);
                                resultsContainer.hide();
                            });
                            resultsContainer.append(resultItem);
                        });
                    } else {
                        resultsContainer.append("<p>No se encontraron resultados</p>");
                    }
                }
            });
        } else {
            $("#results-container").hide();
        }
    });

    // Hide results when clicking outside
    $(document).click(function(event) { 
        if(!$(event.target).closest('#buscador, #results-container').length) {
            if($('#results-container').is(":visible")) {
                $('#results-container').hide();
            }
        }        
    });
});

let submitBtn = document.getElementById("filters_button");
submitBtn.addEventListener("click", (event) => {
    event.preventDefault(); // Prevent the form from submitting immediately
    if (validateForm()) {
        document.getElementById("val-box").hidden = true;
        document.getElementById("filter_form").submit(); // Submit the form if the user confirms
    }
});

const validateName = (name) => {
    if (!name) return false;

    //length validation
    let lengthValid = name.length <= 200;

    //format validation
    let name_course = /^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]{0,200}$/
    let formatValid = name_course.test(name)

    return formatValid && lengthValid;
};

const validateForm = () => {
    let isValid = true;
    
    let name = document.getElementById("buscador").value;

    // validation auxiliary variables and function.
    let invalidInputs = [];
    const setInvalidInput = (inputName) => {
        invalidInputs.push(inputName);
        isValid = false;
    };
    if (!validateName(name)) {
        setInvalidInput(
            "El nombre debe tener entre 1 y 200 caracteres y solo puede contener letras y tildes"
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