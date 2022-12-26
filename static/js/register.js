id = document.getElementById("id");
record = document.getElementById("record");
modal = document.getElementById("modal");
complete = document.getElementById("complete");
register_btn = document.getElementById("register_btn");

if (navigator.mediaDevices) {
  const constraints = {
    audio: true,
  };
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then((stream) => {
      const mediaRecorder = new MediaRecorder(stream);
      let chunks = [];

      record.addEventListener("click", () => {
        modal.hidden = false;
        mediaRecorder.start();
        console.log("녹음 시작");
        console.log(mediaRecorder.state);
      });

      complete.addEventListener("click", () => {
        modal.hidden = true;
        mediaRecorder.stop();
        console.log("녹음 끝");
        console.log(mediaRecorder.state);
      });

      mediaRecorder.ondataavailable = (e) => {
        chunks.push(e.data);
        console.log(e.data);
        console.log(chunks[0]);
      };

      mediaRecorder.addEventListener("stop", () => {
        console.log("id : " + id.value);
        console.log("chunk : " + chunks.value);
      });

      register_btn.addEventListener("click", async () => {
        let formData = new FormData();
        formData.enctype = "multipart/form-data";
        formData.append("id", id.value);

        console.log(formData);
        formData.append("passwd", chunks[0], id.value);

        let response = await fetch("/register", {
          method: "POST",
          body: formData,
          headers: {},
        });
        await response.json().then((result) => {
          chunks = [];
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
