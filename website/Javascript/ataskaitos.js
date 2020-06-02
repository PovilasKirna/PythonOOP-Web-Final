//change arrow directions on sort (sort function depreciated because of jquery implementation of datatables)
var direction = "asc";
function changeArrowDirection(n){
  var nameUP = 'i[name = "arrowUp'+n+'"';
  var nameDOWN = 'i[name = "arrowDown'+n+'"';
    //display arrow down or up
    if(direction == "asc"){
      $(nameUP).css({
        'display': 'inline'
      });
      $(nameDOWN).css({
        'display': 'none'
      });
      direction = "desc";
    } else if (direction == "desc"){
      $(nameUP).css({
        'display': 'none'
      });
      $(nameDOWN).css({
        'display': 'inline'
      });
      direction = "asc";
    }
    //remove other arrows
    var i;
    for(i = 0; i < 3; i++){
      var name_UP = 'i[name = "arrowUp'+i+'"';
      var name_DOWN = 'i[name = "arrowDown'+i+'"';
      if(i != n){
        $(name_UP).css({
          'display': 'none'
        });
        $(name_DOWN).css({
          'display': 'none'
        });
      }
    }
  }

//initiates the table
$(document).ready( function () {
  $('#mainTable').DataTable({
    "ajax": "convertDBtoJSON.php",
    "columns":[
      {"data":"Username"},
      {"data":"TimeCompleted"},
      {"data":"IsdavimoData"},
      {"data":"GrazinimoData"}
    ]
  });
});
