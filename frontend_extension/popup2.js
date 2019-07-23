$(document).ready(function(){
    $("#printEmergency").click(function(){

        var $input = "EMERGENCY"+ $("#input").val();
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
           document.getElementById("url1").textContent=datalist[3];
           document.getElementById("url2").textContent=datalist[4];
           
          var icon1 = document.getElementById('liveicon1');
          var icon2 = document.getElementById('liveicon2');
          var display1 = icon1.style.display;
          var display2 = icon2.style.display;
          if (display1 == 'none'){
            icon1.style.display = 'block';
          }
          if (display2 == 'none'){
            icon2.style.display = 'block';
          }
          }

        
    });
});

});