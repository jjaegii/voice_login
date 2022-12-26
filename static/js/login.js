login = document.getElementById("login");
modal = document.getElementById("modal");
complete = document.getElementById("complete");

if (navigator.mediaDevices) {
  const constraints = {
    audio: true,
  };
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then((stream) => {
      const mediaRecorder = new MediaRecorder(stream);
      chunks = [];

      login.addEventListener("click", () => {
        modal.hidden = false;
        mediaRecorder.start();
        console.log("녹음 시작");
      });

      complete.addEventListener("click", () => {
        modal.hidden = true;
        mediaRecorder.stop();
        console.log("녹음 끝");
      });

      mediaRecorder.addEventListener("stop", () => {
        let blob = new Blob(chunks);

        // upload file
        let formdata = new FormData();
        formdata.append("fname", "audio.webm");
        formdata.append("data", blob);

        let xhr = new XMLHttpRequest();
        xhr.open("POST", "/login", false);
        xhr.send(formdata);
      });
    })
    .catch((err) => {
      console.log("The following error occurred" + err);
    });
}
