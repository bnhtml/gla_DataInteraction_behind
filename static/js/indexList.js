
    var box=document.getElementById("content_con");
        var box2=document.getElementById("content_right_con");
        var con1=document.getElementById("con1");
        var con12=document.getElementById("con12");
        var con2=document.getElementById("con2");
        var con22=document.getElementById("con22");
        var speed=50;
        con2.innerHTML=con1.innerHTML;
        function  ScrollUp(){
            if( box.scrollTop >= con1.scrollHeight){
                box.scrollTop=0;
            }else
                box.scrollTop++;
        }

        var i=setInterval("ScrollUp()",speed);
        function Stop(){
            clearInterval(i);
        }
        function Up(){
            i=setInterval("ScrollUp()",speed);
        }



        con22.innerHTML=con12.innerHTML;
        function  ScrollUp2(){
            if( box2.scrollTop>=con12.scrollHeight){
                box2.scrollTop=0;
            }else
                box2.scrollTop++;
        }


        var j=setInterval("ScrollUp2()",speed);
        function Stop2(){
            clearInterval(j);
        }
        function Up2(){
            j=setInterval("ScrollUp2()",speed);
        }


