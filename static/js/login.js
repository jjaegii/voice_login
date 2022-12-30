login = document.getElementById("login");
modal = document.getElementById("modal");
complete = document.getElementById("complete");

let id = { value: "login_test" };

if (navigator.mediaDevices) {
  const constraints = {
    audio: true,
  };
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then((stream) => {
      const mediaRecorder = new MediaRecorder(stream);
      let chunks = [];

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

      mediaRecorder.ondataavailable = (e) => {
        chunks.push(e.data);
      };

      mediaRecorder.addEventListener("stop", () => {
        console.log("id : " + id.value);
        console.log("chunk : " + chunks.value);
      });

      mediaRecorder.addEventListener("stop", async () => {
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
