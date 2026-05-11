function checkURL(){

let url=document.getElementById("urlInput").value;

if(url.includes("@") || url.includes("http://")){
document.getElementById("result").innerHTML="Phishing URL Detected";
}
else{
document.getElementById("result").innerHTML="Safe URL";
}

}

