

function checkLogin() {

    if (!isLoggedIn) {
        alert("Please login first 🔒");
        window.location.href = "login";
        return false;
    }
    return true;
}