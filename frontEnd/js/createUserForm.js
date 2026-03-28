
async function createUser() {
    const username = document.getElementById("username").value;
    const fn = document.getElementById("fn").value;
    const ln = document.getElementById("ln").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const year = parseInt(document.getElementById("year").value);
    const month = parseInt(document.getElementById("month").value);
    const day = parseInt(document.getElementById("day").value);

    const weight = parseFloat(document.getElementById("weight").value);
    const height = parseFloat(document.getElementById("height").value);

    const user = JSON.stringify({
        username, 
        fn,
        ln,
        email,
        password,
        year, 
        month,
        day, 
        weight,
        height
    })

    const response = await fetch(`${CONFIG.BASE_URL}/create-user`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: user
    });

    if (response.ok) {
        window.location.href = "/login"
    } else {
        document.getElementById("error-message").style.display = "block";
    }

}