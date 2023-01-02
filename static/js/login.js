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
      const chunks = [];

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

      mediaRecorder.addEventListener("dataavailable", (event) => {
        chunks.push(event.data);
      });

      mediaRecorder.addEventListener("stop", async () => {
        let formData = new FormData();
        formData.enctype = "multipart/form-data";

        console.log(formData);
        formData.append("passwd", chunks[0], "login.webm");

        let response = await fetch("/login", {
          method: "POST",
          body: formData,
          headers: {},
        });
        await response.json().then((result) => {
          var form = document.createElement("form");
          form.setAttribute("method", "get");
          form.setAttribute("action", result.redirect);
          document.body.appendChild(form);
          form.submit();
        });
      });
    })
    .catch((err) => {
      console.log("The following error occurred" + err);
    });
}
