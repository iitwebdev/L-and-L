function logout() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", "/logout", false);
    xmlhttp.send();
    location.reload();
}
