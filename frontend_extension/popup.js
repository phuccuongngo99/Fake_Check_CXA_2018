$(document).ready(function(){
    $("#printOutput").click(function(){

        var $input = $("#input").val();
        var $shout = $.ajax({
          type: 'POST',
          url: "http://127.0.0.1:5000/",
          data: {'message':$input},
          success: function(data){
             var datalist = data.split(";;;"); 
          $("#demo").text(datalist[0]);


          function move1(num) {
             var elem = document.getElementById("myBar1");   
             var width = 0;
             var id = setInterval(frame, 10);
             function frame() {
               if (width >= num) {  //the 90 here is the percentage that we are supposed to take in
                clearInterval(id);
              } else {
                  width++; 
                  elem.style.width = width + '%'; 
                  elem.textContent = 'Credibility: '+ width * 1  + '%';
                }
              }
           }
           function move2(num) {
             var elem = document.getElementById("myBar2");   
             var width = 0;
             var id = setInterval(frame, 10);
             function frame() {
               if (width >= num) {  //the 90 here is the percentage that we are supposed to take in
                clearInterval(id);
              } else {
                  width++; 
                  elem.style.width = width + '%'; 
                  elem.textContent = 'Sentiment:' + width * 1  + '%';
                }
              }
           }
           function move3(num) {
             var elem = document.getElementById("myBar3");   
             var width = 0;
             var id = setInterval(frame, 10);
             function frame() {
               if (width >= num) {  //the 90 here is the percentage that we are supposed to take in
                clearInterval(id);
              } else {
                  width++; 
                  elem.style.width = width + '%'; 
                  elem.textContent = 'Level of Support' + width * 1  + '%';
                }
              }
           }
           move1(parseInt(datalist[0]));
           move2(parseInt(datalist[1]));
           move3(parseInt(datalist[2]));
           document.getElementById("stand1").textContent=datalist[3];
           document.getElementById("stand2").textContent=datalist[6];
           document.getElementById("stand3").textContent=datalist[9];
           document.getElementById("stand4").textContent=datalist[12];
           document.getElementById("stand5").textContent=datalist[15];
           document.getElementById("url1").textContent=datalist[4];
           document.getElementById("url2").textContent=datalist[7];
           document.getElementById("url3").textContent=datalist[10];
           document.getElementById("url4").textContent=datalist[13];
           document.getElementById("url5").textContent=datalist[16];
           var progress1 = document.getElementById("progress1");
           progress1.style.width = datalist[5];
           var progress2 = document.getElementById("progress2");
           progress1.style.width = datalist[8];
           var progress3 = document.getElementById("progress3");
           progress1.style.width = datalist[11];
           var progress4 = document.getElementById("progress4");
           progress1.style.width = datalist[14];
           var progress5 = document.getElementById("progress5");
           progress1.style.width = datalist[17];
           
          
          }

        
    });
});

});