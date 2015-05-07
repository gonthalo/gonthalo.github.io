function nada(){};
//function boton(numero){
//	function nuevoton(){
//
//	}
//	for (var bla=1; bla<=numero; bla++){
//		nuevoton();
//	}
//}
//function aprieta_boton(){}
function edad(){
	var fecha = Date();
	var lista = [31,28,31,30,31,30,31,31,30,31,30,31];
	var dia = fecha.getDate() - 24;
	var mes = fecha.getMonth() - 12;
	var anio = fecha.getFullYear() - 1997;
	if (dia<0){
		dia = dia + lista[mes + 11];
		mes = mes - 1;
	}
	if (mes<0){
		mes = mes + 12;
		anio = anio - 1;
	}
	alert ("Mi edad es de " + anio + " años");
}
