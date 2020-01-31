//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;
var gumStream;
//stream from getUserMedia()
var rec;
//Recorder.js object
var input;
var audioChunks;
//MediaStreamAudioSourceNode we'll be recording
// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;

//new audio context to help us record
var record= document.getElementById("record");
record.addEventListener("click", startRecording());

function startRecording() {
	console.log("record clicked");
	$("#first").addClass('hide');
$("#loading").removeClass('hide');
    var constraints = { audio: true, video:false }
	var audioContext = new AudioContext();
	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

		gumStream = stream;
		input = audioContext.createMediaStreamSource(stream);

		rec = new Recorder(input,{numChannels:1})
		 rec.record();
        console.log("Recording started");

    setTimeout(function(){
        rec.stop();
        console.log("Recording stopped")
         gumStream.getAudioTracks()[0].stop();
    //create the wav blob and pass it on to createDownloadLink
         rec.exportWAV(createDownloadLink);
    }, 5000);
    audioChunks = [];
    record.addEventListener("dataavailable", event => {
      audioChunks.push(event.data);
    });
});

}

function createDownloadLink(blob) {
	console.log("blob", blob);
    var url = URL.createObjectURL(blob);
    var au = document.createElement('audio');
    var li = document.createElement('li');
    var link = document.createElement('a');

    //add controls to the <audio> element
    au.controls = true;
    au.src = url;
    //link the a element to the blob
    link.href = url;
    link.download = new Date().toISOString() + '.wav';
    link.innerHTML = link.download;
    //add the new audio and a elements to the li element
    li.appendChild(au);
    li.appendChild(link);
    //add the li element to the ordered list
    recordingsList.appendChild(li);

    var fileType = 'audio';
    var fileName = "sound" + '.wav';
    var formData = new FormData();
    formData.append(fileType,blob,fileName);
$.ajax({
    type: 'POST',
    url: 'http://127.0.0.1:5000',
    data: formData,
    processData: false,  // prevent jQuery from converting the data
    contentType: false,  // prevent jQuery from overriding content type
    success: function(response) {
        // alert(response);
        $("#response").append(response);
    }
});
}
