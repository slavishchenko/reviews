function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

let btn = document.getElementById("like");
let likeCount = document.getElementById("like_count");

btn.addEventListener("click", () => {
  fetch("/like/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      review_id: btn.value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      likeCount.innerHTML = data.result;
    });
});
