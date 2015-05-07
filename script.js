function nada(){}
function boton(var numero){
	function nuevoton(){

	}
	for (var bla=1; bla<=numero; bla++){
		nuevoton();
	}
}
function aprieta_boton(){}
function edad(){
	var lista = [31,28,31,30,31,30,31,31,30,31,30,31]
	var dia = getDate(); - 24
	var mes = getMonth(); - 12
	var anio = getFullYear() - 1997;
	if (dia<0){
		dia = dia + lista[getMonth()-1];
		mes = mes - 1;
	}
	if (mes<0){
		mes = mes + 12;
		anio = anio - 1;
	}
	var str1;
	var srt2;
	alert ("Mi edad es de " + anio + " años");
}
