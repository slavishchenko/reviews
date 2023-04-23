let dev = false;

if (window.location.protocol === "http:") {
  dev = true;
}

const baseURL = `${window.location.protocol}//${window.location.hostname}`;
const port = `${window.location.port}`;
const apiURL = `api/`;

let select = document.getElementById("categorySelect");

window.addEventListener("load", () => {
  getCompanies();
});

select.addEventListener("change", () => {
  getCompanies(select.value);
});

function getCompanies(category) {
  category = category || 0;
  if (category == 0) {
    url = `${baseURL}:${port}/${apiURL}kompanije/`;
  } else {
    url = `${baseURL}:${port}/${apiURL}kompanije?category=${category}`;
  }

  fetch(url, {
    method: "get",
    credentials: "same-origin",
    headers: {
      Accept: "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      let output = "";
      if (data.length === 0) {
        output += `
                <p class="mt-5 text-nowrap lead">Nema rezultata za izabranu kategoriju.</p>
            `;
        document.getElementById("output").innerHTML = output;
      }
      data.forEach((company) => {
        let averageRating = company.average_rating ? company.average_rating : 0;
        let reviewCount = company.review_count ? company.review_count : 0;
        output += `
                <div class="col">
                    <div class="card shadow h-100">
                        <div class="card-body">
                            <h5 class="card-title text-center">
                                <a class="text-decoration-none" href="/kompanija/${
                                  company.id
                                }/${company.slug}">
                                    ${company.name}
                                </a>
                            </h5>
                            <div class="d-flex flex-wrap justify-content-center mb-3 gap-2">
                                ${Object.values(company.category)
                                  .map(function (category) {
                                    return `<span class="badge bg-success">${category}</span>`;
                                  })
                                  .join("")}
                            </div>
                            <p class="card-text text-center">Lorem ipsum dolor sit amet consectetur adipisicing elit. Ad, quis!</p>
                            <div class="d-flex justify-content-center mt-3">
                                <a href="${baseURL}:${port}/kompanija/${
          company.id
        }/recenzija/" class="text-decoration-none text-info">Podeli svoje iskustvo</a>
                            </div>
                        </div>
                        <div class="card-footer">
                            <div class="d-flex justify-content-around">
                                <div>
                                    <i class="bi bi-star-fill text-warning"></i>
                                    ${averageRating}
                                </div> 
                                <a href="/kompanija/${company.id}/${
          company.slug
        }" class="text-decoration-none">
                                    <i class="bi bi-clipboard-check-fill"></i>
                                    ${reviewCount}
                                </a> 
                                <div>
                                    <a href="${
                                      company.website_url
                                    }"><i class="bi bi-link-45deg"></i></a>
                                </div> 
                            </div>
                        </div>
                    </div>
                </div>       
            `;
        document.getElementById("output").innerHTML = output;
      });
    });
}
