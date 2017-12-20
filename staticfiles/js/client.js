function addFiles(data) {
    var content = "";
    if (data === undefined) {
        // If there are no files, highlight this
        content += "<p>There are no any files</p>";
    }
    else {
        // Otherwise print list of files in table
        content += "<p>Files:</p>";
        content += "<table>";
        data.forEach(function(file) {
            content += "<tr>";
            content += "<td>" + file.username + "</td>";
            content += "<td><a href='/uploader/download/" + file.id + "/'>" + file.display_name + "</a></td>";
            content += "<td><a href='/delete/" + file.id + "/'>delete</a></td>";
            content += "</tr>";
        });
        content += "</table>";
    }
    document.getElementById("content").innerHTML = content;
};

var socket = new WebSocket("ws://localhost:1337/ws/files");

socket.onopen = function() {
  console.log("Connection is opened.");
};

socket.onclose = function(event) {
  if (event.wasClean) {
    console.log('Connection successfully closed.');
  } else {
    console.log('Connection is aborted');
  }
  console.log('Code: ' + event.code + ' reason: ' + event.reason);
};

socket.onerror = function(error) {
  console.log("Error " + error.message);
};

socket.onmessage = function(event) {
  var data = JSON.parse(event.data);
  console.log("Data received " + data.data.files);
  addFiles(data.data.files);
};
