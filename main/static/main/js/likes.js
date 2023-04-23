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

let btn = document.getElementById("like");
let likeCount = document.getElementById("like_count");
let userId = btn.getAttribute("data-userid");

btn.addEventListener("click", () => {
  if (userId === "None") {
    let redirect_to = window.location.pathname;
    let loginUrl = getLoginUrl();
    window.location.href = `${loginUrl}?next=${redirect_to}`;
  } else {
    fetch("/like/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        review_id: btn.value,
      }),
    })
      .then((response) => {
        if (response.redirected === true) {
          return (window.location.href = response.url);
        } else {
          return response.json();
        }
      })
      .then((data) => {
        likeCount.innerHTML = data.like_count;
      });
  }
});
