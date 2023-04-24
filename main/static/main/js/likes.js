function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function deleteCookie(name, path, domain) {
  if (getCookie(name)) {
    document.cookie =
      name +
      "=" +
      (path ? ";path=" + path : "") +
      (domain ? ";domain=" + domain : "") +
      ";expires=Thu, 01 Jan 1970 00:00:01 GMT";
  }
}

function appendToCookie(name, value) {
  let cookie = getCookie(name);
  cookie += `,${value}`;
  document.cookie = "liked=" + cookie;
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

function sendRequest(endpoint, btn, likeCount, icon, iconFill) {
  fetch(`/${endpoint}/`, {
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
      likeCount.innerHTML = data.like_count;
      if (endpoint === "like") {
        like(btn, data, icon, iconFill);
      } else {
        dislike(btn, data, icon, iconFill);
      }
    });
}

function like(btn, data, icon, iconFill) {
  if (data.liked) {
    btn.innerHTML = iconFill;
    if (getCookie("disliked")) {
      dislikeButtons.forEach((button) => {
        if (button.value === btn.value) {
          button.innerHTML = `<i class="bi bi-caret-down text-info fs-2"></i>`;
        }
      });
    }
    deleteCookie("disliked");
    if (!getCookie("liked")) {
      document.cookie = `liked=${btn.value}`;
    } else {
      appendToCookie("liked", btn.value);
    }
  } else {
    btn.innerHTML = icon;
    deleteCookie("liked");
  }
}

function dislike(btn, data, icon, iconFill) {
  if (data.disliked) {
    btn.innerHTML = iconFill;
    if (getCookie("liked")) {
      likeButtons.forEach((button) => {
        if (button.value === btn.value) {
          button.innerHTML = `<i class="bi bi-caret-up text-info fs-2"></i>`;
        }
      });
    }
    deleteCookie("liked");
    document.cookie = `disliked=${btn.value}`;
  } else {
    btn.innerHTML = icon;
    deleteCookie("disliked");
  }
}

let caretUp = `<i class="bi bi-caret-up text-info fs-2"></i>`;
let caretDown = `<i class="bi bi-caret-down text-info fs-2"></i>`;
let caretUpFill = `<i class="bi bi-caret-up-fill text-info fs-2"></i>`;
let caretDownFill = `<i class="bi bi-caret-down-fill text-info fs-2"></i>`;

let reviews = Array.from(document.getElementsByClassName("review-detail-card"));
const userId = document
  .getElementById("likeScript")
  .getAttribute("data-user-id");
let likeButtons = Array.from(document.getElementsByClassName("btn-like"));
let dislikeButtons = Array.from(document.getElementsByClassName("btn-dislike"));

window.addEventListener("load", () => {
  console.log(document.cookie);
  let userLike = getCookie("liked");
  let userDislike = getCookie("disliked");
  reviews.forEach((review) => {
    if (review.getAttribute("data-reviewid") === userLike) {
      review.getElementsByClassName("btn-like")[0].innerHTML = caretUpFill;
    } else if (review.getAttribute("data-reviewid") === userDislike) {
      review.getElementsByClassName("btn-dislike")[0].innerHTML = caretDownFill;
    }
  });
});

likeButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (userId === "None") {
      let redirect_to = window.location.pathname;
      let loginUrl = getLoginUrl();
      window.location.href = `${loginUrl}?next=${redirect_to}`;
    } else {
      let counter = document.getElementById(`counter-${btn.value}`);
      sendRequest("like", btn, counter, caretUp, caretUpFill);
    }
  });
});

dislikeButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (userId === "None") {
      let redirect_to = window.location.pathname;
      let loginUrl = getLoginUrl();
      window.location.href = `${loginUrl}?next=${redirect_to}`;
    } else {
      let counter = document.getElementById(`counter-${btn.value}`);
      sendRequest("dislike", btn, counter, caretDown, caretDownFill);
    }
  });
});
