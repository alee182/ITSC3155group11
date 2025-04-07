document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelector(".messages");
    if (messages) {
      messages.scrollTop = messages.scrollHeight;
    }
  });

document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("userSearch");
  const userLinks = document.querySelectorAll(".user-link");

  searchInput.addEventListener("input", function () {
    const query = this.value.toLowerCase();

    userLinks.forEach(link => {
      const username = link.textContent.trim().toLowerCase();
      if (username.startsWith(query)) {
        link.style.display = "block";
      } else {
        link.style.display = "none";
      }
    });
  });
});