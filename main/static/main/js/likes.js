function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function getLoginUrl() {
  const endpoint = "accounts/login/";
  const protocol = window.location.protocol;
  const domain = window.location.hostname;

  if (window.location.port) {
    return `${protocol}//${domain}:${window.location.port}/${endpoint}`;
  } else {
    return `${protocol}//${domain}/${endpoint}`;
  }
}

function like(id, likeCount) {
  fetch("/like/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      review_id: id,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      likeCount.innerHTML = data.like_count;
    });
}

const userId = document
  .getElementById("likeScript")
  .getAttribute("data-user-id");
let buttons = Array.from(document.getElementsByClassName("btn-like"));

buttons.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (userId === "None") {
      let redirect_to = window.location.pathname;
      let loginUrl = getLoginUrl();
      window.location.href = `${loginUrl}?next=${redirect_to}`;
    } else {
      let counter = document.getElementById(`counter-${btn.value}`);
      like(btn.value, counter);
    }
  });
});

// let buttons = Array.from(document.getElementsByClassName("like-btn"));
// let likeCount = document.getElementById("like-count");
// const userId = document
//   .getElementById("likeScript")
//   .getAttribute("data-user-id");

// function like(id, likeCount) {
//   fetch("/like/", {
//     method: "POST",
//     headers: {
//       "X-CSRFToken": getCookie("csrftoken"),
//     },
//     body: JSON.stringify({
//       review_id: id,
//     }),
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       likeCount.innerHTML = data.like_count;
//     });
// }

// buttons.forEach((btn) => {
//   btn.addEventListener("click", () => {
//     if (userId === "None") {
//       let redirect_to = window.location.pathname;
//       let loginUrl = getLoginUrl();
//       window.location.href = `${loginUrl}?next=${redirect_to}`;
//     } else {
//       like(btn.value, likeCount);
//     }
//   });
// });
