
var queryString = window.location.href;
queryString = queryString.replace('resultpage.html?sentence=','');
var input = queryString;
var $shout = $.ajax({
    type: 'POST',
    url: "https://infocommsociety.com:5000/",
    data: {'message':input},
    success: function(data){ 
    $("#demo").text(data);
    }
}, true);


      