

function checkLogin() {

    if (!isLoggedIn) {
        alert("Please login first 🔒");
        window.location.href = "login";
        return false;
    }
    return true;
}
const menuToggle = document.getElementById("menu-toggle");
const navLinks = document.getElementById("nav-links");

menuToggle.addEventListener("click", function () {
    navLinks.classList.toggle("active");
});