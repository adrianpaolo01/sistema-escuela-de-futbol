// Leer JSON desde el HTML
const alumnos = JSON.parse(
    document.getElementById("alumnos-data").textContent
);

// Elementos
const input = document.getElementById("buscador");
const resultados = document.getElementById("resultados");
const inputId = document.getElementById("alumno_id");

// Escuchar cuando el usuario escribe
input.addEventListener("input", function(){
    //Texto que escribe el usuario
    let texto = input.value.toLowerCase();

    // Limpiar resultados anteriores
    resultados.innerHTML = "";

    //Si está vacio, no mostrar nada
    if(texto == "") return;

    // Filtro alumnos
    let filtrados = alumnos.filter(alumno =>
        alumno.nombre.toLowerCase().includes(texto)
    );

    // Recorrer resultados
    filtrados.forEach(alumno => {

        // Crear div para cada resultado
        let div = document.createElement("div");
        div.textContent = alumno.nombre;

        //Estilo basico
        div.classList.add("item");

        // Cuando haces click
        div.addEventListener("click", function(){

            // Mostrar nombre de input
            input.value = alumno.nombre;

            // Guardar ID (IMPORTANTE)
            inputId.value = alumno.id;

            //Limpiar resultados
            resultados.innerHTML = "";
        });

        //Agregar al contenedor
        resultados.appendChild(div);
    });
})