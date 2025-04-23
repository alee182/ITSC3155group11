document.addEventListener("DOMContentLoaded", function () {
  // Auto-scroll to latest message
  const messages = document.querySelector(".messages");
  if (messages) {
    messages.scrollTop = messages.scrollHeight;
  }

  // Search bar filtering
  const searchInput = document.getElementById("userSearch");
  const userLinks = document.querySelectorAll(".user-link");

  searchInput.addEventListener("input", function () {
    const query = this.value.toLowerCase();

    userLinks.forEach(link => {
      const usernameElement = link.querySelector(".username");
      const username = usernameElement ? usernameElement.textContent.toLowerCase() : "";

      if (username.startsWith(query)) {
        link.style.display = "block";
      } else {
        link.style.display = "none";
      }
    });
  });
});