var http=require('http');
var https=require('https');
var url = require('url');

var listenAddress="http://127.0.0.1:8081";

//创建服务器
http.createServer(function(request,response) {
    //解析请求，包括文件名
    var uparse = url.parse(request.url)
    var pathname= uparse.pathname;
    var path = uparse.path;
    var filename = pathname.replace(/(^\/|\/$)/g,'');
    //输出请求的文件名
    console.log("Request for "+ pathname + "  received.");

    if(path.startsWith('/mpegts/')>0)
    {
	realUri=path.slice(8)
	console.log("RD: "+realUri)
        response.writeHead(200,{
		    'Content-Type': 'video/MP2T',
		    'Content-Disposition': 'attachment;filename='+filename+".ts"
	});
	sendJpgTs(realUri,response);
    }
    else if(path.startsWith('/m3u8/')>0)
    {
	headUri=listenAddress;
	realUri=path.slice(6)
	console.log("RM: "+realUri)
	console.log("RH: "+headUri);
        response.writeHead(200,{
		    'Content-Type': 'application/vnd.apple.mpegurl',
		    'Content-Disposition': 'attachment;filename='+filename+".m3u8"
	});
	sendM3U8(realUri,headUri,response);
    }
    else
    {
        response.end();
    }
}).listen(url.parse(listenAddress).port);

function sendM3U8(uri, headuri, response){
	var schema=url.parse(uri).protocol;
	var helper=http;
	if(schema=="https:")helper=https;
	return new Promise(function (resolve, reject) {
	var req = helper.get(uri, function(res) {
		res.setEncoding('utf8');
		console.log(res.headers);
		if ((res.headers["content-type"]!="application/vnd.apple.mpegurl") && (res.headers["content-type"]!="image/png"))
		{
			isClosed=true;
			response.end();
		}
		var m3u8="";
		res.on("data",(data)=>{
			m3u8+=data
		});
		res.on("end",()=>{
			var red="";
			//m3u8+=data;
			MArr=m3u8.split(/[(\r\n)\r\n]+/);
			MArr.forEach((item,index)=>{
				if(item.startsWith('#'))
				{
					red+=item+"\r\n";
				}else if(item.startsWith('http'))
				{
					if(item.indexOf(".m3u8")>0)
					{
						red+=headuri+"/m3u8/";
					}else
					{
						red+=headuri+"/mpegts/";
					}
					red+=item+"\r\n";
				}
			})
			response.write(red);
			response.end();
		});
	}).on("error",(e)=>{
		console.log('error');
	});
	});
}

function sendJpgTs(uri, response){
	var schema=url.parse(uri).protocol;
	var helper=http;
	if(schema=="https:")helper=https;
	return new Promise(function (resolve, reject) {
	var req = helper.get(uri, function(res) {
		var isClosed=false;
		var isFirstPkg=true;
		if (res.headers["content-type"]!="image/png")
		{
			isClosed=true;
			response.end();
		}
		res.on("data",(data)=>{
			if(!isClosed)
			{
				var tmp=data;
				if(isFirstPkg)
				{
					if((data[0]==0x89) && (data[1]==0x50) && (data[2]==0x4e) && (data[3]==0x47))
					{
						tmp[0]=0xff;
						tmp[1]=0xff;
						tmp[2]=0xff;
						tmp[3]=0xff;
					}
					isFirstPkg=false;
				}
				response.write(tmp);
			}
		});
		res.on("end",()=>{
			response.end();
		});
	}).on("error",(e)=>{
		console.log('error');
	});
	});
}

console.log('Server running at ' + listenAddress);
