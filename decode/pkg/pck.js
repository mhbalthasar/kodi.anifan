  f = function (arg1) {
    var restr = new RegExp("(^| )" + arg1 + "=([^;]*)(;|$)");
    if ((cook = document.cookie.match(restr))) {
      return unescape(cook[2]);
    } else {
      return null;
    }
  };
  f2 = function (arg1, arg2) {
    var dateObj = new Date();
    dateObj.setTime(dateObj.getTime()+(30*24*60*60*1000));
    document.cookie =arg1+"="+escape(arg2)+";expires=" + dateObj.toGMTString() + ";path=/";
  };

  t1 = Math["round"](Number(f("t1")) / 1000) >> 0x5;

  f2("k2", (t1 * (t1 % 0x1000) + 0x99d6) * (t1 % 0x1000) + t1);

  f2("t2", new Date()["getTime"]());


//pck1 (next:pck2)


var cT1=getCookie("t1")
tT1 = round(cT1 / 1000) >> 5; //有符号右位移
k2 = ( tT1 * ( tT1 % 4096 ) + 39382 ) * ( tT1 % 4096) + tT1
//t2 = new Date().getTime() 
t2 = time.time() * 1000 //Python use this


