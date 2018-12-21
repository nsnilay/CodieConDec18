var names = ["jsfidde", "adobe"];
var myPhoto = ["http://mediad.publicbroadcasting.net/p/mpbn/files/201609/PrimaryLogo_RGB.png", "http://cdn.sstatic.net/stackoverflow/img/tag-adobe.png"];

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
