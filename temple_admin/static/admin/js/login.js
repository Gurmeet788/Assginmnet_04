const loginForm = document.getElementById("loginForm");
const errorMessage = document.getElementById("errorMessage");

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            errorMessage.textContent = data.error || "Login failed";
            return;
        }

        const accessToken = data.access_token;

        localStorage.setItem("access_token", accessToken);

        window.location.href = "/admin/dashboard";

    } catch (error) {
        console.error(error);
        errorMessage.textContent = "Something went wrong.";
    }
});