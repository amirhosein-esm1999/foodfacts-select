// Load available brands when the page loads

document.addEventListener("DOMContentLoaded", async () => {
const brandSelect = document.getElementById("brand");
const countrySelect = document.getElementById("country");

try {
  const [brandRes, countryRes] = await Promise.all([
    fetch("/brands"),
    fetch("/countries")
  ]);

  const brands = await brandRes.json();
  const countries = await countryRes.json();

  brands.forEach(brand => {
    const option = document.createElement("option");
    option.value = brand;
    option.textContent = brand;
    brandSelect.appendChild(option);
  });

  countries.forEach(country => {
    const option = document.createElement("option");
    option.value = country;
    option.textContent = country;
    countrySelect.appendChild(option);
  });
} catch (err) {
  console.error("Failed to load brands or countries:", err);
}
});


// Handle form submission for product search
document.getElementById("search-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  const brand = document.getElementById("brand").value;
  const country = document.getElementById("country").value;

  const response = await fetch("/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ brand, country })
  });

  const data = await response.json();
  const resultsDiv = document.getElementById("results");
  resultsDiv.style.display = "block"

  if (data.length === 0) {
    resultsDiv.innerHTML = "<p>No results found.</p>";
  } else {
    resultsDiv.innerHTML = "<ul>" + data.map(product =>
      `<li><strong>${product[0]}</strong> (${product[1]}) - ${product[2]} kcal - ${product[3]}</li>`
    ).join("") + "</ul>";
  }
});
