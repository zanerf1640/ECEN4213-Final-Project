if (!!window.EventSource) {
    var source = new EventSource('/');
    source.onmessage = function(e) {
      var bumper = e.data[1]
      var cliff = e.data[3];
      var drop = e.data[5];


      // finish the code to handle the bumper status
      let b1 = document.getElementById("but1")
        if (bumper=="0")
          {
            document.getElementById("but1").value = "OFF";
            b1.style.backgroundColor = "green"
          }
        if (bumper=="1")
        {
          document.getElementById("but1").value = "Right";
          b1.style.backgroundColor = "red"
        }
        if (bumper=="2")
        {
          document.getElementById("but1").value = "Center"
          b1.style.backgroundColor = "red"
        }
        if (bumper=="4")
        {
          document.getElementById("but1").value = "Left"
          b1.style.backgroundColor = "red"
        }
         
        
        // finish the code to handle the wheel drop status
        let b2 = document.getElementById("but2")
      if (drop=="0")
        {
          document.getElementById("but2").value = "OFF";
          b2.style.backgroundColor = "green"
        }
      if (drop=="1")
        {
          document.getElementById("but2").value = "Right";
          b2.style.backgroundColor = "red"
        }
      if (drop=="2")
        {
          document.getElementById("but2").value = "Left"
          b2.style.backgroundColor = "red"
        }
      if (drop=="3")
      {
        document.getElementById("but2").value = "Both"
        b2.style.backgroundColor = "red"
      }

      // finish the code to handle cliff status
      let b3 = document.getElementById("but3") 
      if (cliff=="0")
        {
          document.getElementById("but3").value = "OFF";
          b3.style.backgroundColor = "green"
        }
      if (cliff=="1")
        {
          document.getElementById("but3").value = "Right";
          b3.style.backgroundColor = "red"
        }
      if (cliff=="2")
        {
          document.getElementById("but3").value = "Center";
          b3.style.backgroundColor = "red"
        }
      if (cliff=="4")
        {
          document.getElementById("but3").value = "Left";
          b3.style.backgroundColor = "red"
        }

    }
  }