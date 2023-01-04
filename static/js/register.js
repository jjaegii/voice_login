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
      let count = 0;

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
        count++;
        if (count == 3) {
          register_btn.disabled = false;
          record.disabled = true;
        } else {
          record.innerText = count + 1 + "차 녹음";
        }
      });

      mediaRecorder.addEventListener("dataavailable", (event) => {
        chunks.push(event.data);
      });

      mediaRecorder.addEventListener("stop", async () => {
        console.log("id : " + id.value);
        console.log("chunk : " + chunks[0]);
        // console.log(Object.keys(chunks[0]));
        let formData = new FormData();
        formData.enctype = "multipart/form-data";
        // formData.append("id", id.value);
        formData.append("passwd", chunks[0], id.value + ".webm");
        console.log(formData);

        await fetch("/record", {
          method: "POST",
          body: formData,
        }).then((chunks = []));
      });

      register_btn.addEventListener("click", () => {
        let form = document.createElement("form");
        form.action = "/register";
        form.method = "POST";
        document.body.appendChild(form);
        form.submit();
      });
    })
    .catch((err) => {
      console.log("The following error occurred" + err);
    });
}
