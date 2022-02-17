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

  try {
    ksub = f("k2").slice(-1);
    while (!![]) {
      t2 = new Date().getTime();
      if (t2.toString().slice(-3).indexOf(ksub) >= 0x0) {
        f2("t2", t2);
        break;
      }
    }
  } catch (e) {}


//PCK2

