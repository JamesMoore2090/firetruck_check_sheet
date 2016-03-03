var counter = 2;
function addInput(divName){
          var newdiv = document.createElement('div');
        //   var newcounter = document.getElementById('counter');
          newdiv.innerHTML = "Chapter " + (counter) + " <br><input type='text' name='Chapter_'" + (counter)">";
          document.getElementById(divName).appendChild(newdiv);
          document.getElementById('counter').setAttribute('value', counter)
          
          counter++;
     
}