var tabla = document.getElementById("tabla");
var filas = [];
var matriz = [];
var enlaces = ["http://gonthalo.github.io", "http://xkcd.com", "http://gonthalo.github.io/eSdlB.html"];
var colorines = ["rgb(5, 250, 100)", "rgb(5, 20, 200)", "white"]
var num_filas = 15;
var num_col = 15;

function iniciar(){
	for(var ii=0; ii<num_filas; ii++){
		tabla.innerHTML = tabla.innerHTML + '<tr id="fila' + ii +'"></tr>';
		matriz[ii] = [];
		aux = document.getElementById("fila" + ii);
		for (var jj=0; jj<num_col; jj++){
			aux.innerHTML = aux.innerHTML + '<td id="fil' + ii +'col' + jj + '"></td>';
			document.getElementById("fil" + ii +"col" + jj).innerHTML = '<input type="button" value="    " onclick="nada()" id="f' + ii +'c' + jj + '">';
			//document.getElementById("f" + ii +"c" + jj).background = "white";
			matriz[ii][jj] = "white";
		}
	}
}

function enlace(numero){
	window.location=enlaces[numero];
}

function boton(num, x0, y0){
	console.log([num, x0, y0]);
	document.getElementById("fil" + x0 + "col" + y0).innerHTML = '<input type="button" value="    " onclick="enlace(' + num + ')">';
	matriz[x0][y0] = colorines[num];
	document.getElementById("fil" + x0 + "col" + y0).style.backgroundColor = colorines[num];
}

function actualizar(){
	r = parseInt(Math.random()*num_col*num_filas);
	c = matriz[r%num_filas][parseInt(r/num_filas)];
	for(var tt=0; tt<num_filas*num_col; tt++){
		if(matriz[tt%num_filas][parseInt(tt/num_filas)]==c && tt!=r){
			k = parseInt(Math.random()*enlaces.length);
			boton(k, r%num_filas, parseInt(r/num_filas));
			return
		}
	}
}

function nada(){}

iniciar();
boton(0, 2, 3);
window.setInterval(actualizar, 200);
