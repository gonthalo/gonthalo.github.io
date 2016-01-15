var tabla = document.getElementById("tabla");
var filas = [];
var matriz = [];

function iniciar(){
	for(var ii=0; ii<5; ii++){
		tabla.innerHTML = tabla.innerHTML + '<tr id="fila' + ii +'"></tr>';
		matriz[ii] = [];
		aux = document.getElementById("fila" + ii);
		for (var jj=0; jj<5; jj++){
			aux.innerHTML = aux.innerHTML + '<td id="fil' + ii +'col' + jj + '"></td>';
			matriz[ii][jj] = document.getElementById("fil" + ii +"col" + jj);
			matriz[ii][jj].innerHTML = "Hola!";
		}
	}
}

function boton(strin, x0, y0){
	document.getElementById("fil" + x0 + "col" + y0).innerHTML = '<input type="button" value="" onclick="' + strin + '">';
}

function nada(){}

iniciar();

function enlace(){
	window.location="http://gonthalo.github.io";
}

boton("enlace()", 2, 3);
