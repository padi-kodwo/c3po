let gumStream;
let input;
let URL = window.URL || window.webkitURL;
let AudioContext = window.AudioContext || window.webkitAudioContext;
const audioContext = new AudioContext;
let rec;

let chatContainer = $("#chat_container");

let micIndicator = $("#mic__indicator");
let micText = $("#mic__text");
let record =  $("#record");

record.on('click', ()=>{startRecording()});

$(document).ready((e)=>{
    console.log("document is ready for first time");
    chatContainer.append(getBotBubble("Hello"));

});

function startRecording() {
    console.log("Recording Started");
    micIndicator.css("background-color", "red");
    micText.html("Im listening to you");

    let constraint = {audio: true, video: false};


    navigator.mediaDevices.getUserMedia(constraint).then((stream)=> {
        gumStream = stream;
        input = audioContext.createMediaStreamSource(stream);

        rec = new Recorder(input, {numChannels: 1});

        rec.record();

        setTimeout(()=>{
            rec.stop();
            gumStream.getAudioTracks()[0].stop();
            rec.exportWAV(sendData)
        }, 5000);
    })
}


function sendData(blob) {
    let url = URL.createObjectURL(blob);
    let fileType = 'audio';
    let fileName = 'sound.wav';
    let formData = new FormData();
    const audio = new Audio(url);

    audio.play().then(r => console.log(r));

    formData.append(fileType, blob, fileName);
    console.log(...formData);
    micIndicator.css("background-color", "rgba(0, 128, 128, 0.1)");
    micText.html("Thinking...");

    $.ajax({
    type: 'POST',
    url: 'http://127.0.0.1:5000/c3p0',
    data: formData,
    processData: false,  // prevent jQuery from converting the data
    contentType: false,  // prevent jQuery from overriding content type
    success: function(response) {
        // alert(response);
        console.log(response);
        let audio = new Audio(response.audio);
        if(response.transcribed_text){
            chatContainer.append(getUserBubble(response.transcribed_text));
        }
        if(response.response_text){
            chatContainer.append(getBotBubble(response.response_text));
        }



        // audio.play();

    }
});

}

function getBotBubble(text ) {
    return `
<li>
<div class="bot__callout">
<span style="color: white; margin: auto; font-size: 18px; font-family: Arial, Helvetica, sans-serif">${text}</span>
</div>
</li>`
}

function getUserBubble(text) {
    return `
<li>
 <div class="user__callout">
<span style="color: #fff; margin: auto; font-size: 18px; font-family: Arial, Helvetica, sans-serif">${text}</span>
 </div></li>`
}
