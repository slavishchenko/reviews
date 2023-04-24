const userId = parseInt(
  document.getElementById("likeScript").getAttribute("data-user-id")
);
let likeButtons = Array.from(document.getElementsByClassName("btn-like"));
let dislikeButtons = Array.from(document.getElementsByClassName("btn-dislike"));
let reviewCards = Array.from(
  document.getElementsByClassName("review-detail-card")
);
const caretUpFill = `<i class="bi bi-caret-up-fill text-info fs-2"></i>`;
const caretDownFill = `<i class="bi bi-caret-down-fill text-info fs-2"></i>`;

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

function sendRequest(endpoint, id, likeCount) {
  fetch(`/${endpoint}/`, {
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

function getReview(id) {
  return fetch(`http://127.0.0.1:8000/api/recenzija/${id}`, {
    method: "get",
    credentials: "same-origin",
    headers: {
      Accept: "application/json",
    },
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      const review = data;
      return review;
    });
}

window.addEventListener("load", () => {
  reviewCards.forEach((card) => {
    let reviewId = card.getAttribute("data-reviewid");

    getReview(reviewId).then((review) => {
      let likes = review.likes;
      let dislikes = review.dislikes;

      if (likes.includes(userId)) {
        card.getElementsByClassName("btn-like")[0].innerHTML = caretUpFill;
      } else if (dislikes.includes(userId)) {
        card.getElementsByClassName("btn-dislike")[0].innerHTML = caretDownFill;
      } else {
        //pass
      }
    });
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
      sendRequest("like", btn.value, counter);
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
      sendRequest("dislike", btn.value, counter);
    }
  });
});
