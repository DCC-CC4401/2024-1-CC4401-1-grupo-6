$(document).ready(function () {
    $("#buscador").keyup(function () {
        var query = $(this).val();
        if (query.length > 0) {
            $.ajax({
                url: "/search_courses",
                data: {
                    'search': query
                },
                dataType: 'json',
                success: function (data) {
                    var resultsContainer = $("#results-container");
                    resultsContainer.empty().show();
                    if (data.length > 0) {
                        data.forEach(function (item) {
                            var resultItem = $("<div class='result-item'></div>");
                            resultItem.text(item.nombre + " (" + item.codigo_curso + ")");
                            resultItem.click(function () {
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
    $(document).click(function (event) {
        if (!$(event.target).closest('#buscador, #results-container').length) {
            if ($('#results-container').is(":visible")) {
                $('#results-container').hide();
            }
        }
    });
});