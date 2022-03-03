/* CODIGO QUE REALIZA LA PAGINA (detalle.html) APENAS ARRANCA*/ 
var posicion;
window.onload = function() {
    var code = document.getElementById("codigo").innerHTML;
    var ruta = document.getElementById("ruta").innerHTML;
    var foto = document.getElementById("foto");
    //foto.src = "/static/img/Productos/"+code+"/"+code+"_1.jpg";
    //foto.src = ruta+"Div1/"+code+"/"+code+"_1.jpg";

    if (parseInt(code,10) <= 67388){
        foto.src = ruta+"Div1/"+code+"/"+code+"_1.jpg";
        posicion=1
    }
    else if (parseInt(code,10) <= 256642){
        foto.src = ruta+"Div2/"+code+"/"+code+"_1.jpg";
        posicion=2
    }
    else if (parseInt(code,10) <= 257179){
        foto.src = ruta+"Div3/"+code+"/"+code+"_1.jpg";
        posicion=3
    }
    else if (parseInt(code,10) <= 1008023){
      foto.src = ruta+"Div4/"+code+"/"+code+"_1.jpg";
      posicion=4
    }
    else if (parseInt(code,10) <= 66661102){
      foto.src = ruta+"Div5/"+code+"/"+code+"_1.jpg";
      posicion=5
    }
    else if (parseInt(code,10) <= 77770108){
      foto.src = ruta+"Div6/"+code+"/"+code+"_1.jpg";
      posicion=6
    }
}

function Error() {
    var foto = document.getElementById("foto");
    foto.src = "https://raw.githubusercontent.com/NickCracker/Global/main/static/img/image-not-found.png";
    //foto.src = "/static/img/Productos/"+code+"/"+code+"_1.jpg";
    }

var num = 1;

function siguiente(){
    num++;
    if (num>3){
        num=1;
    }
    var code = document.getElementById("codigo").innerHTML
    var foto = document.getElementById("foto");
    foto.src = "https://raw.githubusercontent.com/NickCracker/Global/main/assets/Div"+posicion+"/"+code+"/"+code+"_"+num+".jpg";
}

function anterior(){
    num--;
    if (num<1){
        num=1;
    }
    var code = document.getElementById("codigo").innerHTML
    var foto = document.getElementById("foto");
    foto.src = "https://raw.githubusercontent.com/NickCracker/Global/main/assets/Div"+posicion+"/"+code+"/"+code+"_"+num+".jpg";
}

