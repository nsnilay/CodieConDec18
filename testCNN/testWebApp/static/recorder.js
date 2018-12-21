var buttonRecord = document.getElementById("record");
var buttonStop = document.getElementById("stop");

var names = ["jsfidde", "adobe"];
var myPhoto = ["http://cdn.sstatic.net/stackoverflow/img/tag-adobe.png",
"http://mediad.publicbroadcasting.net/p/mpbn/files/201609/PrimaryLogo_RGB.png"];

buttonStop.disabled = true;

buttonRecord.onclick = function() {
    // var url = window.location.href + "record_status";
    buttonRecord.disabled = true;
    buttonStop.disabled = false;
    
    // disable download link
    var downloadLink = document.getElementById("recorder");
    downloadLink.text = "";
    downloadLink.href = "";

    var container = document.getElementById("table_container");

    var table = document.createElement("table");
    document.getElementById("table_container").appendChild(table);


    for (var i=0, len = names.length; i < len; ++i) {
        var row = document.createElement("tr"),
        name = document.createElement("td"),
        photo = document.createElement("td"),
        img = new Image();

        name.appendChild(document.createTextNode(names[i]));

        img.src = myPhoto[i];
        img.alt = names[i];
        photo.appendChild(img);

        row.appendChild(photo);
        row.appendChild(name);

        table.appendChild(row);
    }

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);
        }
    }
//    xhr.open("POST", "/record_status");
//    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
//    xhr.send(JSON.stringify({ status: "true" }));
};

buttonStop.onclick = function() {
    buttonRecord.disabled = false;
    buttonStop.disabled = true;    

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);

            // enable download link
            var downloadLink = document.getElementById("download");
            downloadLink.text = "Download Video";
            downloadLink.href = "/static/video.avi";
        }
    }
//    xhr.open("POST", "/record_status");
//    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
//    xhr.send(JSON.stringify({ status: "false" }));
};

